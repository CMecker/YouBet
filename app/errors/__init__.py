from flask import Blueprint

err_bp = Blueprint('errors', __name__)

from app.errors import handlers
