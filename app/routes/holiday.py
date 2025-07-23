from flask import Blueprint, request, jsonify
from datetime import datetime
from app.utils.holiday_utils import is_public_holiday
import asyncpg
from app.config import DB_URL

holiday_bp = Blueprint('holiday', __name__)

@holiday_bp.route('/is-holiday')
async def check_holiday():
    date_str = request.args.get("date")
    if not date_str:
        return jsonify({"error": "Missing 'date' query param"}), 400

    try:
        input_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

    conn = await asyncpg.connect(DB_URL)
    try:
        is_holiday = await is_public_holiday(conn, input_date)
        return jsonify({"date": date_str, "is_holiday": is_holiday})
    finally:
        await conn.close()