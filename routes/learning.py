from flask import Blueprint, render_template
from routes import login_required

learning_bp = Blueprint('learning', __name__)

@learning_bp.route('/learning')
@login_required
def index():
    return render_template('learning.html')
