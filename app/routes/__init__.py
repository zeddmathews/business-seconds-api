from flask import Blueprint
from .holiday import holiday_bp
from .business import business_bp

bp = Blueprint('api', __name__)
bp.register_blueprint(holiday_bp)
bp.register_blueprint(business_bp)

@bp.route('/', methods=['GET'])
def home():
    return {"message": "Landing page"}