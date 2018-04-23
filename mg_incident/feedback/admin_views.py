from flask_admin.contrib.sqla import ModelView

from mg_incident import admin, db
from mg_incident.feedback import models


class FeedbackView(ModelView):
    pass


admin.add_view(FeedbackView(models.Feedback, db.session))
