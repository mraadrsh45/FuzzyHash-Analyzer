import os
from flask import Blueprint, render_template, send_file, flash, redirect, url_for
from routes import login_required
from models import db
from models.analysis import Analysis
from services.report_service import ReportService

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/reports')
@login_required
def index():
    analyses = Analysis.query.order_by(Analysis.created_at.desc()).all()
    return render_template('reports.html', analyses=analyses)

@reports_bp.route('/reports/<analysis_id>')
@login_required
def view_report(analysis_id):
    analysis_record = Analysis.query.filter_by(analysis_id=analysis_id).first_or_404()
    return render_template('report.html', analysis=analysis_record)

@reports_bp.route('/reports/<analysis_id>/download')
@login_required
def download_report(analysis_id):
    analysis_record = Analysis.query.filter_by(analysis_id=analysis_id).first_or_404()

    report_path = analysis_record.report_path
    if not report_path or not os.path.exists(report_path):
        # Generate on demand
        try:
            an_dict = analysis_record.to_dict()
            an_dict['investigator'] = analysis_record.case.investigator if analysis_record.case else 'Forensic Investigator'
            report_path = ReportService.generate_pdf_report(an_dict)
            analysis_record.report_path = report_path
            db.session.commit()
        except Exception as e:
            flash(f"Error generating PDF report: {str(e)}", "danger")
            return redirect(url_for('reports.view_report', analysis_id=analysis_id))

    return send_file(
        report_path,
        as_attachment=True,
        download_name=f"Forensic_Report_{analysis_record.analysis_id}.pdf",
        mimetype='application/pdf'
    )
