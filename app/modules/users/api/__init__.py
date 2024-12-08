import flask
from app.modules.users.api import (
    user_external_views,
    user_internal_views,
    users_views,
)

users = flask.Blueprint('users', __name__)

users.add_url_rule(
    '/api/v1/users/external/',
    view_func=user_external_views.UserExternalCreateView.as_view("users_external_app"),
    methods=['POST'],
)

users.add_url_rule(
    '/api/v1/users/internal/',
    view_func=user_internal_views.UserInternalCreateView.as_view("users_internal_app"),
    methods=['POST'],
)

users.add_url_rule(
    '/api/v1/users/internal/',
    view_func=users_views.UserInternalListView.as_view("list_internal_users"),
    methods=['GET'],
)

users.add_url_rule(
    '/api/v1/users/external/',
    view_func=users_views.UserExternalListView.as_view("list_external_users"),
    methods=['GET'],
)

users.add_url_rule(
    '/api/v1/users/<int:user_id>/',
    view_func=users_views.UserDeleteView.as_view("delete_users"),
    methods=['DELETE'],
)

users.add_url_rule(
    '/api/v1/users/<int:user_id>/',
    view_func=users_views.UserUpdateView.as_view("update_user_external"),
    methods=['PATCH'],
)