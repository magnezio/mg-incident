from flask import abort, url_for, redirect, request, render_template
from flask_security import Security, SQLAlchemySessionUserDatastore, current_user
from flask_security.forms import Required, ConfirmRegisterForm, Length
from wtforms import StringField
from wtforms.validators import Regexp


class AuthRequiredMixin():
    def is_accessible(self):
        if current_user.is_active or current_user.is_authenticated:
            return True
        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                abort(403)
            else:
                return redirect(url_for('security.login', next=request.url))


class UserRequiredMixin(AuthRequiredMixin):
    def is_accessible(self):
        result = all([
            super().is_accessible(), any([
                current_user.has_role('user'), current_user.has_role('admin'),
            ]),
        ])
        return result


class AdminRequiredMixin(UserRequiredMixin):
    def is_accessible(self):
        result = all([
            super().is_accessible(), current_user.has_role('admin'),
        ])
        return result


def do_security(app, db, AppUser, AppRole):
    user_datastore = SQLAlchemySessionUserDatastore(
        db.session, AppUser, AppRole
    )

    from flask_security.forms import RegisterForm

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

    security = Security(app, datastore=user_datastore, register_form=ExtendedRegisterForm,
                        confirm_register_form=ExtendedConfirmationForm)

    from mg_incident import admin
    from flask_admin import helpers

    @security.context_processor
    def security_context_processor():
        """For integrations flask-admin templates to flask-security (from official docs)"""
        return dict(
            admin_base_template=admin.base_template,
            admin_view=admin.index_view,
            h=helpers,
            get_url=url_for
        )

    return security
