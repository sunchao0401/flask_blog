import os
from flask_blog import create_app

# 获取环境配置
config_name = os.environ.get('FLASK_ENV', 'production')
app = create_app(config_name)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
