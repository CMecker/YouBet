from flask import render_template
from app import app, db
from app.errors import err_bp

@app.errorhandler(404)
def not_found_error(error):
    return render_template('err/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('err/500.html'), 500
