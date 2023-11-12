from flask import Blueprint, render_template


bp = Blueprint("dashboard_v1", __name__)


@bp.get('/', )
def dashboard():
    return render_template('index.html')
