from datetime import datetime, timezone
import re
from app import db


def slugify(text):
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    text = re.sub(r'^-+|-+$', '', text)
    return text


class News(db.Model):
    __tablename__ = 'news'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    title_en = db.Column(db.String(255), nullable=True)
    slug = db.Column(db.String(255), unique=True, nullable=False)
    category = db.Column(db.String(50), nullable=False, default='Umum')
    cover_image = db.Column(db.String(255), nullable=True)
    excerpt = db.Column(db.Text, nullable=True)
    excerpt_en = db.Column(db.Text, nullable=True)
    content = db.Column(db.Text, nullable=False)
    content_en = db.Column(db.Text, nullable=True)
    status = db.Column(db.Enum('draft', 'published'), nullable=False, default='draft')
    published_at = db.Column(db.DateTime, nullable=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc),
                           onupdate=lambda: datetime.now(timezone.utc))

    def generate_slug(self):
        base_slug = slugify(self.title)
        slug = base_slug
        counter = 1
        while News.query.filter_by(slug=slug).filter(News.id != self.id).first():
            slug = f'{base_slug}-{counter}'
            counter += 1
        self.slug = slug

    def publish(self):
        self.status = 'published'
        if not self.published_at:
            self.published_at = datetime.now(timezone.utc)

    def unpublish(self):
        self.status = 'draft'

    @property
    def cover_url(self):
        if self.cover_image:
            return f'/static/uploads/{self.cover_image}'
        return None

    def __repr__(self):
        return f'<News {self.slug}>'
