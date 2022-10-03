from flask import Flask
import os


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    from flaskr.flask_web_request import page
    app.register_blueprint(page)
    app.config['VALID_FILE_EXTENSION'] = ['json', 'txt', 'png', 'sh', 'py']
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app
