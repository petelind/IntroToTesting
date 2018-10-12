from django.test import SimpleTestCase
from django.core.exceptions import ValidationError
from todo.validators import DisallowedWordsPasswordValidator


class DisallowedWordsPasswordValidatorSimpleTestCase(SimpleTestCase):

    def test_valid_password_doesnt_raise(self):
        valid_password = "mypass"
        validator = DisallowedWordsPasswordValidator()
        try:
            validator.validate(valid_password)
        except ValidationError:
            self.fail("ValidationError thrown when validating valid password.")

    def test_invalid_password_raises(self):
        invalid_password = "mypass" + DisallowedWordsPasswordValidator.disallowed_words[0]
        validator = DisallowedWordsPasswordValidator()
        self.assertRaises(ValidationError, validator.validate, invalid_password)

    def test_invalid_password_gives_exact_message(self):
        invalid_password = "mypass" + DisallowedWordsPasswordValidator.disallowed_words[0]
        message = "Password may not contain the words: todo, task, list"

        validator = DisallowedWordsPasswordValidator()

        with self.assertRaisesMessage(ValidationError, message):
            validator.validate(invalid_password)
    
