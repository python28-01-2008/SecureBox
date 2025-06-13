from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from .. import db
from ..forms import ItemForm
from ..models import Item

bp = Blueprint('dashboard', __name__)

@bp.route('/')
@login_required
def dashboard():
    fernet = current_user.get_fernet()
    items = Item.query.filter_by(owner_id=current_user.id).all()
    decrypted_items = [
        {'id': i.id, 'title': i.title, 'content': fernet.decrypt(i.encrypted_content.encode()).decode()}
        for i in items
    ]
    return render_template('dashboard.html', items=decrypted_items)

@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = ItemForm()
    if form.validate_on_submit():
        encrypted = current_user.get_fernet().encrypt(form.content.data.encode()).decode()
        item = Item(owner_id=current_user.id, title=form.title.data, encrypted_content=encrypted)
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('dashboard.dashboard'))
    return render_template('add.html', form=form)

@bp.route('/delete/<int:item_id>')
@login_required
def delete(item_id):
    item = Item.query.get_or_404(item_id)
    if item.owner_id != current_user.id:
        flash('Unauthorized', 'danger')
        return redirect(url_for('dashboard.dashboard'))
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('dashboard.dashboard'))
