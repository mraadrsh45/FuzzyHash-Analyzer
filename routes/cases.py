from flask import Blueprint, render_template, request, redirect, url_for, flash
from routes import login_required
from models import db
from models.case import Case
from services.case_service import CaseService

cases_bp = Blueprint('cases', __name__)

@cases_bp.route('/cases')
@login_required
def index():
    query = request.args.get('q', '').strip()
    status_filter = request.args.get('status', '').strip()

    cases_query = Case.query

    if query:
        cases_query = cases_query.filter(
            (Case.name.ilike(f"%{query}%")) |
            (Case.case_id.ilike(f"%{query}%")) |
            (Case.investigator.ilike(f"%{query}%"))
        )

    if status_filter and status_filter != 'All':
        cases_query = cases_query.filter_by(status=status_filter)

    all_cases = cases_query.order_by(Case.created_at.desc()).all()
    return render_template('cases.html', cases=all_cases, search_query=query, current_status=status_filter)

@cases_bp.route('/cases/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        investigator = request.form.get('investigator', '').strip() or 'Lead Investigator'
        status = request.form.get('status', 'Open')

        if not name:
            flash('Case Name is required.', 'danger')
            return render_template('create_case.html', auto_case_id=CaseService.generate_case_id())

        case_id = CaseService.generate_case_id()
        new_case = Case(
            case_id=case_id,
            name=name,
            description=description,
            investigator=investigator,
            status=status
        )
        db.session.add(new_case)
        db.session.commit()

        flash(f'Forensic Case {case_id} successfully created.', 'success')
        return redirect(url_for('cases.detail', case_id=new_case.case_id))

    auto_case_id = CaseService.generate_case_id()
    return render_template('create_case.html', auto_case_id=auto_case_id)

@cases_bp.route('/cases/<case_id>')
@login_required
def detail(case_id):
    case_obj = Case.query.filter_by(case_id=case_id).first_or_404()
    return render_template('case_detail.html', case=case_obj)
