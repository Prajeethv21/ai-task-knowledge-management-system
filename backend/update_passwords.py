from app.database.session import SessionLocal
from app.models.user import User
from app.utils.security import hash_password

db = SessionLocal()
admin = db.query(User).filter(User.email=='admin@example.com').first()
if admin:
    admin.password_hash = hash_password('admin123')
    db.commit()
    print('Updated admin password hash')
else:
    print('Admin not found')

user = db.query(User).filter(User.email=='user@example.com').first()
if user:
    user.password_hash = hash_password('user123')
    db.commit()
    print('Updated normal user password hash')
else:
    print('User not found')

db.close()
