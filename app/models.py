from app import db
from datetime import datetime


# Create Tabel Pengeraman
class Pengeraman(db.Model):
    id = db.Column("pengeraman_id", db.Integer, primary_key=True)
    total_days = db.Column(db.Integer, default=0)
    day = db.Column(db.Integer, default=1)
    next_day = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "<Name {}>".format(self.name)


# Create table tools
class Tools(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    active = db.Column(db.Boolean, default=False)

    def __repr__(self) -> str:
        return "<Name {}>".format(self.name)


# Delete all record in Pengeraman
def delete_record_of_pengeraman() -> None:
    records = Pengeraman.query.all()
    for record in records:
        db.session.delete(record)
        db.session.commit()
