import warnings
from datetime import datetime

import pandas as pd
from flask import *
from sklearn import preprocessing
from sklearn.externals import joblib

from project import app
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession
from project.com.dao.PredictionDAO import PredictionDAO
from project.com.vo.PredictionVO import PredictionVO

warnings.filterwarnings('ignore')


@app.route("/user/loadPrediction")
def userLoadPredicion():
    try:

        if adminLoginSession() == "user":
            return render_template('user/addPrediction.html')
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route("/user/insertPrediction", methods=["POST"])
def userInsertPrediction():
    try:
        if adminLoginSession() == "user":
            predictionVO = PredictionVO()
            predictionDAO = PredictionDAO()

            countryName = request.form["countryName"]

            examType = request.form['examType']

            passOutYear = request.form['passOutYear']
            workExperience = request.form['workExperience']
            internshipMonth = request.form['internshipMonth']
            researchPaper = request.form['researchPaper']
            conferenceAttend = request.form['conferenceAttend']

            currentDate = str(datetime.now().date())
            currentTime = datetime.now().strftime('%H:%M:%S')

            if countryName == 'Australia':
                AustraliaUniversityList = ['University of Melbourne', 'Australian National University',
                                           'University of Sydney',
                                           'University of Queensland', 'Monash University', 'University of Adelaide',
                                           'University of Western Australia', 'University of Canberra',
                                           'Griffith University',
                                           'James Cook University','University of Wollongong','Queensland University of Tecgnology',
                                           'Curtin University','Macquarie University','RMIT University','Deakin University',
                                           'University of Southern Australia (UniSA)','University of Tasmania','Griffith University','James Cook University (JCU)'
                                           ,'Swinburne University of Technology','La Trobe University','Flinders University',
                                           'Bond University']

                GPA = float(request.form['GPA'])

                columnName = ['IELTS', 'TOFEL', 'GPA', 'PassOutYear', 'WorkExp', 'InternshipMonth', 'ResearchPaper',
                              'ConferenceAttend']

                model_dump = joblib.load('project/static/userResource/Model/Model_AUS.sav')

                le1 = preprocessing.LabelEncoder()
                le1.fit_transform(AustraliaUniversityList)

                if examType == 'IELTS':
                    IELTS = float(request.form['IELTS_Score'])
                    columnValue = [IELTS, 0, GPA, passOutYear, workExperience, internshipMonth, researchPaper,
                                   conferenceAttend]

                    X = pd.DataFrame([columnValue], columns=columnName)

                    X_test = X.as_matrix()
                    print(type(X_test))

                    prediction = model_dump.predict(X_test)
                    print('predictiom>>>>', prediction)

                    ans = str(le1.inverse_transform(prediction))

                    j = ans.replace("['", "")
                    universityName = j.replace("']", "")
                    print('universityName>>>', universityName)

                    predictionVO.IELTSScore = IELTS
                    predictionVO.university = universityName

                elif examType == 'TOFEL':
                    TOFEL = int(request.form['TOFEL_Score'])
                    columnValue = [0, TOFEL, GPA, passOutYear, workExperience, internshipMonth, researchPaper,
                                   conferenceAttend]

                    X = pd.DataFrame([columnValue], columns=columnName)

                    X_test = X.as_matrix()
                    print(type(X_test))

                    prediction = model_dump.predict(X_test)

                    ans = str(le1.inverse_transform(prediction))

                    j = ans.replace("['", "")
                    universityName = j.replace("']", "")
                    print('universityName>>>', universityName)

                    predictionVO.TOFELScore = TOFEL
                    predictionVO.university = universityName

                predictionVO.GPAScore = GPA
                predictionVO.passOutYear = passOutYear
                predictionVO.workExperience = workExperience
                predictionVO.researchPaper = researchPaper
                predictionVO.internshipMonth = internshipMonth
                predictionVO.conferenceAttend = conferenceAttend
                predictionVO.countryName = countryName
                predictionVO.predictionDate = currentDate
                predictionVO.predictionTime = currentTime
                predictionVO.prediction_LoginId = session['session_loginId']

                predictionDAO.insertPrediction(predictionVO)

            elif countryName == 'Canada':
                CanadaUniversityList = ['University of Alberta', 'The University of British Columbia',
                                        'McGill University',
                                        'University of Toronto', 'University of Waterloo', 'University of Windsor',
                                        'University of Calgary', 'University of Saskatchewan', 'University of Ottawa',
                                        'Dalhousie University','Simon Fraser University','York University',
                                        "Queen's University",'McMaster University','Western University','University of Victoria'
                                        'Université de Montréal','Université Laval']
                GRE = request.form['GRE']
                GPA = float(request.form['GPA'])
                IELTS = float(request.form['IELTS_Score'])

                columnName = ['GRE', 'IELTS', 'GPA', 'PassOutYear', 'WorkExp', 'InternshipMonth', 'ResearchPaper',
                              'ConferenceAttend']

                model_dump = joblib.load('project/static/userResource/Model/Model_Canada.sav')

                le1 = preprocessing.LabelEncoder()
                le1.fit_transform(CanadaUniversityList)

                columnValue = [GRE, IELTS, GPA, passOutYear, workExperience, internshipMonth, researchPaper,
                               conferenceAttend]

                X = pd.DataFrame([columnValue], columns=columnName)

                X_test = X.as_matrix()
                print(type(X_test))

                prediction = model_dump.predict(X_test)
                print('predictiom>>>>', prediction)

                ans = str(le1.inverse_transform(prediction))

                j = ans.replace("['", "")
                universityName = j.replace("']", "")
                print('universityName>>>', universityName)

                predictionVO.GREScore = GRE
                predictionVO.GPAScore = GPA
                predictionVO.IELTSScore = IELTS
                predictionVO.passOutYear = passOutYear
                predictionVO.workExperience = workExperience
                predictionVO.researchPaper = researchPaper
                predictionVO.internshipMonth = internshipMonth
                predictionVO.conferenceAttend = conferenceAttend
                predictionVO.university = universityName
                predictionVO.countryName = countryName
                predictionVO.predictionDate = currentDate
                predictionVO.predictionTime = currentTime
                predictionVO.prediction_LoginId = session['session_loginId']
                predictionDAO.insertPrediction(predictionVO)

            elif countryName == 'USA':
                USAUniversityList = ['Massachusetts Institute of Technology (MIT) ', 'Stanford University',
                                     'Harvard University ',
                                     'University of Pennsylvania', 'University of California, Berkeley (UCB)',
                                     'Princeton University',
                                     'University of California, Los Angeles (UCLA)',
                                     'Georgia Institute of Technology (Georgia Tech)',
                                     'University of Washington',
                                     'University of Texas at Austin','California Institute of Technology','Yale University',
                                     'University of Chicago','Johns Hopkins University','Columbia University','Cornell University',
                                     'Duke University','University of Michigan-Ann Arbor','Northwestern University',
                                     'Carnegie Mellon University','New York University',
                                     'University of California, San Diego',
                                     'University of Illinois at Urbana-Champaign',
                                     'University of Wisconsin-Madison',
                                     ]

                GPA = float(request.form['GPA'])
                GRE = request.form['GRE']

                columnName = ['GRE', 'IELTS', 'GPA', 'TOFEL', 'PassOutYear', 'WorkExp', 'InternshipMonth',
                              'ResearchPaper',
                              'ConferenceAttend']

                model_dump = joblib.load('project/static/userResource/Model/Model_USA.sav')

                le1 = preprocessing.LabelEncoder()
                le1.fit_transform(USAUniversityList)

                if examType == 'IELTS':
                    IELTS = float(request.form['IELTS_Score'])
                    columnValue = [GRE, IELTS, GPA, 0, passOutYear, workExperience, internshipMonth, researchPaper,
                                   conferenceAttend]

                    X = pd.DataFrame([columnValue], columns=columnName)

                    X_test = X.as_matrix()
                    print(type(X_test))

                    prediction = model_dump.predict(X_test)
                    print('predictiom>>>>', prediction)

                    ans = str(le1.inverse_transform(prediction))

                    j = ans.replace("['", "")
                    universityName = j.replace("']", "")
                    print('universityName>>>', universityName)

                    predictionVO.IELTSScore = IELTS
                    predictionVO.university = universityName

                elif examType == 'TOFEL':
                    TOFEL = int(request.form['TOFEL_Score'])
                    columnValue = [GRE, 0, GPA, TOFEL, passOutYear, workExperience, internshipMonth, researchPaper,
                                   conferenceAttend]

                    X = pd.DataFrame([columnValue], columns=columnName)

                    X_test = X.as_matrix()
                    print(type(X_test))

                    prediction = model_dump.predict(X_test)

                    ans = str(le1.inverse_transform(prediction))

                    j = ans.replace("['", "")
                    universityName = j.replace("']", "")
                    print('universityName>>>', universityName)

                    predictionVO.TOFELScore = TOFEL
                    predictionVO.university = universityName

                predictionVO.GPAScore = GPA
                predictionVO.passOutYear = passOutYear
                predictionVO.workExperience = workExperience
                predictionVO.researchPaper = researchPaper
                predictionVO.internshipMonth = internshipMonth
                predictionVO.conferenceAttend = conferenceAttend
                predictionVO.countryName = countryName
                predictionVO.predictionDate = currentDate
                predictionVO.predictionTime = currentTime
                predictionVO.prediction_LoginId = session['session_loginId']
                predictionDAO.insertPrediction(predictionVO)
        else:
            return adminLogoutSession()

        return redirect(url_for('userViewPrediction'))

    except Exception as ex:
        print(ex)


@app.route('/user/viewPrediction', methods=['GET'])
def userViewPrediction():
    try:
        if adminLoginSession() == "user":
            predictionVO = PredictionVO()
            predictionDAO = PredictionDAO()

            predictionVO.prediction_LoginId = session['session_loginId']

            predictionVOList = predictionDAO.viewPrediction(predictionVO)
            print('predictionVOList>>>>>', predictionVOList)

        else:
            return adminLogoutSession()

        return render_template('user/viewPrediction.html', predictionVOList=predictionVOList)
    except Exception as ex:
        print(ex)


@app.route('/user/deletePrediction', methods=['GET'])
def userDeletePrediction():
    try:
        if adminLoginSession() == "user":
            predictionVO = PredictionVO()
            predictionDAO = PredictionDAO()

            predictionId = request.args.get('predictionId')

            predictionVO.predictionId = predictionId

            predictionDAO.deletePrediction(predictionVO)

        else:
            return adminLogoutSession()

        return redirect(url_for('userViewPrediction'))
    except Exception as ex:
        print(ex)
