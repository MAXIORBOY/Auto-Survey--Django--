from django.contrib import admin
from .models import *

class SurveyAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'survey_creation_date',)

class AnswerAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'answer_creation_date',)

class VisitorAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'survey_name',)

admin.site.register(Survey, SurveyAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Visitor, VisitorAdmin)
