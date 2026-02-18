import os
from flask import Flask, render_template, request
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@app.route("/", methods=["GET", "POST"])
def index():
    recommendation = ""
    if request.method == "POST":
        budget = request.form.get("budget")
        days = request.form.get("days")
        month = request.form.get("month")
        interests = request.form.get("interests") or "general sightseeing"

        try:
            # Updated prompt including month and removing currency restrictions
            prompt = (
                f"Plan a {days}-day trip for the month of {month}. "
                f"Total Budget: {budget}. Interests: {interests}. "
                f"Suggest a suitable destination for this month and budget, "
                f"provide a day-by-day itinerary, and a cost breakdown."
            )

            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are a professional travel planner."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
            )
            recommendation = completion.choices[0].message.content
        except Exception as e:
            recommendation = f"Error: {str(e)}"

    return render_template("index.html", recommendation=recommendation)

if __name__ == "__main__":
    app.run(debug=True)