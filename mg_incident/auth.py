from flask import abort, url_for, redirect, request
from flask_security import Security, SQLAlchemySessionUserDatastore, current_user


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
    security = Security(app, datastore=user_datastore)
    return security
