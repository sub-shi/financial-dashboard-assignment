from database import db
from datetime import datetime

class Record(db.Model):
    __tablename__ = "records"

    id = db.Column(db.Integer, primary_key=True)

    amount = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(10), nullable=False)  # income / expense
    category = db.Column(db.String(50), nullable=False)

    date = db.Column(db.Date, default=datetime.utcnow)
    note = db.Column(db.String(255))

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "amount": self.amount,
            "type": self.type,
            "category": self.category,
            "date": str(self.date),
            "note": self.note,
            "user_id": self.user_id
        }