import gradio as gr
import requests

BASE_URL = "http://127.0.0.1/api"


def get_location_names():
    try:
        res = requests.get(f"{BASE_URL}/locations")
        if res.status_code == 200:
            return res.json().get("locations", [])
    except Exception as e:
        print("Error fetching locations:", e)
    return []


def get_estimated_price(total_sqft, bath, bhk, location):
    if not all([total_sqft, bath, bhk, location]):
        return "⚠️ Please fill in all fields."

    try:
        params = {
            "total_sqft": total_sqft,
            "bath": bath,
            "bhk": bhk,
            "location": location,
        }
        res = requests.get(f"{BASE_URL}/predict", params=params)
        if res.status_code == 200:
            price = res.json().get("estimated_price", "N/A")
            return f"🏠 Estimated Price: ₹{price} Lakh"
        else:
            return f"⚠️ Server error ({res.status_code})"
    except Exception as e:
        return f"❌ Error: {e}"


def build_ui():
    with gr.Blocks(title="🏡 Real Estate Price Estimator") as demo:
        gr.Markdown("## 🏙️ Real Estate Price Prediction")
        locations = get_location_names()

        total_sqft = gr.Textbox(label="Total Area (sqft)", placeholder="e.g. 1200")
        bath = gr.Textbox(label="Bathrooms", placeholder="e.g. 2")
        bhk = gr.Textbox(label="Bedrooms (BHK)", placeholder="e.g. 3")
        location = gr.Dropdown(choices=locations, label="Location")
        output = gr.Textbox(label="Predicted Price", interactive=False)
        estimate_btn = gr.Button("Estimate Price 🏠")

        estimate_btn.click(
            fn=get_estimated_price,
            inputs=[total_sqft, bath, bhk, location],
            outputs=output,
        )

    return demo


if __name__ == "__main__":
    demo = build_ui()
    demo.launch(theme="soft")
