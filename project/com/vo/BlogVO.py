from project import db
from project.com.vo.LoginVO import LoginVO


class BlogVO(db.Model):
    __tablename__ = 'blogmaster'
    blogId = db.Column('blogId', db.INTEGER, primary_key=True, autoincrement=True)
    blogSubject = db.Column('blogSubject', db.VARCHAR(200), nullable=False)
    blogDescription = db.Column('blogDescription', db.VARCHAR(200), nullable=False)
    blogDate = db.Column('blogDate', db.VARCHAR(100), nullable=False)
    blogTime = db.Column('blogTime', db.VARCHAR(100), nullable=False)
    blogTo_LoginId = db.Column('blogTo_LoginId', db.Integer, db.ForeignKey(LoginVO.loginId))
    blogFrom_LoginId = db.Column('blogFrom_LoginId', db.Integer, db.ForeignKey(LoginVO.loginId))

    def as_dict(self):
        return {
            ' blogId': self. blogId,
            ' blogSubject': self. blogSubject,
            ' blogDescription': self. blogDescription,
            ' blogDate': self. blogDate,
            ' blogTime': self. blogTime,
            ' blogTo_LoginId': self. blogTo_LoginId,
            ' blogFrom_LoginId': self. blogFrom_LoginId,

        }


db.create_all()
