from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Import blueprint groups from each module
    from app.auth import blueprints as auth_bps
    
    # Adding all the blueprints
    all_blueprints = auth_bps

    for bp in all_blueprints:
        app.register_blueprint(bp)
        
    return app
