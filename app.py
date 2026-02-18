from flask import Flask, render_template, request
from groq import Groq
import os
from dotenv import load_dotenv

# 1. Load your API key from the .env file
load_dotenv()

app = Flask(__name__)

# 2. Initialize the Groq Client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@app.route("/", methods=["GET", "POST"])
def index():
    recommendation = None
    if request.method == "POST":
        budget = request.form.get("budget")
        days = request.form.get("days")
        month = request.form.get("month")
        interests = request.form.get("interests")

        # 3. Specialized Prompt for India with all 4 transport modes
        prompt = (
            f"Act as a professional Indian Travel Consultant. Plan a {days}-day trip in India "
            f"for the month of {month} with a total budget of ₹{budget}. "
            f"User Interests: {interests}. "
            f"Requirements: "
            f"- Provide a day-by-day itinerary. "
            f"- Use Indian Rupees (₹) for all costs. "
            f"- Recommend the best mix of transport: Airlines, Indian Railways (Trains), "
            f"Inter-city Buses, and Car rentals/Taxis based on the distance and budget."
        )
        
        try:
            # 4. Use the correct current model
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile", 
                messages=[
                    {"role": "system", "content": "You are an expert in Indian tourism and multi-modal transportation logistics."},
                    {"role": "user", "content": prompt}
                ]
            )
            recommendation = completion.choices[0].message.content
        except Exception as e:
            recommendation = f"Error: {str(e)}"

    return render_template("index.html", recommendation=recommendation)

if __name__ == "__main__":
    app.run(debug=True)