from flask import Blueprint, jsonify, request
from datetime import datetime, time, timedelta

bp = Blueprint('api', __name__)

@bp.route('/', methods=['GET'])
def home():
    return jsonify(message="Landing page");    

@bp.route('/business_seconds', methods=['GET'])
def business_seconds():
    start_time_str = request.args.get('start_time')
    end_time_str = request.args.get('end_time')

    if not start_time_str and not end_time_str:
        return jsonify(error="Missing 'start_time' and 'end_time' parameter"), 400
    if not start_time_str:
        return jsonify(error="Missing 'start_time' parameter"), 400
    if not end_time_str:
        return jsonify(error="Missing 'end_time' parameter"), 400
    try:
        start_time = datetime.fromisoformat(start_time_str)
        end_time = datetime.fromisoformat(end_time_str)
    except ValueError:
        return jsonify(error="Invalid datetime format, must be ISO-8601"), 400
    
    if start_time >= end_time:
        return jsonify(error="'start_time' must be before 'end_time'"), 400
    
    try:
        total_seconds = calculate_business_seconds(start_time, end_time)
    except Exception as e:
        return jsonify(error=str(e)), 500

    return jsonify(total_business_seconds=total_seconds)

from datetime import datetime, time, timedelta

def calculate_business_seconds(start: datetime, end: datetime) -> int:
    if not isinstance(start, datetime):
        raise TypeError("Start has incorrect format. Please use ISO-8601")
    if not isinstance(end, datetime):
        raise TypeError("End has incorrect format. Please use ISO-8601")
    if start >= end:
        raise ValueError("'Start' must be before 'End'")
    
    BUSINESS_START = time(8, 0, 0)
    BUSINESS_END = time(17, 0, 0)
    
    total_elapsed = 0
    current = start

    while current < end:
        if current.weekday() >= 5:
            new_week = 7 - current.weekday()
            next_monday = current + timedelta(days=new_week)
            current = datetime.combine(next_monday.date(), BUSINESS_START)
            continue

        day_business_start = datetime.combine(current.date(), BUSINESS_START)
        day_business_end = datetime.combine(current.date(), BUSINESS_END)

        effective_start = max(current, day_business_start)
        effective_end = min(end, day_business_end)

        if effective_start < effective_end:
            seconds = (effective_end - effective_start).total_seconds()
            total_elapsed += seconds

        next_day = current + timedelta(days=1)
        current = datetime.combine(next_day.date(), BUSINESS_START)

    return int(total_elapsed)