from app.config import *
from app.modules.category_classificator import api as classificator_apps
from app.modules.user_recognition import api as recognition_apps
from app.modules.users import api as users_app
from app.modules.auth_user_internal import api as auth_user


# Apps
app.register_blueprint(classificator_apps.category_classificator_app)
app.register_blueprint(recognition_apps.user_recognition_app)
app.register_blueprint(users_app.users)
app.register_blueprint(auth_user.auth_user_internal)

with app.app_context():
    db.create_all()

# Run Application
if __name__ == '__main__':
    app.run(debug=True)