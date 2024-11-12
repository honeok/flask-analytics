from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(50), nullable=True)
    os_info = db.Column(db.String(255), nullable=True)
    cpu_arch = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return f"<Log {self.action} at {self.timestamp}>"
