"""
# Database models for Flask application
# This is an example implementation using SQLAlchemy

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

db = SQLAlchemy()

class BaseModel(db.Model):
    \"\"\"Base model with common fields.\"\"\"
    
    __abstract__ = True
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def to_dict(self):
        \"\"\"Convert model to dictionary.\"\"\"
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }

class User(BaseModel):
    \"\"\"User model.\"\"\"
    
    __tablename__ = 'users'
    
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    last_login = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<User {self.username}>'

class DeploymentLog(BaseModel):
    \"\"\"Deployment log model.\"\"\"
    
    __tablename__ = 'deployment_logs'
    
    version = db.Column(db.String(50), nullable=False)
    environment = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), nullable=False)  # success, failed, rollback
    deployed_by = db.Column(db.String(100))
    deployment_time = db.Column(db.DateTime, default=datetime.utcnow)
    rollback_version = db.Column(db.String(50))
    notes = db.Column(db.Text)
    
    def __repr__(self):
        return f'<DeploymentLog {self.version} - {self.status}>'
"""
