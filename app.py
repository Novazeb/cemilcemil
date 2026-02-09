from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt

app = Flask(__name__)

# --- KONFIGURASI ---
app.config['SECRET_KEY'] = 'rahasia_super_aman' # Ganti terserah kamu
# Koneksi ke XAMPP MySQL (user: root, pass: kosong, db: portfolio_db)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/portfolio_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# --- DATABASE MODEL ---
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_link = db.Column(db.String(500))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- ROUTING (HALAMAN) ---


@app.route('/')
def home():
    projects = Project.query.all() # Ambil semua project dari DB
    return render_template('home.html', projects=projects)

# Halaman Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Jika sudah login, lempar ke dashboard
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        # Cek user ada DAN password cocok
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Login gagal. Periksa username atau password.', 'danger')
            
    return render_template('login.html')

# Halaman Dashboard (Hanya Admin)
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if request.method == 'POST':
        # Ambil data dari form
        title = request.form.get('title')
        description = request.form.get('description')
        image_link = request.form.get('image_link')
        
        # Simpan ke Database
        new_project = Project(title=title, description=description, image_link=image_link)
        db.session.add(new_project)
        db.session.commit()
        flash('Project berhasil ditambahkan!', 'success')
        return redirect(url_for('dashboard'))

    # Ambil semua data project dari database untuk ditampilkan
    all_projects = Project.query.all()
    return render_template('dashboard.html', projects=all_projects)

# Route untuk Menghapus Project
@app.route('/delete_project/<int:id>')
@login_required
def delete_project(id):
    project = Project.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    flash('Project berhasil dihapus!', 'warning')
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)