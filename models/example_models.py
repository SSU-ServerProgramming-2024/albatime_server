from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    isemployer = db.Column(db.Boolean, nullable=False)
    age = db.Column(db.Integer)
    boss = db.relationship('Boss', backref='user', uselist=False)

class Boss(db.Model):
    __tablename__ = 'boss'
    bossno = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    company = db.relationship('Company', backref='boss', uselist=False)

class Company(db.Model):
    __tablename__ = 'company'
    comno = db.Column(db.BigInteger, primary_key=True)
    type = db.Column(db.BigInteger, nullable=False)
    bossno = db.Column(db.BigInteger, db.ForeignKey('boss.bossno'), nullable=False)
    com_name = db.Column(db.String(255), nullable=False)
    com_loc = db.Column(db.String(255), nullable=False)

class WorkInformation(db.Model):
    __tablename__ = 'work_information'
    work_key = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    bossno = db.Column(db.BigInteger, db.ForeignKey('boss.bossno'), nullable=False, default=None)  # boss 테이블과의 관계를 가정
    reviewno = db.Column(db.BigInteger, db.ForeignKey('employee_review.reviewno'), nullable=True, default=None)
    startday = db.Column(db.Date, nullable=False)
    money = db.Column(db.Integer, nullable=False)
    comno = db.Column(db.BigInteger, db.ForeignKey('company.comno'), nullable=True, default=None)  # company 테이블과의 관계를 가정
    albano = db.Column(db.BigInteger, db.ForeignKey('alba.albano'), nullable=True)
    absent = db.Column(db.Integer, nullable=True, default=None)
    late = db.Column(db.Integer, nullable=True,default=None)
    alba_relation = db.relationship('Alba', backref=db.backref('work_info', lazy=True))
    
class EmployeeReview(db.Model):
    __tablename__ = 'employee_review'
    reviewno = db.Column(db.BigInteger, primary_key=True)
    content = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.user_id'), nullable=False)
    comno = db.Column(db.BigInteger, db.ForeignKey('company.comno'), nullable=False)
    
class TimeBlock(db.Model):
    __tablename__ = 'timeblock'
    timeblock_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    start_time = db.Column(db.Integer, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    albano = db.Column(db.BigInteger, db.ForeignKey('alba.albano'), nullable=False)
    bossno = db.Column(db.BigInteger, db.ForeignKey('boss.bossno'), nullable=True)    
    
class Alba(db.Model):
    __tablename__ = 'alba'
    albano = db.Column(db.BigInteger, primary_key=True)
    age = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    bossno = db.Column(db.Integer, nullable=False)
    
class Timetable(db.Model):
    __tablename__ = 'timetable'
    time_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    albano = db.Column(db.BigInteger, db.ForeignKey('alba.albano'), nullable=False)
    weekday = db.Column(db.String(10), nullable=False)
    comno = db.Column(db.BigInteger, db.ForeignKey('company.comno'), nullable=False)
    bossno = db.Column(db.BigInteger, db.ForeignKey('boss.bossno'), nullable=False)