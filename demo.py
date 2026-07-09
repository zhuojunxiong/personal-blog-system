"""
演示模式 — 多端口同时启动，一个端口 = 一个身份。

用法：
    python demo.py            # 启动全部 4 个端口
    python demo.py --stop     # 停止全部实例

浏览器切换：
    端口 5000 → 游客视角（公开浏览、搜索、文章详情）
    端口 5001 → alice 已登录（个人中心、写文章、点赞收藏评论）
    端口 5002 → admin 已登录（后台仪表盘、用户管理、内容审核）
    端口 5003 → bob 已登录（权限演示：编辑他人文章 → 403）

演示路径：
    1. 打开 4 个浏览器 tab，分别访问 4 个端口
    2. 切换 tab 即可展示不同身份下的全部功能
    3. 无需反复登录退出
"""

import subprocess
import sys
import time
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PYTHON = os.path.join(BASE_DIR, ".venv", "bin", "python")

INSTANCES = [
    {"port": 5000, "user": "",          "label": "游客 — 首次进入页"},
    {"port": 5001, "user": "alice",     "label": "alice — AI 写作辅助"},
    {"port": 5002, "user": "admin",     "label": "admin — 后台治理"},
    {"port": 5003, "user": "bob",       "label": "bob — 权限演示 403"},
    {"port": 5004, "user": "",          "label": "游客 — 柳无心个人主页"},
    {"port": 5005, "user": "alice",     "label": "alice — AI 阅读助手"},
    {"port": 5006, "user": "",          "label": "游客 — AI 智能搜索"},
    {"port": 5007, "user": "admin",     "label": "admin — AI 审核状态"},
    {"port": 5008, "user": "alice",     "label": "alice — AI 写作评分 72分"},
]

OPEN_PAGES = {
    5000: "/?landing=1",
    5001: "/write",
    5002: "/admin/dashboard",
    5003: "/write",
    5004: "/users/2",
    5005: "/articles/第一次创业最容易犯的五个错误",
    5006: "/search?q=学习Flask",
    5007: "/admin/ai",
    5008: "/my/articles/1/edit",
}


def start():
    """启动所有演示实例"""
    print("\n  演示模式启动中...\n")
    processes = []

    for cfg in INSTANCES:
        env = os.environ.copy()
        if cfg["user"]:
            env["DEMO_AUTO_LOGIN"] = cfg["user"]
        else:
            env.pop("DEMO_AUTO_LOGIN", None)

        # 确保 AI 功能可用（如果配置了 Key）
        # env["AI_ENABLED"] = "1"

        cmd = [
            PYTHON, "-c",
            f"""
import os
os.environ["DEMO_AUTO_LOGIN"] = {repr(cfg['user'])}
from app import create_app
app = create_app()
app.config["SESSION_COOKIE_NAME"] = f"session_{cfg['port']}"
app.config["SESSION_COOKIE_PATH"] = "/"
print(f"\\n  http://127.0.0.1:{cfg['port']}  →  {cfg['label']}")
app.run(debug=False, port={cfg['port']}, host="127.0.0.1")
"""
        ]

        proc = subprocess.Popen(
            cmd,
            env=env,
            cwd=BASE_DIR,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        processes.append((cfg, proc))
        time.sleep(0.8)

    print(f"\n  {'='*60}")
    print(f"  全部 {len(INSTANCES)} 个端口已启动，浏览器即将自动打开...\n")
    for cfg in INSTANCES:
        page = OPEN_PAGES.get(cfg["port"], "/")
        url = f"http://127.0.0.1:{cfg['port']}{page}"
        print(f"    {url}  →  {cfg['label']}")
        # 自动打开浏览器 tab
        subprocess.run(["open", url], check=False)
        time.sleep(0.4)
    print(f"\n  停止演示：python demo.py --stop")
    print(f"  {'='*60}\n")

    try:
        for _, proc in processes:
            proc.wait()
    except KeyboardInterrupt:
        print("\n  正在停止...")
        for _, proc in processes:
            proc.terminate()
        print("  已停止全部实例。")


def stop():
    """停止所有演示实例"""
    import signal
    killed = 0
    for cfg in INSTANCES:
        port = cfg["port"]
        try:
            result = subprocess.run(
                ["lsof", "-ti", f"tcp:{port}"],
                capture_output=True, text=True
            )
            for pid in result.stdout.strip().split("\n"):
                if pid:
                    os.kill(int(pid), signal.SIGTERM)
                    killed += 1
        except Exception:
            pass

    # 也尝试通过进程名杀
    try:
        subprocess.run(
            ["pkill", "-f", "DEMO_AUTO_LOGIN"],
            capture_output=True
        )
    except Exception:
        pass

    print(f"  已停止 {killed} 个演示实例。")


if __name__ == "__main__":
    if "--stop" in sys.argv:
        stop()
    else:
        start()
