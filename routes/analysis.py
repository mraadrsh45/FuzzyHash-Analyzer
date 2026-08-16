import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from routes import login_required
from models import db
from models.case import Case
from models.evidence import Evidence
from models.analysis import Analysis
from services.file_validation_service import FileValidationService, FileValidationError
from services.hash_service import HashService
from services.fuzzy_hash_service import FuzzyHashService
from services.similarity_service import SimilarityService
from services.metadata_service import MetadataService
from services.case_service import CaseService
from services.report_service import ReportService

analysis_bp = Blueprint('analysis', __name__)

@analysis_bp.route('/analysis/new')
@login_required
def new_analysis():
    cases = Case.query.order_by(Case.created_at.desc()).all()
    selected_case_id = request.args.get('case_id')
    return render_template('analysis.html', cases=cases, selected_case_id=selected_case_id)

@analysis_bp.route('/analysis/run', methods=['POST'])
@login_required
def run_analysis():
    case_db_id = request.form.get('case_id')
    analyst_notes = request.form.get('notes', '').strip()
    
    file_a = request.files.get('file_a')
    file_b = request.files.get('file_b')

    if not case_db_id:
        flash('Please select a target forensic case for this analysis.', 'danger')
        return redirect(url_for('analysis.new_analysis'))

    case_obj = Case.query.get(case_db_id)
    if not case_obj:
        flash('Target case not found.', 'danger')
        return redirect(url_for('analysis.new_analysis'))

    if not file_a or not file_b or not file_a.filename or not file_b.filename:
        flash('Both File A and File B must be selected for similarity analysis.', 'danger')
        return redirect(url_for('analysis.new_analysis'))

    saved_path_a = None
    saved_path_b = None

    try:
        # Step 1 & 2: Validate Files
        val_a = FileValidationService.validate_file(file_a)
        val_b = FileValidationService.validate_file(file_b)

        # Step 3: Save temporary safe non-executable paths
        saved_path_a, name_a = FileValidationService.save_temp_file(file_a)
        saved_path_b, name_b = FileValidationService.save_temp_file(file_b)

        # Step 4: Extract Metadata & PE Info
        meta_a = MetadataService.extract_metadata(saved_path_a, val_a['original_filename'])
        meta_b = MetadataService.extract_metadata(saved_path_b, val_b['original_filename'])

        # Step 5 & 6: Cryptographic Hashes
        hashes_a = HashService.calculate_all(saved_path_a)
        hashes_b = HashService.calculate_all(saved_path_b)

        # Step 7: Fuzzy Hashes
        fuzzy_a = FuzzyHashService.generate_all(saved_path_a)
        fuzzy_b = FuzzyHashService.generate_all(saved_path_b)

        # Step 8 & 9: Similarity & Assessment
        eval_result = SimilarityService.evaluate(
            fuzzy_a['ssdeep'], fuzzy_b['ssdeep'],
            fuzzy_a['tlsh'], fuzzy_b['tlsh']
        )

        # Step 10: Save Evidence Items
        ev_id_a = CaseService.generate_evidence_id()
        evidence_a = Evidence(
            evidence_id=ev_id_a,
            case_id=case_obj.id,
            filename=name_a,
            original_filename=val_a['original_filename'],
            file_path=saved_path_a,
            file_size=val_a['file_size'],
            mime_type=meta_a['mime_type'],
            md5=hashes_a['md5'],
            sha256=hashes_a['sha256'],
            fuzzy_hash_ssdeep=fuzzy_a['ssdeep'],
            fuzzy_hash_tlsh=fuzzy_a['tlsh']
        )
        db.session.add(evidence_a)
        db.session.flush()

        ev_id_b = CaseService.generate_evidence_id()
        evidence_b = Evidence(
            evidence_id=ev_id_b,
            case_id=case_obj.id,
            filename=name_b,
            original_filename=val_b['original_filename'],
            file_path=saved_path_b,
            file_size=val_b['file_size'],
            mime_type=meta_b['mime_type'],
            md5=hashes_b['md5'],
            sha256=hashes_b['sha256'],
            fuzzy_hash_ssdeep=fuzzy_b['ssdeep'],
            fuzzy_hash_tlsh=fuzzy_b['tlsh']
        )
        db.session.add(evidence_b)
        db.session.flush()

        # Step 11 & 12: Save Analysis
        an_code = CaseService.generate_analysis_id()
        analysis_record = Analysis(
            analysis_id=an_code,
            case_id=case_obj.id,
            evidence_a_id=evidence_a.id,
            evidence_b_id=evidence_b.id,
            ssdeep_score=eval_result['ssdeep_score'],
            tlsh_score=eval_result['tlsh_distance'],
            tlsh_similarity_pct=eval_result['tlsh_similarity_pct'],
            similarity_score=eval_result['overall_score'],
            assessment=eval_result['assessment'],
            notes=analyst_notes or eval_result['description']
        )
        db.session.add(analysis_record)
        db.session.commit()

        # Step 13: Generate PDF Report asynchronously / cached
        try:
            an_dict = analysis_record.to_dict()
            an_dict['investigator'] = case_obj.investigator
            report_path = ReportService.generate_pdf_report(an_dict)
            analysis_record.report_path = report_path
            db.session.commit()
        except Exception as pdf_err:
            print(f"PDF generation note: {pdf_err}")

        flash(f"Forensic Analysis {an_code} completed successfully.", "success")
        return redirect(url_for('analysis.results', analysis_id=analysis_record.analysis_id))

    except FileValidationError as e:
        FileValidationService.cleanup_file(saved_path_a)
        FileValidationService.cleanup_file(saved_path_b)
        flash(f"File Validation Error: {str(e)}", "danger")
        return redirect(url_for('analysis.new_analysis'))
    except Exception as ex:
        FileValidationService.cleanup_file(saved_path_a)
        FileValidationService.cleanup_file(saved_path_b)
        flash(f"Analysis Error: {str(ex)}", "danger")
        return redirect(url_for('analysis.new_analysis'))

@analysis_bp.route('/analysis/<analysis_id>')
@login_required
def results(analysis_id):
    analysis_record = Analysis.query.filter_by(analysis_id=analysis_id).first_or_404()
    
    meta_a = MetadataService.get_pe_info(analysis_record.evidence_a.file_path) if os.path.exists(analysis_record.evidence_a.file_path) else None
    meta_b = MetadataService.get_pe_info(analysis_record.evidence_b.file_path) if os.path.exists(analysis_record.evidence_b.file_path) else None

    eval_meta = SimilarityService.evaluate(
        analysis_record.evidence_a.fuzzy_hash_ssdeep,
        analysis_record.evidence_b.fuzzy_hash_ssdeep,
        analysis_record.evidence_a.fuzzy_hash_tlsh,
        analysis_record.evidence_b.fuzzy_hash_tlsh
    )

    return render_template(
        'results.html',
        analysis=analysis_record,
        pe_a=meta_a,
        pe_b=meta_b,
        eval_meta=eval_meta
    )
