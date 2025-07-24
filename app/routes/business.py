from flask import Blueprint, request, jsonify
from datetime import datetime
from app.config import DB_URL
from app.utils.time_utils import calculate_business_seconds
import asyncpg

business_bp = Blueprint('business', __name__)

@business_bp.route('/business_seconds', methods=['GET'])
async def business_seconds():
    start_time_str = request.args.get('start_time')
    end_time_str = request.args.get('end_time')

    if not start_time_str or not end_time_str:
        return jsonify(error="Missing 'start_time' or 'end_time' parameter"), 400

    try:
        start_time = datetime.fromisoformat(start_time_str)
        end_time = datetime.fromisoformat(end_time_str)
    except ValueError:
        return jsonify(error="Invalid datetime format, must be ISO-8601"), 400

    if start_time >= end_time:
        return jsonify(error="'start_time' must be before 'end_time'"), 400

    conn = await asyncpg.connect(DB_URL)
    try:
        total_seconds = await calculate_business_seconds(start_time, end_time, conn)
    except Exception as e:
        return jsonify(error=str(e)), 500
    finally:
        await conn.close()

    return jsonify(total_business_seconds=total_seconds)