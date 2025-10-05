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