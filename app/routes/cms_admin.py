from datetime import date
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
from app.extensions import db
from app.models import Notice, Event, GalleryAlbum, GalleryImage, Document, AdmissionApplication, ContactMessage
from app.utils.decorators import role_required
from app.utils.helpers import save_upload_file

cms_bp = Blueprint('cms', __name__)


# --- Notices Management ---
@cms_bp.route('/notices', methods=['GET', 'POST'])
@login_required
@role_required('Super Admin', 'Admin', 'Principal')
def notices():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        target_role = request.form.get('target_role', 'All')
        exp_date_str = request.form.get('expiry_date')

        attachment_file = request.files.get('attachment')
        attachment_path = save_upload_file(attachment_file, subfolder='documents')

        notice = Notice(
            title=title,
            content=content,
            attachment_path=attachment_path,
            target_role=target_role,
            is_published=True,
            expiry_date=date.fromisoformat(exp_date_str) if exp_date_str else None
        )
        db.session.add(notice)
        db.session.commit()
        flash('Notice published successfully.', 'success')
        return redirect(url_for('cms.notices'))

    all_notices = Notice.query.order_by(Notice.created_at.desc()).all()
    return render_template('dashboard/content/notices.html', notices=all_notices)


@cms_bp.route('/notices/<int:id>/delete', methods=['POST'])
@login_required
@role_required('Super Admin', 'Admin')
def delete_notice(id):
    notice = Notice.query.get_or_404(id)
    db.session.delete(notice)
    db.session.commit()
    flash('Notice deleted.', 'success')
    return redirect(url_for('cms.notices'))


# --- Events Management ---
@cms_bp.route('/events', methods=['GET', 'POST'])
@login_required
@role_required('Super Admin', 'Admin', 'Principal')
def events():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        event_date_str = request.form.get('event_date')
        event_time = request.form.get('event_time', '09:00 AM')
        location = request.form.get('location', 'Main Campus')
        reg_link = request.form.get('registration_link', '')

        img_file = request.files.get('image')
        img_path = save_upload_file(img_file, subfolder='photos') or 'default_event.jpg'

        ev = Event(
            title=title,
            description=description,
            event_date=date.fromisoformat(event_date_str),
            event_time=event_time,
            location=location,
            image_path=img_path,
            registration_link=reg_link,
            is_upcoming=True
        )
        db.session.add(ev)
        db.session.commit()
        flash('Event created successfully.', 'success')
        return redirect(url_for('cms.events'))

    all_events = Event.query.order_by(Event.event_date.asc()).all()
    return render_template('dashboard/content/events.html', events=all_events)


# --- Gallery Management ---
@cms_bp.route('/gallery', methods=['GET', 'POST'])
@login_required
@role_required('Super Admin', 'Admin')
def gallery():
    if request.method == 'POST':
        album_id = request.form.get('album_id', type=int)
        title = request.form.get('album_title')

        if title and not album_id:
            # Create new album
            album = GalleryAlbum(title=title, description=request.form.get('description', ''))
            db.session.add(album)
            db.session.commit()
            album_id = album.id

        files = request.files.getlist('images')
        for f in files:
            p = save_upload_file(f, subfolder='photos')
            if p:
                img = GalleryImage(album_id=album_id, image_path=p, caption=title)
                db.session.add(img)

        db.session.commit()
        flash('Gallery updated successfully.', 'success')
        return redirect(url_for('cms.gallery'))

    albums = GalleryAlbum.query.all()
    return render_template('dashboard/content/gallery.html', albums=albums)


# --- Documents Center Management ---
@cms_bp.route('/documents', methods=['GET', 'POST'])
@login_required
@role_required('Super Admin', 'Admin')
def documents():
    if request.method == 'POST':
        title = request.form.get('title')
        category = request.form.get('category', 'General')
        desc = request.form.get('description', '')

        f = request.files.get('document')
        doc_path = save_upload_file(f, subfolder='documents')

        if doc_path:
            doc = Document(title=title, category=category, file_path=doc_path, description=desc)
            db.session.add(doc)
            db.session.commit()
            flash('Document uploaded.', 'success')
        else:
            flash('Please select a valid document file to upload.', 'danger')

        return redirect(url_for('cms.documents'))

    docs = Document.query.order_by(Document.uploaded_at.desc()).all()
    return render_template('dashboard/content/documents.html', documents=docs)


# --- Admissions Review ---
@cms_bp.route('/admissions')
@login_required
@role_required('Super Admin', 'Admin', 'Principal')
def admissions():
    status = request.args.get('status', '')
    query = AdmissionApplication.query
    if status:
        query = query.filter_by(status=status)
    applications = query.order_by(AdmissionApplication.created_at.desc()).all()
    return render_template('dashboard/admissions/list.html', applications=applications, selected_status=status)


@cms_bp.route('/admissions/<int:id>/status', methods=['POST'])
@login_required
@role_required('Super Admin', 'Admin', 'Principal')
def update_admission_status(id):
    app_obj = AdmissionApplication.query.get_or_404(id)
    new_status = request.form.get('status')
    notes = request.form.get('admin_notes', '')

    if new_status:
        app_obj.status = new_status
        app_obj.admin_notes = notes
        db.session.commit()
        flash(f'Application {app_obj.application_number} updated to {new_status}.', 'success')

    return redirect(url_for('cms.admissions'))


# --- Contact Inbox Management ---
@cms_bp.route('/messages')
@login_required
@role_required('Super Admin', 'Admin', 'Principal')
def messages():
    all_msgs = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    return render_template('dashboard/messages/list.html', messages=all_msgs)


@cms_bp.route('/messages/<int:id>/read', methods=['POST'])
@login_required
def mark_message_read(id):
    msg = ContactMessage.query.get_or_404(id)
    msg.is_read = True
    db.session.commit()
    flash('Message marked as read.', 'info')
    return redirect(url_for('cms.messages'))
