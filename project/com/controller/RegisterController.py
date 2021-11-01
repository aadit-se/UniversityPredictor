import random
import smtplib
import string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import render_template, request, url_for, redirect, session

from project import app
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession
from project.com.dao.LoginDAO import LoginDAO
from project.com.dao.RegisterDAO import RegisterDAO
from project.com.vo.LoginVO import LoginVO
from project.com.vo.RegisterVO import RegisterVO


@app.route('/user/loadRegister')
def userLoadRegister():
    try:
        return render_template("user/addRegister.html")
    except Exception as ex:
        print(ex)


@app.route('/user/insertRegister', methods=['POST'])
def userInsertRegister():
    try:
        loginVO = LoginVO()
        loginDAO = LoginDAO()

        registerVO = RegisterVO()
        registerDAO = RegisterDAO()

        loginUsername = request.form['loginUsername']
        registerFirstname = request.form['registerFirstname']
        registerLastname = request.form['registerLastname']
        registerGender = request.form['registerGender']
        registerContactNumber = request.form['registerContactNumber']

        loginPassword = ''.join((random.choice(string.ascii_letters + string.digits)) for x in range(8))

        sender = "universitypredictor@gmail.com"

        receiver = loginUsername

        msg = MIMEMultipart()

        msg['From'] = sender

        msg['To'] = receiver

        msg['Subject'] = "LOGIN PASSWORD"

        msg.attach(MIMEText(loginPassword, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)

        server.starttls()

        server.login(sender, "UniversityPredictor")

        text = msg.as_string()

        server.sendmail(sender, receiver, text)

        loginVO.loginUsername = loginUsername
        loginVO.loginPassword = loginPassword
        loginVO.loginRole = "user"
        loginVO.loginStatus = "active"

        loginDAO.insertLogin(loginVO)

        registerVO.registerFirstname = registerFirstname
        registerVO.registerLastname = registerLastname
        registerVO.registerGender = registerGender
        registerVO.registerContactNumber = registerContactNumber
        registerVO.register_LoginId = loginVO.loginId

        registerDAO.insertRegister(registerVO)

        server.quit()

        return redirect(url_for('adminLoadLogin'))
    except Exception as ex:
        print(ex)


@app.route('/user/editRegister', methods=['GET'])
def userEditRegister():
    try:
        if adminLoginSession() == 'user':
            registerDAO = RegisterDAO()
            registerVO = RegisterVO()
            register_LoginId = session['session_loginId']
            registerVO.register_LoginId = register_LoginId
            registerVOList = registerDAO.userEditRegister(registerVO)
            print(registerVOList)
            return render_template('user/editRegister.html', registerVOList=registerVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/updateRegister', methods=['post'])
def userUpdateRegister():
    try:
        loginId = request.form['loginId']
        loginUsername = request.form['loginUsername']

        registerId = request.form['registerId']
        registerFirstname = request.form['registerFirstname']
        registerLastname = request.form['registerLastname']
        registerGender = request.form['registerGender']
        registerContactNumber = request.form['registerContactNumber']

        loginVO = LoginVO()
        loginDAO = LoginDAO()

        loginVO.loginId = loginId

        loginVOList = loginDAO.editLogin(loginVO)

        if loginVOList.loginUsername != loginUsername:
            loginVO.loginUsername = loginUsername

            loginPassword = ''.join((random.choice(string.ascii_letters + string.digits)) for x in range(8))

            sender = "universitypredictor@gmail.com"

            receiver = loginUsername

            msg = MIMEMultipart()

            msg['From'] = sender

            msg['To'] = receiver

            msg['Subject'] = "LOGIN PASSWORD"

            msg.attach(MIMEText(loginPassword, 'plain'))

            server = smtplib.SMTP('smtp.gmail.com', 587)

            server.starttls()

            server.login(sender, "UniversityPredictor")

            text = msg.as_string()

            server.sendmail(sender, receiver, text)

            server.quit()

        loginDAO.updateLogin(loginVO)

        registerVO = RegisterVO()
        registerDAO = RegisterDAO()

        registerVO.registerId = registerId
        registerVO.registerFirstname = registerFirstname
        registerVO.registerLastname = registerLastname
        registerVO.registerContactNumber = registerContactNumber
        registerVO.registerGender = registerGender
        registerVO.register_LoginId = loginId

        registerDAO.userUpdateRegister(registerVO)

        return redirect('/user/loadDashboard')

    except Exception as ex:
        print(ex)


@app.route('/admin/viewRegister')
def adminViewRegister():
    try:
        if adminLoginSession() == "admin":
            registerDAO = RegisterDAO()
            registerVOList = registerDAO.adminViewRegister()

            return render_template("admin/viewRegister.html", registerVOList=registerVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/blockUser', methods=['GET'])
def adminBlockUser():
    try:
        if adminLoginSession() == 'admin':
            loginDAO = LoginDAO()
            loginVO = LoginVO()
            loginId = request.args.get('loginId')
            loginStatus = 'deactive'

            loginVO.loginId = loginId
            loginVO.loginStatus = loginStatus

            loginDAO.blockUser(loginVO)

            return adminViewRegister()
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)
