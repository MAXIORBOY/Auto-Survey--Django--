from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.simple_tag
def define(variable=None):
    return variable

@register.simple_tag
def replace_whitespaces(string):
    return string.replace(' ', '_')

@register.simple_tag
def determine_page_numbers(current_site_number):
    page_numbers = [current_site_number + i -2 for i in range(5)]
    page_numbers_min = min(page_numbers)
    if page_numbers_min < 1:
        difference = 1 - page_numbers_min
        return  list(map(lambda item: item + difference, page_numbers))
    else:
        return page_numbers

@register.filter
def get_list_item(list_, index):
    return list_[index]

@register.simple_tag
def increment_value(val):
    return val + 1

@register.simple_tag
def decrement_value(val):
    return val - 1

@register.simple_tag
def merge_url(site_mode):
    if site_mode is None:
        return ''
    return site_mode
