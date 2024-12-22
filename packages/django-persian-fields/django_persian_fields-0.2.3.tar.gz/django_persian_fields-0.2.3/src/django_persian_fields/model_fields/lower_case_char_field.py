from django.db import models

class LowerCaseCharField(models.CharField):

    def get_prep_value(self, value):
        return super().get_prep_value(value.lower() if value else value)
