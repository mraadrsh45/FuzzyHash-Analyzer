from flask import Blueprint, render_template, jsonify
from routes import login_required
from models import db
from models.case import Case
from models.analysis import Analysis
from models.evidence import Evidence

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
def index():
    total_cases = Case.query.count()
    total_analyses = Analysis.query.count()

    high_sim_count = Analysis.query.filter_by(assessment='High Similarity').count()
    mod_sim_count = Analysis.query.filter_by(assessment='Moderate Similarity').count()
    low_sim_count = Analysis.query.filter_by(assessment='Low Similarity').count()

    recent_analyses = Analysis.query.order_by(Analysis.created_at.desc()).limit(8).all()
    recent_cases = Case.query.order_by(Case.created_at.desc()).limit(4).all()

    return render_template(
        'dashboard.html',
        total_cases=total_cases,
        total_analyses=total_analyses,
        high_sim_count=high_sim_count,
        mod_sim_count=mod_sim_count,
        low_sim_count=low_sim_count,
        recent_analyses=recent_analyses,
        recent_cases=recent_cases
    )

@dashboard_bp.route('/api/dashboard_metrics')
@login_required
def dashboard_metrics():
    """API endpoint for Chart.js interactive dashboard charts."""
    high = Analysis.query.filter_by(assessment='High Similarity').count()
    mod = Analysis.query.filter_by(assessment='Moderate Similarity').count()
    low = Analysis.query.filter_by(assessment='Low Similarity').count()

    # Get last 7 days activity count
    analyses = Analysis.query.order_by(Analysis.created_at.asc()).limit(30).all()
    timeline = {}
    for a in analyses:
        date_str = a.created_at.strftime('%m/%d')
        timeline[date_str] = timeline.get(date_str, 0) + 1

    return jsonify({
        'distribution': {
            'labels': ['High Similarity (71-100%)', 'Moderate Similarity (31-70%)', 'Low Similarity (0-30%)'],
            'data': [high, mod, low]
        },
        'timeline': {
            'labels': list(timeline.keys()),
            'data': list(timeline.values())
        }
    })
