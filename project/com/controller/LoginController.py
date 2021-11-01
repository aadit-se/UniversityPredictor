import random
import smtplib
import string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import render_template, request, redirect, url_for, session, jsonify

from project import app
from project.com.dao.FeedbackDAO import FeedbackDAO
from project.com.dao.LoginDAO import LoginDAO
from project.com.dao.PredictionDAO import PredictionDAO
from project.com.vo.LoginVO import LoginVO
from project.com.vo.PredictionVO import PredictionVO


@app.route('/')
def adminLoadLogin():
    try:
        session.clear()
        return render_template('admin/login.html')
    except Exception as ex:
        print(ex)


@app.route("/admin/validateLogin", methods=['POST'])
def adminValidateLogin():
    try:
        loginUsername = request.form['loginUsername']
        loginPassword = request.form['loginPassword']

        loginVO = LoginVO()
        loginDAO = LoginDAO()

        loginVO.loginUsername = loginUsername
        loginVO.loginPassword = loginPassword
        loginVO.loginStatus = "active"

        loginVOList = loginDAO.validateLogin(loginVO)

        loginDictList = [i.as_dict() for i in loginVOList]

        lenLoginDictList = len(loginDictList)

        if lenLoginDictList == 0:

            msg = "Something Is Wrong!"

            return render_template('admin/login.html', error=msg)

        elif loginDictList[0]['loginStatus'] == 'inactive':

            msg = 'Your account access is temporary Blocked by Admin !'
            return render_template('admin/login.html', error=msg)

        else:
            for row1 in loginDictList:

                loginId = row1['loginId']

                loginUsername = row1['loginUsername']

                loginRole = row1['loginRole']

                session['session_loginId'] = loginId

                session['session_loginUsername'] = loginUsername

                session['session_loginRole'] = loginRole

                session.permanent = True

                if loginRole == 'admin':
                    return redirect(url_for('adminLoadDashboard'))
                elif loginRole == 'user':
                    return redirect(url_for("userLoadDashboard"))

    except Exception as ex:
        print(ex)


