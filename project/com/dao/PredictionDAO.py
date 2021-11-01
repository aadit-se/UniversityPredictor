from project import db
from project.com.vo.PredictionVO import PredictionVO


class PredictionDAO:
    def insertPrediction(self, predictionVO):
        db.session.add(predictionVO)
        db.session.commit()

    def viewPrediction(self, predictionVO):
        predictionList = PredictionVO.query.filter_by(prediction_LoginId=predictionVO.prediction_LoginId).all()
        return predictionList

    def deletePrediction(self, predictionVO):
        predictionId = PredictionVO.query.get(predictionVO.predictionId)

        db.session.delete(predictionId)

        db.session.commit()

    def adminViewCountry(self):
        countryList = db.session.query(PredictionVO.countryName.distinct()).all()
        return countryList

    def ajaxGPACount(self, predictionVO):
        predictionList = db.session.query(PredictionVO.predictionId, PredictionVO.university, PredictionVO.GPAScore) \
            .filter(PredictionVO.countryName == predictionVO.countryName).all()
        return predictionList
