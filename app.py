from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import joblib
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Form

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


class Item(BaseModel):
    NO_OF_ADULTS: float
    NO_OF_WEEKEND_NIGHTS: float
    NO_OF_WEEK_NIGHTS: float
    REQUIRED_CAR_PARKING_SPACE: float
    LEAD_TIME: float
    ARRIVAL_YEAR: float
    ARRIVAL_MONTH: float
    ARRIVAL_DATE: float
    AVG_PRICE_PER_ROOM: float
    NO_OF_SPECIAL_REQUESTS: float
    NO_OF_NIGHTS: float
    TOTAL_PRICE: float
    WEEKEND_PRICE: float
    WEEKDAY_PRICE: float
    ROOM_TYPE_CATEGORIZED: float
    TYPE_OF_MEAL_PLAN_NOT_SELECTED: float
    MARKET_SEGMENT_TYPE_OFFLINE: float
    MARKET_SEGMENT_TYPE_ONLINE: float


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/predict")
async def predict(request: Request,
                  NO_OF_ADULTS: float = Form(...),
                  NO_OF_WEEKEND_NIGHTS: float = Form(...),
                  NO_OF_WEEK_NIGHTS: float = Form(...),
                  REQUIRED_CAR_PARKING_SPACE: float = Form(...),
                  LEAD_TIME: float = Form(...),
                  ARRIVAL_YEAR: float = Form(...),
                  ARRIVAL_MONTH: float = Form(...),
                  ARRIVAL_DATE: float = Form(...),
                  AVG_PRICE_PER_ROOM: float = Form(...),
                  NO_OF_SPECIAL_REQUESTS: float = Form(...),
                  NO_OF_NIGHTS: float = Form(...),
                  TOTAL_PRICE: float = Form(...),
                  WEEKEND_PRICE: float = Form(...),
                  WEEKDAY_PRICE: float = Form(...),
                  ROOM_TYPE_CATEGORIZED: float = Form(...),
                  TYPE_OF_MEAL_PLAN_NOT_SELECTED: float = Form(...),
                  MARKET_SEGMENT_TYPE_OFFLINE: float = Form(...),
                  MARKET_SEGMENT_TYPE_ONLINE: float = Form(...)):
    data = {
        "NO_OF_ADULTS": NO_OF_ADULTS,
        "NO_OF_WEEKEND_NIGHTS": NO_OF_WEEKEND_NIGHTS,
        "NO_OF_WEEK_NIGHTS": NO_OF_WEEK_NIGHTS,
        "REQUIRED_CAR_PARKING_SPACE": REQUIRED_CAR_PARKING_SPACE,
        "LEAD_TIME": LEAD_TIME,
        "ARRIVAL_YEAR": ARRIVAL_YEAR,
        "ARRIVAL_MONTH": ARRIVAL_MONTH,
        "ARRIVAL_DATE": ARRIVAL_DATE,
        "AVG_PRICE_PER_ROOM": AVG_PRICE_PER_ROOM,
        "NO_OF_SPECIAL_REQUESTS": NO_OF_SPECIAL_REQUESTS,
        "NO_OF_NIGHTS": NO_OF_NIGHTS,
        "TOTAL_PRICE": TOTAL_PRICE,
        "WEEKEND_PRICE": WEEKEND_PRICE,
        "WEEKDAY_PRICE": WEEKDAY_PRICE,
        "ROOM_TYPE_CATEGORIZED": ROOM_TYPE_CATEGORIZED,
        "TYPE_OF_MEAL_PLAN_NOT_SELECTED": TYPE_OF_MEAL_PLAN_NOT_SELECTED,
        "MARKET_SEGMENT_TYPE_OFFLINE": MARKET_SEGMENT_TYPE_OFFLINE,
        "MARKET_SEGMENT_TYPE_ONLINE": MARKET_SEGMENT_TYPE_ONLINE
    }
    X_test = []

    for key in data:
        if key == 'no-of-adults':
            X_test.append(int(data[key]))
        elif key == 'no-of-nights':
            X_test.append(int(data[key]))
        elif key == 'arrival-date':
            date = data[key]
            year, month, day = (int(x) for x in date.split('-'))
            X_test.append(year)
            X_test.append(month)
            X_test.append(day)
        elif key == 'arrival-month':
            X_test.append(int(data[key]))
        elif key == 'required-parking':
            X_test.append(int(data[key]))
        elif key == 'lead-time':
            X_test.append(int(data[key]))
        elif key == 'room-type':
            if data[key] == 'Standard Room':
                X_test.extend([1, 0, 0])
            elif data[key] == 'Superior Room':
                X_test.extend([0, 1, 0])
            elif data[key] == 'Deluxe Room':
                X_test.extend([0, 0, 1])
        elif key == 'meal-plan':
            if data[key] == 'No Meal Package':
                X_test.extend([1, 0])
            else:
                X_test.extend([0, 1])
        elif key == 'market-segment':
            if data[key] == 'Online':
                X_test.extend([0, 1])
            else:
                X_test.extend([1, 0])
        elif key == 'special-requests':
            X_test.append(int(data[key]))

        model = joblib.load("final_model.pkl")
        # X_test listesi üzerinden tahmin yap
        prediction = model.predict([X_test])

        # Tahmin sonucunu kullanıcıya göster
        from tkinter import messagebox
        messagebox.showinfo("Prediction Result", f"The predicted price is {prediction[0]:.2f} €.")
