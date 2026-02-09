from app import app, db, User, bcrypt

# Masuk ke konteks aplikasi
with app.app_context():
    # 1. Buat semua tabel (Tables) di MySQL
    db.create_all()
    print("Tabel berhasil dibuat di Database!")

    # 2. Cek apakah admin sudah ada?
    if not User.query.filter_by(username='admin').first():
        # Jika belum ada, buat user admin baru
        hashed_password = bcrypt.generate_password_hash('password123').decode('utf-8')
        admin = User(username='admin', password=hashed_password)
        
        db.session.add(admin)
        db.session.commit()
        print("User 'admin' dengan password 'password123' berhasil dibuat!")
    else:
        print("User admin sudah ada.")