from django.db import models
import datetime

class Survey(models.Model):
    survey_name = models.CharField(max_length=26, unique=True)
    survey_description = models.CharField(max_length=200)
    survey_photo_link = models.CharField(max_length=300)
    survey_photo_orientation = models.CharField(max_length=50, default='horizontal', choices=(
                                                                                        ('horizontal', 'Horizontal'), 
                                                                                        ('portrait', 'Portrait')))
    survey_type = models.CharField(max_length=50, choices=(
                                                    ('single_choice', 'Single choice'), 
                                                    ('multi_choice', 'Multi choice'),
                                                    ('answer_comparasion', 'Answer comparasion')))
    survey_type_parameter = models.IntegerField(default=2)
    survey_user_has_one_vote = models.BooleanField(default=True)
    survey_creation_date = models.DateTimeField(auto_now_add=True)
    survey_completion_date = models.DateTimeField(null=True, blank=True)

    @property
    def is_survey_active(self):
        if self.survey_completion_date is None:
            return True
        else:
            if self.survey_completion_date > datetime.datetime.now(datetime.timezone.utc):
                return True
            else:
                return False
    
    def __str__(self):
        return self.survey_name

class Answer(models.Model):
    answer_name = models.CharField(max_length=25)
    answer_description = models.CharField(null=True, blank=True, max_length=200)
    answer_photo_link = models.CharField(null=True, blank=True, max_length=300)
    answer_photo_orientation = models.CharField(max_length=25, default='horizontal', choices=(
                                                                                        ('horizontal', 'Horizontal'), 
                                                                                        ('portrait', 'Portrait')))
    votes = models.IntegerField(default=0)
    answer_creation_date = models.DateTimeField(auto_now_add=True)
    survey_name = models.ForeignKey(Survey, on_delete=models.CASCADE)

    def __str__(self):
        return self.answer_name

class Visitor(models.Model):
    visitor_ip = models.GenericIPAddressField(editable=False)
    survey_name = models.ForeignKey(Survey, on_delete=models.CASCADE, editable=False)

    def __str__(self):
        return self.visitor_ip
