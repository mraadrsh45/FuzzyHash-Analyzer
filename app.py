import os
from flask import Flask, render_template
from config import Config
from models import db
from services.case_service import CaseService

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize Database
    db.init_app(app)

    # Register Blueprints
    from routes.auth import auth_bp
    from routes.dashboard import dashboard_bp
    from routes.cases import cases_bp
    from routes.analysis import analysis_bp
    from routes.history import history_bp
    from routes.evidence import evidence_bp
    from routes.reports import reports_bp
    from routes.learning import learning_bp
    from routes.settings import settings_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(cases_bp)
    app.register_blueprint(analysis_bp)
    app.register_blueprint(history_bp)
    app.register_blueprint(evidence_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(learning_bp)
    app.register_blueprint(settings_bp)

    # Error Handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500

    # Initialize tables & seed initial demo dataset inside app context
    with app.app_context():
        db.create_all()
        CaseService.seed_demo_data()

    return app

if __name__ == '__main__':
    app = create_app()
    print("=================================================================")
    print("  FUZZYHASH ANALYZER - DIGITAL FORENSICS WORKSTATION ONLINE     ")
    print("  Access local interface: http://127.0.0.1:5000                 ")
    print("  Default credentials : admin / admin123                        ")
    print("=================================================================")
    app.run(host='127.0.0.1', port=5000, debug=True)
