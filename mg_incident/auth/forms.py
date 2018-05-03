from flask_security.forms import Required, RegisterForm, ConfirmRegisterForm, Length
from wtforms import StringField
from wtforms.validators import Regexp

from mg_incident.models import AppUser


def username_already_exist():
    message = 'This username already exist'

    def _username_already_exist(form, field):
        if AppUser.query.filter(AppUser.username == field.data).first():
            from wtforms import ValidationError
            raise ValidationError(message)

    return _username_already_exist


class ExtendedRegisterForm(RegisterForm):
    username = StringField('Username',
                            [Required('Username not provided'), username_already_exist(), Length(min=4, max=16),
                            Regexp('^(?![_])(?!.*[_]{2})[a-zA-Z0-9._]+(?<![_])$',
                                    message='Available symbols: A-Z, a-z, 0-9, _')])

class ExtendedConfirmationForm(ConfirmRegisterForm):
    username = StringField('Username',
                            [Required('Username not provided'), username_already_exist(), Length(min=4, max=16),
                            Regexp('^(?![_])(?!.*[_]{2})[a-zA-Z0-9._]+(?<![_])$',
                                    message='Available symbols: A-Z, a-z, 0-9, _')])
