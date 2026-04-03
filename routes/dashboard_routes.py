from flask import Blueprint, jsonify
from sqlalchemy import func
from models.record import Record
from database import db
from utils.decorators import require_auth

dashboard_bp = Blueprint("dashboard", __name__)

#DASHBOARD SUMMARY
@dashboard_bp.route("/summary", methods=["GET"])
@require_auth(["admin", "analyst", "viewer"])
def get_summary():
    income = db.session.query(func.sum(Record.amount))\
        .filter(Record.type == "income").scalar() or 0                 #AGGREGATE INCOME

    expense = db.session.query(func.sum(Record.amount))\
        .filter(Record.type == "expense").scalar() or 0                 #AGGREGATE EXPENSE

    return jsonify({
        "total_income": income,
        "total_expense": expense,
        "net_balance": income - expense
    })

#CATEGORY BREAKDOWN
@dashboard_bp.route("/categories", methods=["GET"])
@require_auth(["admin", "analyst"])
def category_breakdown():
    data = db.session.query(
        Record.category,
        func.sum(Record.amount)
    ).group_by(Record.category).all()

    result = [
        {"category": c, "total": t}
        for c, t in data
    ]                                              #CATEGORY-WISE AGGREGATION

    return jsonify(result)

#MONTHLY TRENDS
@dashboard_bp.route("/trends", methods=["GET"])
@require_auth(["admin", "analyst"])
def monthly_trends():
    data = db.session.query(
        func.strftime("%Y-%m", Record.date),
        Record.type,
        func.sum(Record.amount)
    ).group_by(
        func.strftime("%Y-%m", Record.date),
        Record.type
    ).all()                                          #MONTHLY TREND AGGREGATION BY TYPE

    result = []

    for month, rtype, total in data:
        result.append({
            "month": month,
            "type": rtype,
            "total": total
        })

    return jsonify(result)

#RECENT ACTIVITY
@dashboard_bp.route("/recent", methods=["GET"])
@require_auth(["admin", "analyst", "viewer"])
def recent_activity():
    records = Record.query.order_by(Record.date.desc()).limit(5).all()

    return jsonify([r.to_dict() for r in records])