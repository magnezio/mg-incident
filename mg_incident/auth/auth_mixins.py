from flask import abort, url_for, redirect, request
from flask_security import current_user


class AuthRequiredMixin():
    def is_accessible(self):
        return self._current_user_is_aa()

    def _current_user_is_aa(self):
        if current_user.is_active or current_user.is_authenticated:
            return True
        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users
        when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                abort(403)
            else:
                return redirect(url_for('security.login', next=request.url))


class AdminRequiredMixin(AuthRequiredMixin):
    def is_accessible(self):
        return self._current_user_is_aa() and current_user.has_role('admin')


class ManagerRequiredMixin(AdminRequiredMixin):
    def is_accessible(self):
        return super().is_accessible() or \
            (current_user.has_role('manager') and self._current_user_is_aa())


class UserRequiredMixin(ManagerRequiredMixin):
    def is_accessible(self):
        return super().is_accessible() or \
            (current_user.has_role('user') and self._current_user_is_aa())


class WorkerRequiredMixin(ManagerRequiredMixin):
    def is_accessible(self):
        return super().is_accessible() or \
            (current_user.has_role('worker') and self._current_user_is_aa())
