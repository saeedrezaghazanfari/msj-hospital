from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )
account_activation_token = TokenGenerator()


class TokenPhoneGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, code, timestamp):
        return (
            six.text_type(code.id) + six.text_type(timestamp)
            # six.text_type(user.is_active)
        )
account_activation_phone_token = TokenPhoneGenerator()