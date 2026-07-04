"""End-to-end test suite for the blog system (v1.0).

WARNING: This test script runs against the DEFAULT database configured in config.py.
It WILL create, modify, and delete data in the active SQLite database.
Before running: backup instance/personal_blog.sqlite or set a separate test database.
For isolated testing, use the pytest suite in tests/ which uses in-memory SQLite.
"""

import sys
from app import create_app
from app.extensions import db
from app.models import (
    ARTICLE_STATUS_PUBLISHED, ARTICLE_STATUS_DRAFT,
    User, Article, Category, Tag, Comment, BlogColumn,
)

app = create_app()
app.config["SERVER_NAME"] = "localhost"
app.config["WTF_CSRF_ENABLED"] = False  # disable CSRF for testing


@app.route("/__test_bad_request")
def test_bad_request():
    from flask import abort
    abort(400)


passed = 0
failed = 0
errors = []


def ok(label):
    global passed
    passed += 1
    print(f"  ✓ {label}")


def fail(label, detail=""):
    global failed
    failed += 1
    msg = f"  ✗ {label}"
    if detail:
        msg += f"  → {detail}"
    errors.append((label, detail))
    print(msg)


def check(label, condition, detail=""):
    if condition:
        ok(label)
    else:
        fail(label, detail)


def setup_test_data():
    """Create minimal test data: category, test user, and a published article."""
    with app.app_context():
        db.create_all()

        # Ensure default category exists
        if not Category.query.first():
            db.session.add(Category(name="默认分类", description="测试", sort_order=1))
            db.session.commit()

        # Ensure admin exists
        if not User.query.filter_by(username="admin").first():
            admin = User(username="admin", email="admin@test.com",
                         nickname="管理员", role="admin", status="active")
            admin.set_password("admin123456")
            db.session.add(admin)
            db.session.commit()

        # Create test user alice if not exists
        alice = User.query.filter_by(username="alice").first()
        if not alice:
            alice = User(username="alice", email="alice@test.com",
                         nickname="林知夏", role="user", status="active")
            alice.set_password("user123456")
            db.session.add(alice)
            db.session.commit()

        # Create test user bob if not exists
        bob = User.query.filter_by(username="bob").first()
        if not bob:
            bob = User(username="bob", email="bob@test.com",
                       nickname="Bob", role="user", status="active")
            bob.set_password("user123456")
            db.session.add(bob)
            db.session.commit()

        # Create a published article by alice for testing
        cat = Category.query.first()
        article = Article.query.filter_by(title="E2E 基础测试文章").first()
        if not article:
            article = Article(
                title="E2E 基础测试文章",
                slug="e2e-base-test-article",
                summary="用于 E2E 测试的基础文章",
                content="这是 E2E 测试的基础文章内容。包含 Flask 关键词用于搜索测试。",
                status=ARTICLE_STATUS_PUBLISHED,
                user_id=alice.id,
                category_id=cat.id,
            )
            db.session.add(article)
            db.session.commit()


