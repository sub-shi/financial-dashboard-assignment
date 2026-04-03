from flask import Blueprint, request, jsonify, g
from models.record import Record
from database import db
from utils.decorators import require_auth
from datetime import datetime
from utils.helpers import get_json_or_error

record_bp = Blueprint("records", __name__)

#CREATE RECORD
@record_bp.route("/", methods=["POST"])
@require_auth(["admin"])
def create_record():
    data, err, status = get_json_or_error()
    if err:
        return err, status

    # Validation
    if not data.get("amount") or data.get("amount") <= 0:
        return jsonify({"error": "Amount must be positive"}), 400            #POSITIVE NUMBER VALIDATION

    if data.get("type") not in ["income", "expense"]:
        return jsonify({"error": "Invalid type"}), 400             #TYPE VALIDATION

    record = Record(
        amount=data["amount"],
        type=data["type"],
        category=data.get("category", "general"),
        date=datetime.strptime(data.get("date"), "%Y-%m-%d") if data.get("date") else datetime.utcnow(),
        note=data.get("note"),
        user_id=g.user.id              #FROM JWT PAYLOAD
    )

    db.session.add(record)
    db.session.commit()

    return jsonify(record.to_dict()), 201


#GET RECORDS
@record_bp.route("/", methods=["GET"])
@require_auth(["admin", "analyst"])
def get_records():
    query = Record.query

    # Filters
    record_type = request.args.get("type")
    category = request.args.get("category")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    if record_type:
        query = query.filter_by(type=record_type)

    if category:
        query = query.filter_by(category=category)

    if start_date:
        query = query.filter(Record.date >= start_date)

    if end_date:
        query = query.filter(Record.date <= end_date)

    records = query.all()

    return jsonify([r.to_dict() for r in records])



#UPDATE RECORD
@record_bp.route("/<int:id>", methods=["PUT"])
@require_auth(["admin"])
def update_record(id):
    record = Record.query.get_or_404(id)
    data, err, status = get_json_or_error()
    if err:
        return err, status

    if "amount" in data:
        if data["amount"] <= 0:
            return jsonify({"error": "Invalid amount"}), 400
        record.amount = data["amount"]                                  #AMOUNT VALIDATION

    if "type" in data:
        if data["type"] not in ["income", "expense"]:
            return jsonify({"error": "Invalid type"}), 400
        record.type = data["type"]                                     #TYPE VALIDATION

    if "category" in data:
        record.category = data["category"]                             #CATEGORY UPDATE

    if "note" in data:
        record.note = data["note"]                                     #NOTE UPDATE
 
    db.session.commit()

    return jsonify(record.to_dict())


#DELETE RECORD
@record_bp.route("/<int:id>", methods=["DELETE"])
@require_auth(["admin"])
def delete_record(id):
    record = Record.query.get_or_404(id)

    db.session.delete(record)
    db.session.commit()

    return jsonify({"message": "Record deleted"})