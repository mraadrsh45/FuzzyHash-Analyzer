from datetime import datetime, timezone
from models import db

class Evidence(db.Model):
    __tablename__ = 'evidences'

    id = db.Column(db.Integer, primary_key=True)
    evidence_id = db.Column(db.String(50), unique=True, nullable=False) # e.g. EV-2026-0001
    case_id = db.Column(db.Integer, db.ForeignKey('cases.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)
    mime_type = db.Column(db.String(100), nullable=False)
    md5 = db.Column(db.String(32), nullable=False)
    sha256 = db.Column(db.String(64), nullable=False)
    fuzzy_hash_ssdeep = db.Column(db.Text, nullable=True)
    fuzzy_hash_tlsh = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            'id': self.id,
            'evidence_id': self.evidence_id,
            'case_id': self.case_id,
            'filename': self.filename,
            'original_filename': self.original_filename,
            'file_size': self.file_size,
            'mime_type': self.mime_type,
            'md5': self.md5,
            'sha256': self.sha256,
            'fuzzy_hash_ssdeep': self.fuzzy_hash_ssdeep,
            'fuzzy_hash_tlsh': self.fuzzy_hash_tlsh,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
