from project import db
from project.com.vo.LoginVO import LoginVO


class PredictionVO(db.Model):
    __tablename__ = 'predictionmaster'
    predictionId = db.Column('predictionId', db.Integer, primary_key=True, autoincrement=True)
    countryName = db.Column('countryName', db.VARCHAR(200), nullable=True)
    GREScore = db.Column('GREScore', db.Integer)
    IELTSScore = db.Column('IELTSScore', db.Integer)
    TOFELScore = db.Column('TOFELScore', db.Integer)
    GPAScore = db.Column('GPAScore', db.Integer)
    passOutYear = db.Column('passOutYear', db.Integer, nullable=False)
    workExperience = db.Column('workExperience', db.Integer, nullable=False)
    internshipMonth = db.Column('internshipMonth', db.Integer, nullable=False)
    researchPaper = db.Column('researchPaper', db.Integer, nullable=False)
    conferenceAttend = db.Column('conferenceAttend', db.Integer, nullable=False)
    university = db.Column('university', db.VARCHAR(200), nullable=True)
    predictionDate = db.Column('predictionDate', db.VARCHAR(100), nullable=True)
    predictionTime = db.Column('predictionTime', db.VARCHAR(100), nullable=True)
    prediction_LoginId = db.Column('prediction_LoginId', db.Integer, db.ForeignKey(LoginVO.loginId))

    def as_dict(self):
        return {
            'predictionId': self.predictionId,
            'countryName': self.countryName,
            'GREScore': self.GREScore,
            'IELTSScore': self.IELTSScore,
            'TOFELScore': self.TOFELScore,
            'GPAScore': self.GPAScore,
            'passOutYear': self.passOutYear,
            'workExperience': self.workExperience,
            'internshipMonth': self.internshipMonth,
            'researchPaper': self.researchPaper,
            'conferenceAttend': self.conferenceAttend,
            'university': self.university,
            'predictionDate': self.predictionDate,
            'predictionTime': self.predictionTime,
            'prediction_LoginId': self.prediction_LoginId
        }


db.create_all()
