import os
from datetime import datetime

from flask import render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename

from project import app
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession
from project.com.dao.ComplainDAO import ComplainDAO
from project.com.vo.ComplainVO import ComplainVO

UPLOAD_FOLDER = "project/static/adminResource/complain/"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/admin/viewComplain')
def adminViewComplain():
    try:
        if adminLoginSession() == "admin":
            complainVO = ComplainVO()
            complainDAO = ComplainDAO()
            complainVO.complainStatus = "Pending"
            complainVOList = complainDAO.adminViewComplain(complainVO)

            return render_template('admin/viewComplain.html', complainVOList=complainVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/loadComplainReply', methods=['GET'])
def adminLoadComplainReplay():
    try:
        if adminLoginSession() == "admin":
            complainDAO = ComplainDAO()
            complainVO = ComplainVO()
            complainId = request.args.get('complainId')
            complainVO.complainId = complainId
            complainVOList = complainDAO.adminEditComplain(complainVO)

            return render_template('admin/addComplainReply.html', complainVOList=complainVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/insertComplainReply', methods=['POST'])
def adminInsertComplainReply():
    try:
        if adminLoginSession() == 'admin':

            complainDAO = ComplainDAO()
            complainVO = ComplainVO()

            complainId = request.form['complainId']
            replySubject = request.form['replySubject']
            replyMessage = request.form['replyMessage']

            replyDate = str(datetime.date(datetime.now()))

            replyTime = str(datetime.time(datetime.now()))

            complainStatus = 'Replied'

            complainTo_LoginId = session['session_loginId']

            file = request.files['file']

            replyFileName = secure_filename(file.filename)

            replyFilePath = os.path.join(app.config['UPLOAD_FOLDER'])

            file.save(os.path.join(replyFilePath, replyFileName))

            complainVO.complainId = complainId
            complainVO.replySubject = replySubject
            complainVO.replyMessage = replyMessage
            complainVO.replyFileName = replyFileName
            complainVO.replyFilePath = replyFilePath.replace('project', '..')
            complainVO.replyDate = replyDate
            complainVO.replyTime = replyTime
            complainVO.complainTo_LoginId = complainTo_LoginId
            complainVO.complainStatus = complainStatus

            complainDAO.adminInsertComplainReply(complainVO)
            return redirect(url_for('adminViewComplain'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


# user

@app.route('/user/loadComplain')
def userLoadComplain():
    try:
        if adminLoginSession() == "user":
            return render_template('user/addComplain.html')
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/insertComplain', methods=['POST'])
def userInsertComplain():
    try:
        if adminLoginSession() == 'user':
            complainDAO = ComplainDAO()
            complainVO = ComplainVO()

            complainSubject = request.form['complainSubject']
            complainDescription = request.form['complainDescription']

            complainDate = str(datetime.date(datetime.now()))

            complainTime = str(datetime.time(datetime.now()))

            complainStatus = 'Pending'

            file = request.files['file']

            complainFileName = secure_filename(file.filename)

            complainFilePath = os.path.join(app.config['UPLOAD_FOLDER'])

            file.save(os.path.join(complainFilePath, complainFileName))

            complainFrom_LoginId = session['session_loginId']

            complainVO.complainSubject = complainSubject
            complainVO.complainDescription = complainDescription
            complainVO.complainDate = complainDate
            complainVO.complainTime = complainTime
            complainVO.complainStatus = complainStatus
            complainVO.complainFileName = complainFileName
            complainVO.complainFilePath = complainFilePath.replace('project', '..')
            complainVO.complainFrom_LoginId = complainFrom_LoginId

            complainDAO.userInsertComplain(complainVO)

            return redirect(url_for('userViewComplain'))
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/user/viewComplain')
def userViewComplain():
    try:
        if adminLoginSession() == "user":
            complainDAO = ComplainDAO()
            complainVO = ComplainVO()
            complainFrom_LoginId = session['session_loginId']
            complainVO.complainFrom_LoginId = complainFrom_LoginId
            complainVOList = complainDAO.userViewComplain(complainVO)
            return render_template('user/viewComplain.html', complainVOList=complainVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/deleteComplain', methods=['GET'])
def userDeleteComplain():
    try:
        if adminLoginSession() == 'user':
            complainVO = ComplainVO()

            complainDAO = ComplainDAO()

            complainId = request.args.get('complainId')
            complainFileName = request.args.get('complainFileName')

            complainVO.complainId = complainId
            complainVO.complainFileName = complainFileName

            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], complainFileName))
            complainDAO.userDeleteComplain(complainVO)
            return redirect(url_for('userViewComplain'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route("/user/viewComplainReply", methods=['GET'])
def userViewComplainReplay():
    try:
        if adminLoginSession() == "user":
            complainDAO = ComplainDAO()
            complainVO = ComplainVO()
            complainId = request.args.get('complainId')
            complainVO.complainId = complainId
            complainVOList = complainDAO.userViewComplainReply(complainVO)
            return render_template("user/viewComplainReply.html", complainVOList=complainVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)
