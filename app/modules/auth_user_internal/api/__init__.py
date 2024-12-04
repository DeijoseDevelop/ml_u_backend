import flask

from app.modules.auth_user_internal.api import view


auth_user_internal = flask.Blueprint("auth_user", __name__)

auth_user_internal.add_url_rule(
    "/api/v1/auth/login/",
    view_func=view.UserInternaAuthView.as_view("auth_user_interl_app"),
    methods=["POST"]
)
