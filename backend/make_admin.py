"""
سكريبت لترقية مستخدم موجود لمشرف (Admin).

التشغيل:
    python make_admin.py your@email.com
"""
import sys
from app import create_app
from app.extensions import db
from app.models import User, UserRole


def run():
    if len(sys.argv) < 2:
        print("الاستخدام: python make_admin.py your@email.com")
        sys.exit(1)

    email = sys.argv[1].lower().strip()
    app = create_app()

    with app.app_context():
        user = User.query.filter_by(email=email).first()
        if not user:
            print(f"❌ لم يُعثر على مستخدم بالبريد: {email}")
            sys.exit(1)

        user.role = UserRole.ADMIN
        db.session.commit()
        print(f"✅ تمت ترقية '{user.name}' ({user.email}) إلى مشرف بنجاح!")


if __name__ == "__main__":
    run()
