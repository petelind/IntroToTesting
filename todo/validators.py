from django.core.exceptions import ValidationError


class DisallowedWordsPasswordValidator(object):
    """
    DisallowedWordsPasswordValidator ensures that the user's password
    does not contain any of the words in disallowed_words.
    """

    disallowed_words = ['todo', 'task', 'list']

    def __init__(self, min_length=1):
        self.min_length = min_length

    def validate(self, password, user=None):

        if (any(word in password for word in self.disallowed_words)):
            raise ValidationError("Password may not contain the words: {}".format(
                ", ".join(self.disallowed_words)
            ))

    def get_help_text(self):
        return ""