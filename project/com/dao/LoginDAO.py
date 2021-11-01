from project import db
from project.com.vo.LoginVO import LoginVO


class LoginDAO:
    def insertLogin(self, loginVo):
        db.session.add(loginVo)
        db.session.commit()

    def validateLogin(self, loginVO):
        loginList = LoginVO.query.filter_by(loginUsername=loginVO.loginUsername,
                                            loginPassword=loginVO.loginPassword)
        return loginList

    def editLogin(self, loginVO):
        loginList = LoginVO.query.get(loginVO.loginId)
        return loginList

    def updateLogin(self, loginVO):
        db.session.merge(loginVO)
        db.session.commit()

    def blockUser(self, loginVO):
        db.session.merge(loginVO)
        db.session.commit()

    def validateLoginUsername(self, loginVO):
        loginList = LoginVO.query.filter_by(loginUsername=loginVO.loginUsername).all()
        return loginList