@app.route('/admin/loadDashboard')
def adminLoadDashboard():
    try:
        if adminLoginSession() == "admin":
            predictionDAO = PredictionDAO()

            countryList = predictionDAO.adminViewCountry()
            print('countryList>>>>>>>>', countryList)

            return render_template('admin/index.html', countryList=countryList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/ajaxGPACountGraph')
def adminAjaxGPACountGraph():
    try:
        if adminLoginSession() == "admin":
            predictionVO = PredictionVO()
            predictionDAO = PredictionDAO()

            countryName = request.args.get('countryName')

            predictionVO.countryName = countryName

            ajaxGPACountList = predictionDAO.ajaxGPACount(predictionVO)

            print('ajaxGPACountList>>>>>>>>', ajaxGPACountList)

            graphDict = {}
            counter = False
            if len(ajaxGPACountList) != 0:
                counter = True
                for i in ajaxGPACountList:
                    dict1 = {i[0]: {"University": i[1], "GPACount": i[2]}}

                    graphDict.update(dict1)

            if counter:
                response = {'responseKey': graphDict}
                print('response>>>>>>>>', response)

            else:
                response = {'responseKey': 'Error'}

            return jsonify(response)

        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/loadDashboard')
def userLoadDashboard():
    try:
        if adminLoginSession() == "user":
            feedbackDAO = FeedbackDAO()

            feedbackVOList = feedbackDAO.viewFeedback()
            print('feedbackVOList>>>', feedbackVOList)

            return render_template('user/index.html', feedbackVOList=feedbackVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/loginSession')
def adminLoginSession():
    try:
        if 'session_loginId' and 'session_loginRole' in session:
            if session['session_loginRole'] == "admin":

                return "admin"

            elif session['session_loginRole'] == "user":

                return "user"

        else:
            return False

    except Exception as ex:
        print(ex)


@app.route('/admin/logoutSession')
def adminLogoutSession():
    try:
        session.clear()
        return redirect(url_for('adminLoadLogin'))
    except Exception as ex:
        print(ex)


@app.route('/user/loadForgetPassword')
def userLoadForgetPassword():
    try:
        return render_template('user/forgetPassword.html')
    except Exception as ex:
        print(ex)


@app.route('/user/generateOTP', methods=['POST'])
def userGenerateOTP():
    try:
        loginDAO = LoginDAO()
        loginVO = LoginVO()

        loginUsername = request.form['loginUsername']
        loginVO.loginUsername = loginUsername

        loginDictList = [i.as_dict() for i in loginDAO.validateLoginUsername(loginVO)]

        if len(loginDictList) != 0:
            passwordOTP = ''.join((random.choice(string.digits)) for x in range(4))

            session['session_OTP'] = passwordOTP
            session['session_loginUsername'] = loginUsername
            session['session_loginId'] = loginDictList[0]['loginId']

            sender = "universitypredictor@gmail.com"

            receiver = loginUsername

            msg = MIMEMultipart()

            msg['From'] = sender

            msg['To'] = receiver

            msg['subject'] = "ACCOUNT PASSWORD"

            msg.attach(MIMEText('OTP to reset password is:'))

            msg.attach(MIMEText(passwordOTP, 'plain'))

            server = smtplib.SMTP('smtp.gmail.com', 587)

            server.starttls()

            server.login(sender, "UniversityPredictor")

            text = msg.as_string()

            server.sendmail(sender, receiver, text)

            server.quit()

            return render_template('user/addOTP.html')

        else:
            error = "The given Username is not registered yet!"
            return render_template("admin/login.html", error=error)

    except Exception as ex:
        print(ex)


@app.route('/user/validateOTP', methods=['POST'])
def userValidateOTP():
    try:
        passwordOTP = request.form['passwordOTP']

        if passwordOTP == session['session_OTP']:

            loginPassword = ''.join((random.choice(string.ascii_letters + string.digits)) for x in range(8))

            loginUsername = session['session_loginUsername']

            sender = "universitypredictor@gmail.com"

            receiver = loginUsername

            msg = MIMEMultipart()

            msg['From'] = sender

            msg['To'] = receiver

            msg['subject'] = "Reset Password"

            msg.attach(MIMEText('Your new Password is:'))

            msg.attach(MIMEText(loginPassword, 'plain'))

            server = smtplib.SMTP('smtp.gmail.com', 587)

            server.starttls()

            server.login(sender, "UniversityPredictor")

            text = msg.as_string()

            server.sendmail(sender, receiver, text)

            server.quit()

            loginVO = LoginVO()
            loginDAO = LoginDAO()

            loginVO.loginUsername = loginUsername
            loginVO.loginId = session['session_loginId']
            loginVO.loginPassword = loginPassword

            loginDAO.updateLogin(loginVO)

            return render_template("admin/login.html", error="Your new password is sent to your email address!")
        else:
            return render_template('admin/login.html', error="Invalid OTP,Please ty again!")

    except Exception as ex:
        print(ex)


@app.route('/user/loadResetPassword')
def userLoadResetPassword():
    try:
        if adminLoginSession() == 'user':
            return render_template('user/resetPassword.html')
        else:
            return redirect(url_for("adminLogoutSession"))

    except Exception as ex:
        print(ex)


@app.route('/user/resetPassword', methods=['POST'])
def userResetPassword():
    try:
        if adminLoginSession() == 'user':
            oldLoginPassword = request.form['oldLoginPassword']
            newLoginPassword = request.form['newLoginPassword']
            confirmNewLoginPassword = request.form['confirmNewLoginPassword']

            loginVO = LoginVO()
            loginDAO = LoginDAO()

            loginVO.loginId = session['session_loginId']
            print(loginVO.loginId)
            loginVO.loginUsername = session['session_loginUsername']
            print(loginVO.loginUsername)
            loginVO.loginPassword = oldLoginPassword
            print(loginVO.loginPassword)

            loginDictList = [i.as_dict() for i in loginDAO.validateLogin(loginVO)]
            print(loginDictList)

            if len(loginDictList) != 0:
                print([i.as_dict() for i in loginDAO.validateLogin(loginVO)])
                if newLoginPassword == confirmNewLoginPassword:
                    loginVO.loginPassword = newLoginPassword
                    loginDAO.updateLogin(loginVO)
                    return render_template("user/index.html")
                else:
                    return render_template('user/resetPassword.html',
                                           error="Invalid confirmation of new password,Please try again!")
            else:
                return render_template('user/resetPassword.html',
                                       error="Invalid old password,please enter valid Password!")

        else:
            return redirect(url_for("adminLogoutSession"))

    except Exception as ex:
        print(ex)
