from flask import Blueprint, request, jsonify
from datetime import datetime, time, timedelta
from app.config import DB_URL
from app.utils.holiday_utils import is_public_holiday
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

async def calculate_business_seconds(start: datetime, end: datetime, conn: asyncpg.Connection) -> int:
    BUSINESS_START = time(8, 0, 0)
    BUSINESS_END = time(17, 0, 0)

    total_elapsed = 0
    current = start

    while current < end:
        if current.weekday() >= 5:
            current += timedelta(days=(7 - current.weekday()))
            current = datetime.combine(current.date(), BUSINESS_START)
            continue

        if await is_public_holiday(conn, current.date()):
            current += timedelta(days=1)
            current = datetime.combine(current.date(), BUSINESS_START)
            continue
        
        start_of_day = datetime.combine(current.date(), BUSINESS_START)
        end_of_day = datetime.combine(current.date(), BUSINESS_END)

        effective_start = max(current, start_of_day)
        effective_end = min(end, end_of_day)

        if effective_start < effective_end:
            total_elapsed += (effective_end - effective_start).total_seconds()

        current = datetime.combine((current + timedelta(days=1)).date(), BUSINESS_START)

    return int(total_elapsed)
