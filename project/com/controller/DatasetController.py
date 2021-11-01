import os
from datetime import datetime

from flask import render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

from project import app
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession
from project.com.dao.DatasetDAO import DatasetDAO
from project.com.vo.DatasetVO import DatasetVO

UPLOAD_FOLDER = "project/static/adminResource/dataset/"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/admin/loadDataset')
def adminLoadDataset():
    try:
        if adminLoginSession() == "admin":
            return render_template('admin/addDataset.html')
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/insertDataset', methods=['POST'])
def adminInsertDataset():
    try:
        if adminLoginSession() == "admin":

            file = request.files['file']

            datasetFileName = secure_filename(file.filename)

            datasetFilePath = os.path.join(app.config['UPLOAD_FOLDER'])

            file.save(os.path.join(datasetFilePath, datasetFileName))

            datasetUploadDate = str(datetime.date(datetime.now()))

            datasetUploadTime = str(datetime.time(datetime.now()))

            datasetDAO = DatasetDAO()
            datasetVO = DatasetVO()

            datasetVO.datasetFileName = datasetFileName
            datasetVO.datasetFilePath = datasetFilePath.replace('project', "..")
            datasetVO.datasetUploadDate = datasetUploadDate
            datasetVO.datasetUploadTime = datasetUploadTime

            datasetDAO.insertDataset(datasetVO)

            return redirect(url_for('adminViewDataset'))
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/admin/viewDataset')
def adminViewDataset():
    try:
        if adminLoginSession() == "admin":
            datasetDAO = DatasetDAO()
            datasetVOList = datasetDAO.viewDataset()
            return render_template("admin/viewDataset.html", datasetVOList=datasetVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/deleteDataset', methods=['GET'])
def adminDeleteDataset():
    try:
        if adminLoginSession() == "admin":
            datasetVO = DatasetVO()

            datasetDAO = DatasetDAO()

            datasetId = request.args.get('datasetId')
            datasetFileName = request.args.get('datasetFileName')

            print(datasetFileName)

            datasetVO.datasetId = datasetId
            datasetVO.datasetFileName = datasetFileName

            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], datasetFileName))
            datasetDAO.deleteDataset(datasetVO)

            return redirect(url_for('adminViewDataset'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)
