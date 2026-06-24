import sqlite3
from flask import Flask, render_template, request, Response
import pickle

app = Flask(__name__)

# Load AI Model
model = pickle.load(open("model.pkl", "rb"))

# Home Page
@app.route("/")
def home():
    return render_template("login.html")

# Login Page
@app.route("/login")
def login():
    return render_template("login.html")
@app.route("/history")
def history():

    conn = sqlite3.connect("predictions.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM predictions")
    records = cursor.fetchall()

    conn.close()

    return render_template(
        "history.html",
        records=records
    )
@app.route("/dashboard")
def dashboard():

    conn = sqlite3.connect("predictions.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM predictions")
    total_predictions = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM predictions WHERE prediction='High Defect Risk'")
    high_risk = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM predictions WHERE prediction='Low Defect Risk'")
    low_risk = cursor.fetchone()[0]

    total = total_predictions if total_predictions > 0 else 1

    high_percent = round((high_risk / total) * 100)
    low_percent = round((low_risk / total) * 100)

    conn.close()

    return render_template(
    "dashboard.html",
    total_predictions=total_predictions,
    high_risk=high_risk,
    low_risk=low_risk,
    high_percent=high_percent,
    low_percent=low_percent
)
@app.route("/predictpage")
def predictpage():
    return render_template("index.html")
@app.route("/about")
def about():
    return render_template("about.html")
@app.route("/export")
def export():

    conn = sqlite3.connect("predictions.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM predictions")
    data = cursor.fetchall()

    conn.close()

    csv_data = "ID,Size,Complexity,Experience,Prediction,Risk Score\n"

    for row in data:
        csv_data += f"{row[0]},{row[1]},{row[2]},{row[3]},{row[4]},{row[5]}\n"

    return Response(
        csv_data,
        mimetype="text/csv",
        headers={
            "Content-Disposition":
            "attachment; filename=prediction_report.csv"
        }
    )

# Prediction
@app.route("/predict", methods=["POST"])
def predict():

    size = int(request.form["size"])
    complexity = int(request.form["complexity"])
    experience = int(request.form["experience"])

    result = model.predict([[size, complexity, experience]])

    risk_score = min(100, int((size + complexity) * 5 - experience * 2))

    if result[0] == 1:
        prediction = "High Defect Risk"
        recommendation = """
• Perform Code Review
• Increase Testing Coverage
• Refactor Complex Modules
"""
    else:
        prediction = "Low Defect Risk"
        recommendation = """
• Continue Current Development Process
• Maintain Code Quality
• Perform Regular Testing
"""

    # Save to Database
    conn = sqlite3.connect("predictions.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO predictions
    (size, complexity, experience, prediction, risk_score)
    VALUES (?, ?, ?, ?, ?)
    """,
    (size, complexity, experience, prediction, risk_score))

    conn.commit()
    conn.close()

    return render_template(
        "result.html",
        prediction=prediction,
        risk_score=risk_score,
        recommendation=recommendation
    )

if __name__ == "__main__":
    app.run(debug=True)

