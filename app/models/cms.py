from datetime import datetime
from app.extensions import db


class GalleryAlbum(db.Model):
    __tablename__ = 'gallery_albums'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    cover_image = db.Column(db.String(255), default='default_album.jpg')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    images = db.relationship('GalleryImage', backref='album_obj', lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<GalleryAlbum {self.title}>'


class GalleryImage(db.Model):
    __tablename__ = 'gallery_images'

    id = db.Column(db.Integer, primary_key=True)
    album_id = db.Column(db.Integer, db.ForeignKey('gallery_albums.id'), nullable=False)
    image_path = db.Column(db.String(255), nullable=False)
    caption = db.Column(db.String(200))
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<GalleryImage ID:{self.id} Album:{self.album_id}>'


class Document(db.Model):
    __tablename__ = 'documents'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(50), default='General')  # Prospectus, Syllabus, Application Forms, Circulars
    file_path = db.Column(db.String(255), nullable=False)
    file_size = db.Column(db.String(50), default='1 MB')
    description = db.Column(db.Text)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Document {self.title} ({self.category})>'


class SchoolSetting(db.Model):
    __tablename__ = 'school_settings'

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50), unique=True, nullable=False)
    value = db.Column(db.Text)
    label = db.Column(db.String(100))

    def __repr__(self):
        return f'<SchoolSetting {self.key} = {self.value}>'
