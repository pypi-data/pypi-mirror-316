import re

from rest_framework.fields import Field


class SerializerIranMobileField(Field):
    default_error_messages = {
        'invalid_mobile': 'Mobile should be like 09123456789',
    }
    def to_internal_value(self, data):
        if not re.match("^09\d{9}$", data):
            self.fail("invalid_mobile")
        return data

    def to_representation(self, value):
        return value
