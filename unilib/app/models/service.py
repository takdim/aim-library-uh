from app import db


class Service(db.Model):
    __tablename__ = 'services'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    title_en = db.Column(db.String(150), nullable=True)
    description = db.Column(db.Text, nullable=True)
    description_en = db.Column(db.Text, nullable=True)
    icon = db.Column(db.String(100), nullable=True)  # Material Symbol name
    link_url = db.Column(db.String(255), nullable=True)
    sort_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<Service {self.title}>'
