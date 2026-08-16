from flask import Blueprint, render_template, request, redirect, url_for, flash
from routes import login_required
from models import db
from models.analysis import Analysis
from models.evidence import Evidence
from models.case import Case
from services.file_validation_service import FileValidationService
from services.case_service import CaseService
from config import Config

settings_bp = Blueprint('settings', __name__)

@settings_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'clear_temp':
            FileValidationService.cleanup_directory(Config.UPLOAD_FOLDER)
            FileValidationService.cleanup_directory(Config.REPORT_FOLDER)
            flash('Temporary processing uploads and generated reports successfully cleared.', 'success')

        elif action == 'reset_demo':
            try:
                Analysis.query.delete()
                Evidence.query.delete()
                Case.query.delete()
                db.session.commit()
                CaseService.seed_demo_data()
                flash('Database reset and DEMO DATA successfully re-seeded.', 'success')
            except Exception as e:
                db.session.rollback()
                flash(f'Failed to reset database: {str(e)}', 'danger')

        return redirect(url_for('settings.index'))

    max_mb = Config.MAX_CONTENT_LENGTH / (1024 * 1024)
    return render_template('settings.html', max_upload_mb=max_mb)
