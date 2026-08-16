from flask import Blueprint, render_template, request
from routes import login_required
from models import db
from models.analysis import Analysis

history_bp = Blueprint('history', __name__)

@history_bp.route('/history')
@login_required
def index():
    query = request.args.get('q', '').strip()
    assessment_filter = request.args.get('filter', '').strip()

    analysis_query = Analysis.query

    if query:
        analysis_query = analysis_query.filter(
            (Analysis.analysis_id.ilike(f"%{query}%")) |
            (Analysis.notes.ilike(f"%{query}%"))
        )

    if assessment_filter and assessment_filter != 'All':
        if assessment_filter == 'Low':
            analysis_query = analysis_query.filter_by(assessment='Low Similarity')
        elif assessment_filter == 'Moderate':
            analysis_query = analysis_query.filter_by(assessment='Moderate Similarity')
        elif assessment_filter == 'High':
            analysis_query = analysis_query.filter_by(assessment='High Similarity')

    analyses = analysis_query.order_by(Analysis.created_at.desc()).all()

    return render_template(
        'history.html',
        analyses=analyses,
        search_query=query,
        current_filter=assessment_filter
    )
