from flask import abort, url_for, redirect, request, render_template
from flask_admin import helpers
from flask_security import current_user, Security, SQLAlchemySessionUserDatastore


def do_security(app, db, AppUser, AppRole):
    from mg_incident import admin
    from mg_incident.auth.forms import ExtendedRegisterForm, ExtendedConfirmationForm

    user_datastore = SQLAlchemySessionUserDatastore(db.session, AppUser, AppRole)
    security = Security(app, datastore=user_datastore, register_form=ExtendedRegisterForm,
                        confirm_register_form=ExtendedConfirmationForm)


    @security.context_processor
    def security_context_processor():
        """For integrations flask-admin templates to flask-security (from official docs)"""
        return dict(
            admin_base_template=admin.base_template,
            admin_view=admin.index_view,
            h=helpers,
            get_url=url_for
        )
