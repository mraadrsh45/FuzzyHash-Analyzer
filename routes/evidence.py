from flask import Blueprint, render_template, request
from routes import login_required
from models import db
from models.evidence import Evidence

evidence_bp = Blueprint('evidence', __name__)

@evidence_bp.route('/evidence')
@login_required
def index():
    query = request.args.get('q', '').strip()
    evidence_query = Evidence.query

    if query:
        evidence_query = evidence_query.filter(
            (Evidence.evidence_id.ilike(f"%{query}%")) |
            (Evidence.original_filename.ilike(f"%{query}%")) |
            (Evidence.md5.ilike(f"%{query}%")) |
            (Evidence.sha256.ilike(f"%{query}%"))
        )

    evidences = evidence_query.order_by(Evidence.created_at.desc()).all()
    return render_template('evidence.html', evidences=evidences, search_query=query)
