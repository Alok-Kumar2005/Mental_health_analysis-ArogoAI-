from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
import pickle

with open('random_forest_model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('label_encoders.pkl', 'rb') as f:
    label_encoders = pickle.load(f)

app = FastAPI()


class InputData(BaseModel):
    Age: float
    SleepPerDayHours: float
    NumberOfFriend: float
    Gender: str  
    AcademicPerformance: str  
    TakingNoteInClass: str 
    FaceChallangesToCompleteAcademicTask: str  
    LikePresentation: str 
    LikeNewThings: str 

@app.post("/predict/")
async def predict(data: InputData):
    try:
        gender_encoded = label_encoders['Gender'].transform([data.Gender])[0]
        academic_performance_encoded = label_encoders['AcademicPerformance'].transform([data.AcademicPerformance])[0]
        taking_notes_encoded = label_encoders['TakingNoteInClass'].transform([data.TakingNoteInClass])[0]
        challenges_encoded = label_encoders['FaceChallangesToCompleteAcademicTask'].transform([data.FaceChallangesToCompleteAcademicTask])[0]
        like_presentation_encoded = label_encoders['LikePresentation'].transform([data.LikePresentation])[0]
        like_new_things_encoded = label_encoders['LikeNewThings'].transform([data.LikeNewThings])[0]

        input_features = np.array([
            data.Age,
            data.SleepPerDayHours,
            data.NumberOfFriend,
            gender_encoded,
            academic_performance_encoded,
            taking_notes_encoded,
            challenges_encoded,
            like_presentation_encoded,
            like_new_things_encoded
        ]).reshape(1, -1)

        prediction = model.predict(input_features)

        target_encoder = label_encoders['DepressionStatus']
        prediction_label = target_encoder.inverse_transform(prediction)

        return {"prediction": prediction_label[0]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)