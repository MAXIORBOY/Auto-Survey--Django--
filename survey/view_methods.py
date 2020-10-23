from datetime import datetime, timezone
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from .forms import *
import io
import urllib, base64
import numpy as np


def get_column_values_from_database(database_object, column_name):
    return list(database_object.values_list(column_name, flat=True))

def form_a_dictionary(key_list, value_list):
    return dict(zip(key_list, value_list))

def get_objects_from_list(list_, indexes):
    return [list_[index] for index in indexes]

def calculate_time_left_to_completion(survey_completion_dates_dict):
    survey_time_left = []
    current_time = datetime.now(timezone.utc)
    for key in survey_completion_dates_dict.keys():
        if survey_completion_dates_dict[key] is not None:
            time_left = survey_completion_dates_dict[key] - current_time

            if time_left.days:
                if time_left.days > 0:
                    survey_time_left.append(f'{time_left.days}d.')
                else:
                    survey_time_left.append('ended')
            elif time_left.seconds // 3600:
                survey_time_left.append(f'{time_left.seconds // 3600}h.')
            elif time_left.seconds // 60:
                survey_time_left.append(f'{time_left.seconds // 60}m.')
            elif time_left.seconds:
                survey_time_left.append(f'{time_left.seconds}s.')
            else:
                survey_time_left.append(None)
        else:
            survey_time_left.append(None)

    return survey_time_left

def merge_two_dictionaries_with_the_same_keys(dict1, dict2):
    new_dict_keys, new_dict_values = [], []
    for key in dict1.keys():
        new_dict_keys.append(dict1[key])
        new_dict_values.append(dict2[key])

    return dict(zip(new_dict_keys, new_dict_values))

def sort_dictionary(dictionary):
    return {key: value for key, value in sorted(dictionary.items(), key=lambda item: item[1], reverse=True)}

def create_plot(dictionary, top=10):
    def percent_labels(x, pos):
        return f'{x:.0f}%'
        
    matplotlib.font_manager._rebuild()
    plt.rc('font', family='Open Sans')

    fig, ax = plt.subplots()
    dictionary_keys = list(dictionary.keys())

    if len(dictionary_keys) <= top:
        plt.barh(np.arange(len(dictionary_keys)), [dictionary[key] for key in dictionary_keys], height=0.5, color='#0073e6')
        plt.yticks(np.arange(len(dictionary_keys)), tuple(dictionary_keys))
    else:
        top_dict_keys = dictionary_keys[:top]
        cumulative_perc_value_of_other_keys = 0
        for key in dictionary_keys[top:]:
            cumulative_perc_value_of_other_keys += dictionary[key]

        new_dictionary = {key: value for key, value in list(dictionary.items())[:top]}
        new_dictionary['Others'] = cumulative_perc_value_of_other_keys

        new_dictionary_keys = list(new_dictionary.keys())

        plt.barh(np.arange(len(new_dictionary_keys)), [new_dictionary[key] for key in new_dictionary_keys], height=0.5, color='#0073e6')
        plt.yticks(np.arange(len(new_dictionary_keys)), tuple(new_dictionary_keys))


    ax.set_axisbelow(True)
    ax.xaxis.grid(True, color='#EEEEEE')
    ax.xaxis.set_major_formatter(FuncFormatter(percent_labels))
    fig.tight_layout()
    plt.gca().invert_yaxis()

    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())

    return urllib.parse.quote(string)

def get_user_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ipaddress = x_forwarded_for.split(',')[-1].strip()
    else:
        ipaddress = request.META.get('REMOTE_ADDR')

    return ipaddress

def sort_ids_by_creation_date(creation_dates_dict):
    def get_creation_date(key):
        return creation_dates_dict[key]

    return sorted(list(creation_dates_dict.keys()), key=get_creation_date, reverse=True)

def get_form(form_data):
    form = SearchBar(form_data)
    if form.is_valid():
        search = form.cleaned_data['search']
        if search == '':
            search = None
    else:
        form = SearchBar()
        search = None

    return form, search
