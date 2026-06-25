from datetime import datetime, timezone
from app import db


class NavLink(db.Model):
    __tablename__ = 'nav_links'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Enum('repository', 'ejournal'), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    logo_url = db.Column(db.String(255), nullable=True)
    url = db.Column(db.String(255), nullable=False)
    sort_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f'<NavLink {self.type}: {self.name}>'
