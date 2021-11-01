from project import db
from project.com.vo.LoginVO import LoginVO
from project.com.vo.RegisterVO import RegisterVO


class RegisterDAO:
    def insertRegister(self, registerVO):
        db.session.add(registerVO)
        db.session.commit()

    def adminViewRegister(self):
        registerList = db.session.query(RegisterVO, LoginVO). \
            join(LoginVO, RegisterVO.register_LoginId == LoginVO.loginId).all()

        return registerList

    def userEditRegister(self, registerVO):
        registerList = db.session.query(RegisterVO, LoginVO) \
            .join(LoginVO, RegisterVO.register_LoginId == LoginVO.loginId) \
            .filter(RegisterVO.register_LoginId == registerVO.register_LoginId).all()
        return registerList

    def userUpdateRegister(self, registerVO):
        db.session.merge(registerVO)
        db.session.commit()
