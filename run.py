# 自动加载 .env 文件中的环境变量（如果存在）
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    # python-dotenv 未安装，跳过自动加载
    # 用户需手动设置环境变量：
    #   Windows: $env:AI_API_KEY="sk-xxx"
    #   Mac:     export AI_API_KEY="sk-xxx"
    pass

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5000)

# 启动方式：
#   cd /Users/lion/Desktop/系统开发版/personal-blog-system
#   .venv/bin/python run.py
#
# 停止：Ctrl + C
# 访问：http://127.0.0.1:5000
