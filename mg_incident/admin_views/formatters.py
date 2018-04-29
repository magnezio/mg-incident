import datetime
from flask_admin.model import typefmt


def date_format(view, value):
    return value.strftime('%d.%m.%Y %I:%M')

DEFAULT_FORMATTERS = dict(typefmt.BASE_FORMATTERS)
DEFAULT_FORMATTERS.update({
        type(None): lambda *args: "-",
        datetime.date: date_format
})
