import os
import time
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from PIL import Image
from models import db, User, Post, Comment
from config import Config
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'

# Create upload directory
Path(app.config['UPLOAD_FOLDER']).mkdir(parents=True, exist_ok=True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.template_filter('nl2br')
def nl2br_filter(value):
    """Convert newlines to <br> tags"""
    if value:
        return value.replace('\n', '<br>')
    return value

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def save_image(image_file):
    """Save and resize uploaded image"""
    if image_file and allowed_file(image_file.filename):
        filename = secure_filename(image_file.filename)
        timestamp = str(int(time.time() * 1000))
        name, ext = os.path.splitext(filename)
        filename = f"{name}_{timestamp}{ext}"
        
        filepath = Path(app.config['UPLOAD_FOLDER']) / filename
        
        img = Image.open(image_file)
        try:
            resample = Image.Resampling.LANCZOS
        except AttributeError:
            resample = Image.LANCZOS
        img.thumbnail(app.config['IMAGE_MAX_SIZE'], resample)
        img.save(filepath)
        
        return f"uploads/{filename}"
    return None

@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    posts = Post.query.order_by(Post.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    return render_template('index.html', posts=posts)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if not username or not email or not password:
            flash('Please fill in all fields.', 'error')
            return redirect(url_for('register'))
        
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return redirect(url_for('register'))
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'error')
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists.', 'error')
            return redirect(url_for('register'))
        
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = bool(request.form.get('remember'))
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user, remember=remember)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Invalid username or password.', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))

@app.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        ingredients = request.form.get('ingredients') 
        cuisine = request.form.get('cuisine')
        cooking_time = request.form.get('cooking_time')
        image_file = request.files.get('image')

        # Validate required fields
        if not title or not content:
            flash('Recipe title and description are required.', 'error')
            return redirect(url_for('create_post'))

        # Save image if provided
        image_path = save_image(image_file) if image_file else None

        # Create Post instance
        post = Post(
            title=title,
            content=content,
            ingredients=ingredients,
            image_path=image_path,
            cuisine=cuisine,
            cooking_time=cooking_time,
            user_id=current_user.id
        )
        db.session.add(post)
        db.session.commit()

        flash('Recipe posted successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('create_post.html')


@app.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)

    # Check permission
    if post.user_id != current_user.id:
        flash('You do not have permission to edit this post.', 'error')
        return redirect(url_for('post_detail', post_id=post_id))

    if request.method == 'POST':
        post.title = request.form.get('title')
        post.content = request.form.get('content')
        post.ingredients = request.form.get('ingredients')
        post.cuisine = request.form.get('cuisine')
        post.cooking_time = request.form.get('cooking_time')
        image_file = request.files.get('image')

        # Replace image if a new one is uploaded
        if image_file:
            if post.image_path:
                old_path = Path('static') / post.image_path
                if old_path.exists():
                    old_path.unlink()

            image_path = save_image(image_file)
            if image_path:
                post.image_path = image_path

        db.session.commit()
        flash('Recipe updated successfully!', 'success')
        return redirect(url_for('post_detail', post_id=post_id))

    return render_template('edit_post.html', post=post)


@app.route('/post/<int:post_id>')
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post_detail.html', post=post)

    post = Post.query.get_or_404(post_id)
    
    if post.user_id != current_user.id:
        flash('You do not have permission to edit this post.', 'error')
        return redirect(url_for('post_detail', post_id=post_id))
    
    if request.method == 'POST':
        post.title = request.form.get('title')
        post.content = request.form.get('content')
        post.cuisine = request.form.get('cuisine')
        cooking_date_str = request.form.get('cooking_date')
        image_file = request.files.get('image')
        
        if cooking_date_str:
            try:
                post.cooking_date = datetime.strptime(cooking_date_str, '%Y-%m-%d').date()
            except ValueError:
                pass
        else:
            post.cooking_date = None
        
        if image_file:
            if post.image_path:
                old_path = Path('static') / post.image_path
                if old_path.exists():
                    old_path.unlink()
            
            image_path = save_image(image_file)
            if image_path:
                post.image_path = image_path
        
        db.session.commit()
        flash('Recipe updated successfully!', 'success')
        return redirect(url_for('post_detail', post_id=post_id))
    
    return render_template('edit_post.html', post=post)

@app.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    
    if post.user_id != current_user.id:
        flash('You do not have permission to delete this post.', 'error')
        return redirect(url_for('post_detail', post_id=post_id))
    
    if post.image_path:
        image_path = Path('static') / post.image_path
        if image_path.exists():
            image_path.unlink()
    
    db.session.delete(post)
    db.session.commit()
    flash('Recipe deleted successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/post/<int:post_id>/comment', methods=['POST'])
@login_required
def add_comment(post_id):
    post = Post.query.get_or_404(post_id)
    content = request.form.get('content')
    
    if not content:
        flash('Comment cannot be empty.', 'error')
        return redirect(url_for('post_detail', post_id=post_id))
    
    comment = Comment(content=content, user_id=current_user.id, post_id=post_id)
    db.session.add(comment)
    db.session.commit()
    
    flash('Comment added successfully!', 'success')
    return redirect(url_for('post_detail', post_id=post_id))

@app.route('/comment/<int:comment_id>/delete', methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    
    if comment.user_id != current_user.id:
        flash('You do not have permission to delete this comment.', 'error')
        return redirect(url_for('post_detail', post_id=comment.post_id))
    
    post_id = comment.post_id
    db.session.delete(comment)
    db.session.commit()
    flash('Comment deleted successfully!', 'success')
    return redirect(url_for('post_detail', post_id=post_id))

@app.route('/search')
def search():
    query = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    if query:
        posts = Post.query.filter(
            db.or_(
                Post.title.contains(query),
                Post.content.contains(query),
                Post.cuisine.contains(query)
            )
        ).order_by(Post.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    else:
        posts = Post.query.order_by(Post.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('search.html', posts=posts, query=query)

@app.route('/profile/<username>')
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    per_page = 10
    posts = Post.query.filter_by(user_id=user.id).order_by(Post.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    return render_template('profile.html', user=user, posts=posts)

@app.route('/toggle_dark_mode', methods=['POST'])
@login_required
def toggle_dark_mode():
    current_user.dark_mode = not current_user.dark_mode
    db.session.commit()
    return jsonify({'dark_mode': current_user.dark_mode})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
