from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String

class Note(db.Model):
    __tablename__ = "Note"
    ID = db.Column(db.Integer, primary_key=True)
    Data = db.Column(db.String(100000))
    Date = db.Column(db.DateTime(timezone=True), default=func.now())
    UserID = db.Column(db.Integer, db.ForeignKey("User.ID"))

class User(db.Model, UserMixin):
    __tablename__ = "User"
    ID = db.Column(db.Integer, primary_key=True)
    Email = db.Column(db.String(150), unique=True)
    Password = db.Column(db.String(150))
    FirstName = db.Column(db.String(150))
    Notes = db.relationship("Note") # relationship to Note

    # 当你在使用 Flask-Login 时遇到 NotImplementedError: No id attribute - override get_id 错误，
    # 这通常是因为你的用户模型中没有定义 id 属性。
    # Flask-Login 需要每个用户对象都有一个唯一的 id 属性来标识用户。
    # 根据错误的提示，override get_id 即可 
    def get_id(self):
        return self.ID