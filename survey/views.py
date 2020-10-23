from django.shortcuts import render, redirect
from django.db.models import F
from django.http import HttpResponseNotFound
from urllib.parse import urlparse
from .models import *
from .forms import *
from .view_methods import *
import random
from datetime import datetime, timezone
import math as mth


def home_page(request, **kwargs):
    form, search = get_form(request.GET)
    search_results = None

    if kwargs.get('search', None) is not None:
        search = kwargs['search']

    error_code = 0
    if request.session.get('survey_expired_while_voting', False) is True:
        error_code = 1
        request.session['survey_expired_while_voting'] = None
    elif request.session.get('user_already_voted', False) is True:
        error_code = 2
        request.session['user_already_voted'] = None

    vote_successful = False
    if request.session.get('vote_successful', False) is True:
        vote_successful = True
        request.session['vote_successful'] = None

    survey_database = Survey.objects.all()
    survey_ids = get_column_values_from_database(survey_database, 'pk')
    survey_ids.sort(key=lambda index: survey_database.get(pk=index).survey_creation_date, reverse=True)

    site_mode = kwargs.get('mode', None)
    if site_mode is not None:
        if site_mode == 'archives':
           survey_ids = list(filter(lambda index: not(survey_database.get(pk=index).is_survey_active), survey_ids))

        elif site_mode == 'current':
            survey_ids = list(filter(lambda index: survey_database.get(pk=index).is_survey_active, survey_ids))

    if search is not None:
        survey_ids = list(survey_database.filter(survey_name__icontains=search.replace('+', ' ')).values_list('id', flat=True))
        survey_ids.sort(key=lambda index: survey_database.get(pk=index).survey_creation_date, reverse=True)
        search_results = len(survey_ids)

    surveys_on_site = 10
    current_site_number = kwargs.get('page', 1)
    max_sites = int(mth.ceil(len(survey_ids) / surveys_on_site))

    if current_site_number > max_sites and max_sites != 0:
        return HttpResponseNotFound('<h1>Page not found!</h1>')

    survey_ids = survey_ids[surveys_on_site * (current_site_number - 1) : surveys_on_site * current_site_number]
    site_dictionary = {}
    database = []

    for survey_id in survey_ids:
        database.append(Survey.objects.values().filter(pk=survey_id))

    if len(database):
        column_names = list(database[0][0].keys())
        column_names.remove('id')
        for i in range(len(database)):
            for column_name in column_names:
                try:
                    site_dictionary[f'{column_name}s'].update({survey_ids[i]: database[i][0][column_name]})
                except KeyError:
                    site_dictionary[f'{column_name}s'] = {survey_ids[i]: database[i][0][column_name]}

        site_dictionary['survey_ids'] = sort_ids_by_creation_date(site_dictionary['survey_creation_dates'])
        site_dictionary['survey_completion_time_left'] = form_a_dictionary(survey_ids, calculate_time_left_to_completion(site_dictionary['survey_completion_dates']))

    site_dictionary['error_code'] = error_code
    site_dictionary['vote_successful'] = vote_successful
    site_dictionary['current_site_number'] = current_site_number
    site_dictionary['max_sites'] = max_sites
    site_dictionary['site_mode'] = site_mode
    site_dictionary['form'] = form
    site_dictionary['search'] = search
    site_dictionary['search_results'] = search_results

    return render(request, "survey/home.html", site_dictionary)

