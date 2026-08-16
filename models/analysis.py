from datetime import datetime, timezone
from models import db

class Analysis(db.Model):
    __tablename__ = 'analyses'

    id = db.Column(db.Integer, primary_key=True)
    analysis_id = db.Column(db.String(50), unique=True, nullable=False)  # e.g., AN-2026-0001
    case_id = db.Column(db.Integer, db.ForeignKey('cases.id'), nullable=False)
    evidence_a_id = db.Column(db.Integer, db.ForeignKey('evidences.id'), nullable=False)
    evidence_b_id = db.Column(db.Integer, db.ForeignKey('evidences.id'), nullable=False)

    ssdeep_score = db.Column(db.Integer, nullable=True)  # 0 to 100
    tlsh_score = db.Column(db.Integer, nullable=True)    # TLSH distance
    tlsh_similarity_pct = db.Column(db.Integer, nullable=True) # Normalized 0 to 100
    similarity_score = db.Column(db.Integer, nullable=False) # Combined overall %
    assessment = db.Column(db.String(50), nullable=False)   # Low Similarity, Moderate Similarity, High Similarity
    notes = db.Column(db.Text, nullable=True)
    report_path = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    evidence_a = db.relationship('Evidence', foreign_keys=[evidence_a_id], backref='analyses_a')
    evidence_b = db.relationship('Evidence', foreign_keys=[evidence_b_id], backref='analyses_b')

    def to_dict(self):
        return {
            'id': self.id,
            'analysis_id': self.analysis_id,
            'case_id': self.case_id,
            'case_name': self.case.name if self.case else 'N/A',
            'case_code': self.case.case_id if self.case else 'N/A',
            'evidence_a': self.evidence_a.to_dict() if self.evidence_a else None,
            'evidence_b': self.evidence_b.to_dict() if self.evidence_b else None,
            'ssdeep_score': self.ssdeep_score,
            'tlsh_score': self.tlsh_score,
            'tlsh_similarity_pct': self.tlsh_similarity_pct,
            'similarity_score': self.similarity_score,
            'assessment': self.assessment,
            'notes': self.notes,
            'report_path': self.report_path,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
