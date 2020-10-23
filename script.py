import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'first.settings')
django.setup()

from survey.models import Survey, Answer

def add_to_database(data_dictionary):
    new_survey = Survey(survey_name=data_dictionary['survey_name'], 
                        survey_description=data_dictionary['survey_description'], 
                        survey_photo_link=data_dictionary['survey_photo_link'],
                        survey_photo_orientation=data_dictionary.get('survey_photo_orientation', 'horizontal'), 
                        survey_type=data_dictionary['survey_type'], 
                        survey_type_parameter=data_dictionary.get('survey_type_parameter', 2),
                        survey_user_has_one_vote=data_dictionary.get('survey_user_has_one_vote', True))
    new_survey.save()

    none_list = [None] * len(data_dictionary['answer_names'])
    horizontal_list = ['horizontal'] * len(data_dictionary['answer_names'])
    for i in range(len(data_dictionary['answer_names'])):
        new_survey.answer_set.create(answer_name=data_dictionary['answer_names'][i], 
                                     answer_description=data_dictionary.get('answer_descriptions', none_list)[i], 
                                     answer_photo_link=data_dictionary.get('answer_photo_links', none_list)[i],
                                     answer_photo_orientation=data_dictionary.get('answer_photo_orientation', horizontal_list)[i])
        new_survey.answer_set.all()

# Types:
# 'single_choice' -> You must choose one out of all possible answers
# 'multi_choice' -> You can choose up to n (but at least one) out of all possible answers (checkboxes will be used)
# 'answer_comparasion' You must choose one out of n possible answers
# By default n = 2.
#------------------------------------------------------------------------------------------------------------------------------------------------#
fruits = {
    'survey_name': 'Fruits',
    'survey_description': 'Choose your favourite fruit',
    'survey_photo_link': 'https://www.healthyeating.org/images/default-source/home-0.0/nutrition-topics-2.0/general-nutrition-wellness/2-2-2-3foodgroups_fruits_detailfeature.jpg?sfvrsn=64942d53_4',
    'survey_type': 'multi_choice',
    'answer_names': [
        'Orange', 
        'Apple', 
        'Banana'], 
    'answer_photo_links': [
        'https://simlock24.pl/foto/08_40_35_orange.jpg', 
        'https://idsb.tmgrup.com.tr/ly/uploads/images/2020/05/13/35552.jpeg', 
        'https://cdn.mos.cms.futurecdn.net/42E9as7NaTaAi4A6JcuFwG-1200-80.jpg']}

vegetables = {
    'survey_name': 'Vegetables',
    'survey_description': 'Choose your favourite vegetable',
    'survey_photo_link': 'https://img1.mashed.com/img/uploads/2017/07/vegetables.jpg',
    'survey_type': 'single_choice',
    'answer_names': [
        'Carrot', 
        'Cucumber', 
        'Tomato'], 
    'answer_photo_links': [
        'https://www.jessicagavin.com/wp-content/uploads/2019/02/carrots-7-1200.jpg', 
        'https://www.naturefresh.ca/wp-content/uploads/NFF-Cucumber-19-March-2018-2.jpg', 
        'https://images-prod.healthline.com/hlcmsresource/images/AN_images/tomatoes-1296x728-feature.jpg']}

games = {
    'survey_name': 'The Best Games of all time',
    'survey_description': 'Choose your favourite game',
    'survey_photo_link': 'https://www.gry-online.pl/i/h/4/90082371.jpg',
    'survey_type': 'answer_comparasion',
    'survey_user_has_one_vote': False,
    'answer_names': [
        'Wiedźmin 3: Dziki Gon', 
        'Gothic II: Noc Kruka',
        'Mass Effect 2',
        'Gothic',
        'Dragon Age: Początek',
        'Call of Duty 4: Modern Warfare',
        'Medal of Honor: Allied Assault',
        'Grand Theft Auto V',
        'Grand Theft Auto: San Andreas',
        'The Elder Scrolls IV: Oblivion'],
    'answer_photo_links': [
        'https://cdn.gracza.pl/galeria/gry13/grupy/544003500.jpg', 
        'https://cdn.gracza.pl/galeria/gry13/13110031d.jpg',
        'https://cdn.gracza.pl/galeria/gry13/grupy/2548.jpg',
        'https://cdn.gracza.pl/galeria/gry13/1135460781.jpg',
        'https://cdn.gracza.pl/galeria/gry13/grupy/635.jpg',
        'https://cdn.gracza.pl/galeria/gry13/grupy/681.jpg',
        'https://cdn.gracza.pl/galeria/gry13/600320031.jpg',
        'https://www.gry-online.pl/galeria/gry13/3577960.jpg',
        'https://www.gry-online.pl/galeria/gry13/75840406d.jpg',
        'https://www.gry-online.pl/galeria/gry13/63218656.jpg'],
    'answer_photo_orientation': [       
        'portrait',
        'portrait',
        'portrait',
        'portrait',
        'portrait',
        'portrait',
        'portrait',
        'portrait',
        'portrait',
        'portrait']
}

#------------------------------------------------------------------------------------------------------------------------------------------------#

if __name__ == '__main__':
    #add_to_database(fruits)
    #add_to_database(vegetables)
    #add_to_database(games)
    pass
