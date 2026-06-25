from app import db


class Statistic(db.Model):
    __tablename__ = 'statistics'

    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(100), nullable=False)
    value = db.Column(db.Integer, nullable=False, default=0)
    icon = db.Column(db.String(100), nullable=True)  # Material Symbol name
    sort_order = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<Statistic {self.label}: {self.value}>'
