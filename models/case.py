from datetime import datetime, timezone
from models import db

class Case(db.Model):
    __tablename__ = 'cases'

    id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.String(50), unique=True, nullable=False)  # e.g., FH-2026-0001
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    investigator = db.Column(db.String(100), nullable=False, default='Lead Investigator')
    status = db.Column(db.String(30), nullable=False, default='Open')  # Open, In Progress, Closed
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    evidences = db.relationship('Evidence', backref='case', lazy=True, cascade='all, delete-orphan')
    analyses = db.relationship('Analysis', backref='case', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'case_id': self.case_id,
            'name': self.name,
            'description': self.description,
            'investigator': self.investigator,
            'status': self.status,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            'evidence_count': len(self.evidences),
            'analysis_count': len(self.analyses)
        }