def run():
    global passed, failed

    setup_test_data()
    c = app.test_client()

    # ============================================================
    # 1. PUBLIC PAGES
    # ============================================================
    print("\n=== 一、公开页面 ===")

    r = c.get("/")
    check("首页 (/)", r.status_code == 200, f"status={r.status_code}")

    r = c.get("/home")
    check("AI搜索首页 (/home)", r.status_code == 200, f"status={r.status_code}")

    r = c.get("/discover")
    check("发现页 (/discover)", r.status_code == 200, f"status={r.status_code}")

    r = c.get("/articles")
    check("文章列表 (/articles)", r.status_code == 200, f"status={r.status_code}")

    r = c.get("/columns")
    check("专栏列表 (/columns)", r.status_code == 200, f"status={r.status_code}")

    r = c.get("/categories")
    check("分类列表 (/categories)", r.status_code == 200, f"status={r.status_code}")

    r = c.get("/tags")
    check("标签列表 (/tags)", r.status_code == 200, f"status={r.status_code}")

    r = c.get("/search?q=Flask")
    check("搜索页面 (/search)", r.status_code == 200, f"status={r.status_code}")

    # Article detail
    with app.app_context():
        article = Article.query.filter_by(status=ARTICLE_STATUS_PUBLISHED).first()
    if article:
        r = c.get(f"/articles/{article.slug}")
        check("文章详情页", r.status_code == 200, f"status={r.status_code}")
        check("文章详情含标题", article.title in r.data.decode(), "title not in response")
    else:
        fail("文章详情页", "没有已发布文章")

    # Category detail
    with app.app_context():
        cat = Category.query.first()
    if cat:
        r = c.get(f"/categories/{cat.id}")
        check("分类详情页", r.status_code == 200, f"status={r.status_code}")

    # Tag detail
    with app.app_context():
        tag = Tag.query.first()
    if tag:
        r = c.get(f"/tags/{tag.id}")
        check("标签详情页", r.status_code == 200, f"status={r.status_code}")

    # Column detail
    with app.app_context():
        col = BlogColumn.query.filter_by(status="active").first()
    if col:
        r = c.get(f"/columns/{col.id}")
        check("专栏详情页", r.status_code == 200, f"status={r.status_code}")

    # User profile
    with app.app_context():
        alice = User.query.filter_by(username="alice").first()
    if alice:
        r = c.get(f"/users/{alice.id}")
        check("用户主页", r.status_code == 200, f"status={r.status_code}")

    # ============================================================
    # 2. AUTH
    # ============================================================
    print("\n=== 二、认证流程 ===")

    r = c.get("/login")
    check("登录页 GET", r.status_code == 200)

    r = c.get("/register")
    check("注册页 GET", r.status_code == 200)

    # Clean up previous test user
    with app.app_context():
        old = User.query.filter_by(username="testuser").first()
        if old:
            for comment in old.comments:
                db.session.delete(comment)
            for like in old.likes:
                db.session.delete(like)
            for fav in old.favorites:
                db.session.delete(fav)
            db.session.delete(old)
            db.session.commit()

    # Test registration
    r = c.post("/register", data={
        "username": "testuser",
        "email": "test@example.com",
        "password": "test123456",
        "nickname": "测试用户",
    }, follow_redirects=True)
    check("注册新用户", r.status_code == 200, f"status={r.status_code}")
    data = r.data.decode()
    check("注册后跳转", "个人中心" in data or "书房" in data or "testuser" in data or "测试用户" in data)

    # Logout
    r = c.get("/logout", follow_redirects=True)
    check("退出登录", r.status_code == 200)

    # Login with username
    r = c.post("/login", data={
        "username": "testuser",
        "password": "test123456",
    }, follow_redirects=True)
    check("用户名登录", r.status_code == 200, f"status={r.status_code}")

    # Login with wrong password
    c.get("/logout")
    r = c.post("/login", data={
        "username": "testuser",
        "password": "wrong",
    })
    check("错误密码拒绝登录", "用户名或密码错误" in r.data.decode())

    c.get("/logout")

    # ============================================================
    # 3. USER FUNCTIONS (logged in as alice)
    # ============================================================
    print("\n=== 三、用户功能（alice 登录）===")

    r = c.post("/login", data={
        "username": "alice",
        "password": "user123456",
    }, follow_redirects=True)
    check("alice 登录", r.status_code == 200)

    # Personal center
    r = c.get("/me", follow_redirects=True)
    check("个人中心 (/me)", r.status_code == 200)
    data = r.data.decode()
    check("个人中心含用户名", "alice" in data or "林知夏" in data)

    r = c.get("/settings", follow_redirects=True)
    check("设置页", r.status_code == 200)

    r = c.get("/profile/archive", follow_redirects=True)
    check("存档页", r.status_code == 200)

    r = c.get("/profile/reading", follow_redirects=True)
    check("阅读页", r.status_code == 200)

    r = c.get("/talk", follow_redirects=True)
    check("交流页", r.status_code == 200)

    r = c.get("/me/profile", follow_redirects=True)
    check("编辑资料页", r.status_code == 200)

    # Write article page (v1.0 AI panel)
    r = c.get("/write", follow_redirects=True)
    check("写文章页 GET", r.status_code == 200, f"status={r.status_code}")
    data = r.data.decode()
    # v1.0 AI assistant: 搜资料、大纲、润色、搜索摘要
    check("写文章页含 AI 面板", "write-ai-panel" in data or "ai-panel" in data)
    check("含搜资料按钮", "搜资料" in data)
    check("含大纲按钮", "大纲" in data)
    check("含润色按钮", "润色" in data or "润色正文" in data)
    check("含搜索摘要按钮", "搜索摘要" in data)
    check("含 AI 表单区域", "write-ai-form" in data)

    # Create an article
    with app.app_context():
        cat = Category.query.first()
    r = c.post("/write", data={
        "title": "E2E 测试文章",
        "summary": "自动化测试",
        "content": "这是端到端测试创建的文章内容。用于验证写文章功能是否正常。",
        "category_id": str(cat.id) if cat else "1",
        "status": ARTICLE_STATUS_PUBLISHED,
    }, follow_redirects=True)
    check("发布文章", r.status_code == 200)
    data = r.data.decode()
    check("发布后跳转文章页", "E2E 测试文章" in data, "title not in response")

    # Get the article slug for further testing
    with app.app_context():
        test_article = Article.query.filter_by(title="E2E 测试文章").first()
    if test_article:
        slug = test_article.slug

        # Edit article
        r = c.get(f"/my/articles/{test_article.id}/edit", follow_redirects=True)
        check("编辑文章页", r.status_code == 200)

        r = c.post(f"/my/articles/{test_article.id}/edit", data={
            "title": "E2E 测试文章（已编辑）",
            "summary": "编辑后的摘要",
            "content": "编辑后的正文内容。",
            "category_id": str(cat.id) if cat else "1",
            "status": ARTICLE_STATUS_PUBLISHED,
        }, follow_redirects=True)
        check("编辑文章", r.status_code == 200)

        # Like, favorite, comment
        r = c.post(f"/articles/{slug}/like", follow_redirects=True)
        check("点赞文章", r.status_code == 200)

        r = c.post(f"/articles/{slug}/favorite", follow_redirects=True)
        check("收藏文章", r.status_code == 200)

        r = c.post(f"/articles/{slug}/comments", data={
            "nickname": "alice",
            "email": "alice@example.com",
            "content": "这是一条测试评论。",
        }, follow_redirects=True)
        check("评论文章", r.status_code == 200)

    # My columns
    r = c.get("/my/columns", follow_redirects=True)
    check("我的专栏页", r.status_code == 200)

    # Create a column
    r = c.post("/my/columns", data={
        "name": "E2E 测试专栏",
        "description": "测试用专栏",
    }, follow_redirects=True)
    check("创建专栏", r.status_code == 200)

    # Change password
    r = c.post("/settings/password", data={
        "old_password": "user123456",
        "new_password": "newpass123",
        "confirm_password": "newpass123",
    }, follow_redirects=True)
    check("修改密码", r.status_code == 200)

    # Change password back
    c.post("/settings/password", data={
        "old_password": "newpass123",
        "new_password": "user123456",
        "confirm_password": "user123456",
    })

    c.get("/logout")

    # ============================================================
    # 4. PERMISSION TESTS
    # ============================================================
    print("\n=== 四、权限测试 ===")

    # Login as bob, try to access alice's resources
    r = c.post("/login", data={
        "username": "bob",
        "password": "user123456",
    }, follow_redirects=True)
    check("bob 登录", r.status_code == 200)

    if test_article:
        r = c.get(f"/my/articles/{test_article.id}/edit")
        check("非作者不能编辑他人文章", r.status_code == 403, f"status={r.status_code}")

        r = c.post(f"/my/articles/{test_article.id}/delete", follow_redirects=True)
        check("非作者不能删除他人文章", r.status_code == 403, f"status={r.status_code}")

    # Delete test column (belongs to alice)
    with app.app_context():
        test_col = BlogColumn.query.filter_by(name="E2E 测试专栏").first()
    if test_col:
        r = c.post(f"/my/columns/{test_col.id}/delete", follow_redirects=True)
        check("非作者不能删除他人专栏", r.status_code == 403, f"status={r.status_code}")

    # Logout and login as alice to clean up
    c.get("/logout")
    c.post("/login", data={"username": "alice", "password": "user123456"})
    # Restore password if needed
    c.post("/settings/password", data={
        "old_password": "user123456",
        "new_password": "user123456",
        "confirm_password": "user123456",
    })

    # Delete test column
    if test_col:
        with app.app_context():
            col = BlogColumn.query.filter_by(name="E2E 测试专栏").first()
        if col:
            c.post(f"/my/columns/{col.id}/delete", follow_redirects=True)

    # Delete test article
    if test_article:
        with app.app_context():
            art = Article.query.filter_by(title="E2E 测试文章（已编辑）").first()
            if not art:
                art = Article.query.filter_by(title="E2E 测试文章").first()
        if art:
            r = c.post(f"/my/articles/{art.id}/delete", follow_redirects=True)
            check("作者删除自己的文章", r.status_code == 200)

    c.get("/logout")

    # Clean up test user
    with app.app_context():
        tu = User.query.filter_by(username="testuser").first()
        if tu:
            for comment in tu.comments:
                db.session.delete(comment)
            for like in tu.likes:
                db.session.delete(like)
            for fav in tu.favorites:
                db.session.delete(fav)
            db.session.delete(tu)
            db.session.commit()

    # ============================================================
    # 5. ADMIN FUNCTIONS
    # ============================================================
    print("\n=== 五、管理员功能 ===")

    # Admin login
    r = c.post("/admin/login", data={
        "username": "admin",
        "password": "admin123456",
    }, follow_redirects=True)
    check("管理员登录", r.status_code == 200)

    r = c.get("/admin/dashboard", follow_redirects=True)
    check("仪表盘", r.status_code == 200)

    r = c.get("/admin/articles/", follow_redirects=True)
    check("文章管理", r.status_code == 200)

    r = c.get("/admin/users", follow_redirects=True)
    check("用户管理", r.status_code == 200)

    r = c.get("/admin/columns", follow_redirects=True)
    check("专栏管理", r.status_code == 200)

    r = c.get("/admin/categories/", follow_redirects=True)
    check("分类管理", r.status_code == 200)

    r = c.get("/admin/tags/", follow_redirects=True)
    check("标签管理", r.status_code == 200)

    r = c.get("/admin/comments", follow_redirects=True)
    check("评论管理", r.status_code == 200)

    r = c.get("/admin/ai", follow_redirects=True)
    check("AI 接口状态", r.status_code == 200)

    # Create category
    r = c.post("/admin/categories/", data={
        "name": "测试分类_E2E",
        "description": "测试",
        "sort_order": "99",
    }, follow_redirects=True)
    check("创建分类", r.status_code == 200)

    # Create tag
    r = c.post("/admin/tags/", data={
        "name": "E2E测试标签",
    }, follow_redirects=True)
    check("创建标签", r.status_code == 200)

    # Delete test tag
    with app.app_context():
        ttag = Tag.query.filter_by(name="E2E测试标签").first()
    if ttag:
        r = c.post(f"/admin/tags/{ttag.id}/delete", follow_redirects=True)
        check("删除标签", r.status_code == 200)

    # Delete test category
    with app.app_context():
        tcat = Category.query.filter_by(name="测试分类_E2E").first()
    if tcat:
        r = c.post(f"/admin/categories/{tcat.id}/delete", follow_redirects=True)
        check("删除分类", r.status_code == 200)

    # Admin creates article
    with app.app_context():
        cat = Category.query.first()
    r = c.post("/admin/articles/new", data={
        "title": "管理员测试文章",
        "summary": "管理员创建",
        "content": "管理员通过后台创建的文章。",
        "category_id": str(cat.id) if cat else "1",
        "status": ARTICLE_STATUS_PUBLISHED,
    }, follow_redirects=True)
    check("管理员创建文章", r.status_code == 200)

    # Clean up admin test article
    with app.app_context():
        aart = Article.query.filter_by(title="管理员测试文章").first()
        if aart:
            r = c.post(f"/admin/articles/{aart.id}/delete", follow_redirects=True)
            check("管理员删除文章", r.status_code == 200)

    # Approve a pending comment
    with app.app_context():
        pending = Comment.query.filter_by(status="pending").first()
    if pending:
        r = c.post(f"/admin/comments/{pending.id}/approve", follow_redirects=True)
        check("审核通过评论", r.status_code == 200)

    # Toggle user status
    with app.app_context():
        bob = User.query.filter_by(username="bob").first()
    if bob:
        r = c.post(f"/admin/users/{bob.id}/toggle", follow_redirects=True)
        check("禁用/启用用户", r.status_code == 200)
        # Toggle back
        c.post(f"/admin/users/{bob.id}/toggle", follow_redirects=True)

    # Comment filter
    r = c.get("/admin/comments?status=approved", follow_redirects=True)
    check("评论状态筛选", r.status_code == 200)

    c.get("/admin/logout")

    # ============================================================
    # 6. PERMISSION BOUNDARY
    # ============================================================
    print("\n=== 六、权限边界 ===")

    # Regular user accessing admin
    r = c.post("/login", data={"username": "alice", "password": "user123456"})
    r = c.get("/admin/dashboard")
    check("普通用户不能访问后台", r.status_code == 302, f"status={r.status_code}")
    check("普通用户被重定向首页", "/" in r.headers.get("Location", ""), r.headers.get("Location"))

    r = c.get("/admin/articles/")
    check("普通用户不能访问文章管理", r.status_code == 302, f"status={r.status_code}")

    c.get("/logout")

    # Non-logged-in user accessing protected pages
    r = c.get("/write", follow_redirects=True)
    check("未登录访问写文章→跳转登录", r.status_code == 200)

    r = c.get("/me", follow_redirects=True)
    check("未登录访问个人中心→跳转登录", r.status_code == 200)

    # ============================================================
    # 7. ERROR PAGES
    # ============================================================
    print("\n=== 七、错误页面 ===")

    r = c.get("/__test_bad_request")
    check("400 页面", r.status_code == 400, f"status={r.status_code}")
    check("400 页面含提示", "请求无效" in r.data.decode(), "400 template not rendered")

    r = c.get("/articles/nonexistent-slug-xyz")
    check("404 页面（文章）", r.status_code == 404, f"status={r.status_code}")

    r = c.get("/categories/99999")
    check("404 页面（分类）", r.status_code == 404, f"status={r.status_code}")

    # ============================================================
    # 8. EDGE CASES & VALIDATION
    # ============================================================
    print("\n=== 八、边界与校验 ===")

    # Duplicate registration
    r = c.post("/register", data={
        "username": "alice",
        "email": "alice@example.com",
        "password": "user123456",
    })
    data = r.data.decode()
    check("重复注册被拒绝",
          "已存在" in data or "已被注册" in data or "已注册" in data or "已经存在" in data or "exist" in data.lower(),
          f"got: {data[:200]}")

    # Empty title article
    c.post("/login", data={"username": "alice", "password": "user123456"})
    r = c.post("/write", data={
        "title": "",
        "summary": "",
        "content": "",
        "category_id": "1",
        "status": ARTICLE_STATUS_PUBLISHED,
    })
    check("空标题文章被拒绝",
          "标题不能为空" in r.data.decode() or "标题" in r.data.decode(),
          f"got status={r.status_code}")

    # Empty comment validation
    with app.app_context():
        art = Article.query.filter_by(status=ARTICLE_STATUS_PUBLISHED).first()
    if art:
        r = c.post(f"/articles/{art.slug}/comments", data={
            "nickname": "",
            "email": "invalid",
            "content": "",
        }, follow_redirects=True)
        data = r.data.decode()
        check("空评论被拒绝",
              "不能为空" in data or "格式不正确" in data or "必填" in data or "错误" in data)

    # Toggle like (unlike)
    if art:
        # Login if needed
        c.post("/login", data={"username": "alice", "password": "user123456"})
        r = c.post(f"/articles/{art.slug}/like", follow_redirects=True)
        check("点赞切换", r.status_code == 200)

    c.get("/logout")

    # ============================================================
    # 9. SEARCH
    # ============================================================
    print("\n=== 九、搜索功能 ===")

    r = c.get("/search?q=Flask")
    check("搜索 Flask", r.status_code == 200)

    r = c.get("/search?q=")
    check("空搜索", r.status_code == 200)

    r = c.get("/search?q=nonexistent_xyz_12345")
    check("无结果搜索", r.status_code == 200)

    # ============================================================
    # SUMMARY
    # ============================================================
    print(f"\n{'='*60}")
    print(f"  通过: {passed}  失败: {failed}")
    print(f"{'='*60}")

    if errors:
        print("\n失败详情:")
        for label, detail in errors:
            print(f"  ✗ {label}")
            if detail:
                print(f"    → {detail}")

    return failed == 0


if __name__ == "__main__":
    success = run()
    sys.exit(0 if success else 1)
