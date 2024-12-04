from app.config import *
from app.modules.category_classificator import api as classificator_apps
from app.modules.user_recognition import api as recognition_apps
from app.modules.create_user import api as user_create


# Apps
app.register_blueprint(classificator_apps.category_classificator_app)
app.register_blueprint(recognition_apps.user_recognition_app)
app.register_blueprint(user_create.create_user_external)
app.register_blueprint(user_create.create_user_internal)

with app.app_context():
    db.create_all()

# Run Application
if __name__ == '__main__':
    app.run(debug=True)