def survey(request):
    def restore_survey_field_values(request):
        survey_name = str(''.join(filter(lambda char: char != '/', request.path))).replace('_', ' ')
        survey = Survey.objects.filter(survey_name=survey_name)
        survey_id = int(get_column_values_from_database(survey.values('id'), 'id')[0])
        survey_type = str(get_column_values_from_database(survey, 'survey_type')[0])
        survey_type_parameter = int(get_column_values_from_database(survey, 'survey_type_parameter')[0])
        survey_completion_date = get_column_values_from_database(survey, 'survey_completion_date')[0]
        survey_user_has_one_vote = get_column_values_from_database(survey, 'survey_user_has_one_vote')[0]

        return {
            'survey_id': survey_id,
            'survey_name': survey_name, 
            'survey_type': survey_type, 
            'survey_type_parameter': survey_type_parameter,
            'survey_completion_date': survey_completion_date,
            'survey_user_has_one_vote': survey_user_has_one_vote}

    def get_valid_values(values):
        return [retrieved_value for retrieved_value in values if retrieved_value is not None]

    def check_multi_choice_input_correctness(valid_values, max_checks):
        if not len(valid_values):
            return 1
        elif len(valid_values) > max_checks:
            return 2
        else:
            return 0

    def generate_answers_for_answer_comparasion(range_, sample):
        return random.sample(range(range_), sample)


    form, search = get_form(request.GET)
    site_dictionary = restore_survey_field_values(request)
    multi_choice_error_code = 0

    if request.method == "POST": # hit vote button
        if Survey.objects.get(id=site_dictionary['survey_id']).is_survey_active: # survey is still active
            values = [request.POST[key] for key in request.POST.keys() if 'voting_object_' in key]
            valid_values = get_valid_values(values)
            if site_dictionary['survey_type'] == 'multi_choice':
                multi_choice_error_code = check_multi_choice_input_correctness(valid_values, site_dictionary['survey_type_parameter'])

            if site_dictionary['survey_type'] != 'multi_choice' or site_dictionary['survey_type'] == 'multi_choice' and multi_choice_error_code == 0: # multi-choice input is correct
                for value in valid_values:
                    Answer.objects.filter(id=int(value)).update(votes=F('votes')+1)
                if len(valid_values):
                    if site_dictionary['survey_user_has_one_vote']:
                        survey = Survey.objects.get(id=site_dictionary['survey_id'])
                        survey.visitor_set.create(visitor_ip=get_user_ip(request))
                        survey.visitor_set.all()
                    request.session['vote_successful'] = True
                    return redirect(home_page)
            else: # multi-choice input is incorrect
                request.method = 'GET'
        else: # survey is no longer active
            request.session['survey_expired_while_voting'] = True
            return redirect(home_page)

    if request.method == 'GET': # did not hit vote button
        survey_answer_fields = Answer.objects.filter(survey_name=site_dictionary['survey_id'])
        answer_ids = get_column_values_from_database(survey_answer_fields, 'id')
        site_dictionary['answer_ids'] = answer_ids
        
        if Survey.objects.get(id=site_dictionary['survey_id']).is_survey_active: # survey is stil active -> show balot
            visitors = Visitor.objects.filter(survey_name=site_dictionary['survey_id'])
            if not site_dictionary['survey_user_has_one_vote'] or get_user_ip(request) not in set(get_column_values_from_database(visitors, 'visitor_ip')): # no voting limits or user did not vote yet
                site_dictionary['multi_choice_error_code'] = multi_choice_error_code

                if site_dictionary['survey_type'] != 'answer_comparasion':
                    for answer_field_name in [f.name for f in Answer._meta.get_fields(include_parents=False)]:
                        if answer_field_name != 'id' and answer_field_name != 'votes' and answer_field_name != 'survey_name':
                            site_dictionary[f'{answer_field_name}s'] = form_a_dictionary(answer_ids, get_column_values_from_database(survey_answer_fields, answer_field_name))
                else:
                    generated_indexes = generate_answers_for_answer_comparasion(len(answer_ids), site_dictionary['survey_type_parameter'])
                    site_dictionary['answer_ids'] = get_objects_from_list(site_dictionary['answer_ids'], generated_indexes)
                    for answer_field_name in [f.name for f in Answer._meta.get_fields(include_parents=False)]:
                        if answer_field_name != 'id' and answer_field_name != 'votes' and answer_field_name != 'survey_name':
                            site_dictionary[f'{answer_field_name}s'] = form_a_dictionary(get_objects_from_list(answer_ids, generated_indexes), 
                                                                                         get_objects_from_list(get_column_values_from_database(survey_answer_fields, answer_field_name), generated_indexes))
            else: # user already voted
                request.session['user_already_voted'] = True
                return redirect(home_page)

        else: # survey is no longer active -> show results
            survey_dictionary_votes = sort_dictionary(merge_two_dictionaries_with_the_same_keys(form_a_dictionary(answer_ids, get_column_values_from_database(survey_answer_fields, 'answer_name')),
                                                                                form_a_dictionary(answer_ids, get_column_values_from_database(survey_answer_fields, 'votes'))))
            
            total_votes = sum(list(survey_dictionary_votes.values()))
            survey_dictionary_perc_votes = {key: round(100 * value / total_votes, 2) for key, value in survey_dictionary_votes.items()}
            
            site_dictionary['total_votes'] = total_votes
            site_dictionary['answer_names'] = list(survey_dictionary_votes.keys())
            site_dictionary['survey_dictionary_votes'] = survey_dictionary_votes
            site_dictionary['survey_dictionary_perc_votes'] = survey_dictionary_perc_votes
            site_dictionary['survey_plot'] = create_plot(survey_dictionary_perc_votes)

    site_dictionary['multi_choice_error_code'] = multi_choice_error_code
    site_dictionary['form'] = form
    return render(request, 'survey/vote.html', site_dictionary)
