from flask import Blueprint

ref_bp = Blueprint('ref', __name__)

from app.ref import routes
