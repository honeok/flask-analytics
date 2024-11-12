import os
from flask import Flask, request, jsonify, render_template
from config import Config
from models import db, Log
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

# 创建 Flask 应用
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# 定义日志清理任务
def clear_old_logs():
    """清理 3 天前的日志"""
    cutoff_date = datetime.utcnow() - timedelta(days=3)
    logs_to_delete = Log.query.filter(Log.timestamp < cutoff_date.strftime('%Y-%m-%d %H:%M:%S')).all()
    
    for log in logs_to_delete:
        db.session.delete(log)
    
    db.session.commit()
    print(f"清理了 {len(logs_to_delete)} 条过期日志")

# 定期任务设置
scheduler = BackgroundScheduler()
scheduler.add_job(
    func=clear_old_logs,
    trigger=IntervalTrigger(hours=24),  # 每天检查一次过期日志
    id='clear_old_logs',
    name='每 24 小时清理一次日志',
    replace_existing=True
)
scheduler.start()

# 创建数据库表
with app.app_context():
    db.create_all()

# 接收日志的 API
@app.route('/api/log', methods=['POST'])
def log():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid data'}), 400

    action = data.get("action")
    timestamp = data.get("timestamp", datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))
    country = data.get("country")
    os_info = data.get("os_info")
    cpu_arch = data.get("cpu_arch")

    new_log = Log(action=action, timestamp=timestamp, country=country, os_info=os_info, cpu_arch=cpu_arch)
    db.session.add(new_log)
    db.session.commit()

    return jsonify({'message': 'Log received'}), 201

# 展示日志的网页
@app.route('/logs', methods=['GET'])
def view_logs():
    logs = Log.query.all()
    return render_template('logs.html', logs=logs)

# 启动应用
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
