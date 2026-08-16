from datetime import datetime, timezone
from models import db
from models.user import User
from models.case import Case
from models.evidence import Evidence
from models.analysis import Analysis

class CaseService:
    """Service for Case, Evidence, and Analysis data management and demo data seeding."""

    @staticmethod
    def generate_case_id() -> str:
        """Generate next formatted Case ID (e.g. FH-2026-0001)."""
        year = datetime.now().year
        last_case = Case.query.order_by(Case.id.desc()).first()
        next_num = 1
        if last_case and last_case.case_id:
            try:
                parts = last_case.case_id.split('-')
                if len(parts) == 3 and parts[1] == str(year):
                    next_num = int(parts[2]) + 1
            except Exception:
                pass
        return f"FH-{year}-{next_num:04d}"

    @staticmethod
    def generate_analysis_id() -> str:
        """Generate next formatted Analysis ID (e.g. AN-2026-0001)."""
        year = datetime.now().year
        last_an = Analysis.query.order_by(Analysis.id.desc()).first()
        next_num = 1
        if last_an and last_an.analysis_id:
            try:
                parts = last_an.analysis_id.split('-')
                if len(parts) == 3 and parts[1] == str(year):
                    next_num = int(parts[2]) + 1
            except Exception:
                pass
        return f"AN-{year}-{next_num:04d}"

    @staticmethod
    def generate_evidence_id() -> str:
        """Generate next formatted Evidence ID (e.g. EV-2026-0001)."""
        year = datetime.now().year
        last_ev = Evidence.query.order_by(Evidence.id.desc()).first()
        next_num = 1
        if last_ev and last_ev.evidence_id:
            try:
                parts = last_ev.evidence_id.split('-')
                if len(parts) == 3 and parts[1] == str(year):
                    next_num = int(parts[2]) + 1
            except Exception:
                pass
        return f"EV-{year}-{next_num:04d}"

    @classmethod
    def seed_demo_data(cls):
        """Seed initial demo user, case, evidence, and analysis records clearly marked as DEMO DATA."""
        # Ensure default admin user
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', role='Senior Forensic Analyst')
            admin.set_password('admin123')
            db.session.add(admin)

        # Ensure demo case
        demo_case = Case.query.filter_by(case_id='FH-2026-0001').first()
        if not demo_case:
            demo_case = Case(
                case_id='FH-2026-0001',
                name='DEMO - Operation Cobalt File Comparison',
                description='[DEMO DATA] Benchmark forensic investigation comparing suspected derivative payload against reference baseline sample.',
                investigator='Det. M. Sakib',
                status='In Progress'
            )
            db.session.add(demo_case)
            db.session.flush()

            # Demo Evidence items
            ev_a = Evidence(
                evidence_id='EV-2026-0001',
                case_id=demo_case.id,
                filename='baseline_payload_v1.bin',
                original_filename='baseline_payload_v1.bin',
                file_path='demo/baseline_payload_v1.bin',
                file_size=1048576,  # 1 MB
                mime_type='application/octet-stream',
                md5='e10adc3949ba59abbe56e057f20f883e',
                sha256='8613a5217992764b815610e2f5b66d48e89f81a798939c3666d9b897f1f4a9b5',
                fuzzy_hash_ssdeep='24:hMCEm8gMFMEFZL89aXqQL:hum8FMEte9aX',
                fuzzy_hash_tlsh='T18A947B12C45E67890123456789ABCDEF0123456789ABCDEF0123456789ABCDEF012'
            )
            ev_b = Evidence(
                evidence_id='EV-2026-0002',
                case_id=demo_case.id,
                filename='variant_payload_v2.bin',
                original_filename='variant_payload_v2.bin',
                file_path='demo/variant_payload_v2.bin',
                file_size=1052672,  # ~1.00 MB
                mime_type='application/octet-stream',
                md5='c33367701511b4f6020ec61ded352059',
                sha256='29177114b301f2e6b12a875a610f443b8110b64d1f2e6281a8b941551f337f2a',
                fuzzy_hash_ssdeep='24:hMCEm8gMFMEFZL89aXqQK:hum8FMEte9aY',
                fuzzy_hash_tlsh='T18A947B12C45E67890123456789ABCDEF0123456789ABCDEF0123456789ABCDEF014'
            )
            db.session.add_all([ev_a, ev_b])
            db.session.flush()

            # Demo Analysis
            demo_an = Analysis(
                analysis_id='AN-2026-0001',
                case_id=demo_case.id,
                evidence_a_id=ev_a.id,
                evidence_b_id=ev_b.id,
                ssdeep_score=94,
                tlsh_score=12,
                tlsh_similarity_pct=96,
                similarity_score=94,
                assessment='High Similarity',
                notes='[DEMO DATA] Both samples exhibit 94% ssdeep CTPH similarity and 12 TLSH distance (96% similarity), indicating structural code derivative lineage.'
            )
            db.session.add(demo_an)

            # Second demo analysis (Low similarity)
            ev_c = Evidence(
                evidence_id='EV-2026-0003',
                case_id=demo_case.id,
                filename='unrelated_system_log.txt',
                original_filename='unrelated_system_log.txt',
                file_path='demo/unrelated_system_log.txt',
                file_size=45820,
                mime_type='text/plain',
                md5='5d41402abc4b2a76b9719d911017c592',
                sha256='e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
                fuzzy_hash_ssdeep='12:aB3xZ9mN2pQ1rS:aBxZ9mN',
                fuzzy_hash_tlsh='T15F947B12C45E67890123456789ABCDEF0123456789ABCDEF0123456789ABCDEF999'
            )
            db.session.add(ev_c)
            db.session.flush()

            demo_an2 = Analysis(
                analysis_id='AN-2026-0002',
                case_id=demo_case.id,
                evidence_a_id=ev_a.id,
                evidence_b_id=ev_c.id,
                ssdeep_score=0,
                tlsh_score=280,
                tlsh_similarity_pct=6,
                similarity_score=3,
                assessment='Low Similarity',
                notes='[DEMO DATA] Baseline payload compared against plain system log file. 3% overall similarity confirms distinct file structures.'
            )
            db.session.add(demo_an2)

        db.session.commit()
