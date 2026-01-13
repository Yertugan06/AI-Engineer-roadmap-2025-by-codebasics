from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import util


app = FastAPI(
    title="Real Estate Price Prediction API",
    description="Predicts property prices based on input features like location, sqft, BHK, and baths.",
    version="1.0.0"
)

# --- CORS setup ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace "*" with allowed domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/locations", summary="Get available locations")
def get_location_names():
    return {"locations": util.get_location_names()}

@app.get("/predict", summary="Get estimated property price")
def get_estimated_price(
    total_sqft: float = Query(..., description="Total area in square feet"),
    bath: int = Query(..., description="Number of bathrooms"),
    bhk: int = Query(..., description="Number of bedrooms (BHK)"),
    location: str = Query(..., description="Location name"),
):
    
    estimated_price = util.get_estimated_price(total_sqft, bath, bhk, location)
    return {"estimated_price": estimated_price}


if __name__ == "__main__":
    util.load_saved_artifacts()
    uvicorn.run(app, host="127.0.0.1", port=8000)
