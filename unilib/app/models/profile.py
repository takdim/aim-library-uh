from datetime import datetime, timezone
from app import db


class ProfileSection(db.Model):
    __tablename__ = 'profile_sections'

    id = db.Column(db.Integer, primary_key=True)
    section_key = db.Column(db.String(50), unique=True, nullable=False)
    title = db.Column(db.String(150), nullable=False)
    title_en = db.Column(db.String(150), nullable=True)
    content = db.Column(db.Text, nullable=True)
    content_en = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(255), nullable=True)
    updated_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc),
                           onupdate=lambda: datetime.now(timezone.utc))

    VALID_KEYS = [
        'profil_perpustakaan',
        'visi_misi',
        'struktur_organisasi',
        'jam_pelayanan',
        'fasilitas',
    ]

    KEY_LABELS = {
        'profil_perpustakaan': 'Profil Perpustakaan',
        'visi_misi': 'Visi & Misi',
        'struktur_organisasi': 'Struktur Organisasi',
        'jam_pelayanan': 'Jam Pelayanan',
        'fasilitas': 'Fasilitas',
    }

    def __repr__(self):
        return f'<ProfileSection {self.section_key}>'
