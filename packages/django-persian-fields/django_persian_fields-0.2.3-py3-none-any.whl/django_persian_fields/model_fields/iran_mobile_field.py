from django.core.validators import RegexValidator
from django.db import models


class IranMobileField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 11
        kwargs["validators"] = [
            RegexValidator(
                regex=r"^09\d{9}$", message="Mobile should be like 09123456789", code="invalid_mobile"
            )
        ]
        super().__init__(*args, **kwargs)

    def check(self, **kwargs):
        return [
            *super().check(**kwargs),
        ]

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs["validators"]
        return name, path, args, kwargs

    def iso_formated(self):
        return self
