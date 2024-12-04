import flask
from app.modules.create_user.api import user_external_views, user_internal_views

create_user_external = flask.Blueprint('create_user_external', __name__)
create_user_internal = flask.Blueprint('create_user_internal', __name__)


create_user_external.add_url_rule(
    '/api/v1/users/external/',
    view_func=user_external_views.UserExternalCreateView.as_view("create_user_external_app"),
    methods=['POST'],
)

create_user_internal.add_url_rule(
    '/api/v1/users/internal/',
    view_func=user_internal_views.UserInternalCreateView.as_view("create_user_internal_app"),
    methods=['POST'],
)