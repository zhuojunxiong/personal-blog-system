from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from app import create_app
from app.extensions import db
from app.models import Category, User


def init_database():
    reset = "--reset" in sys.argv
    app = create_app()
    with app.app_context():
        if reset:
            db.drop_all()
        db.create_all()

        admin = User.query.filter_by(username="admin").first()
        if not admin:
            admin = User(
                username="admin",
                email="admin@example.com",
                nickname="系统管理员",
                role="admin",
                status="active",
                bio="平台管理员，负责内容和用户管理。",
            )
            admin.set_password("admin123456")
            db.session.add(admin)

        if not Category.query.filter_by(name="默认分类").first():
            db.session.add(
                Category(
                    name="默认分类",
                    description="系统默认分类，用于保存尚未细分的文章。",
                    sort_order=99,
                )
            )

        db.session.commit()
        print("数据库初始化完成。")
        print("默认管理员：admin / admin123456")
        print("首次运行后请及时修改默认密码。")


if __name__ == "__main__":
    init_database()
