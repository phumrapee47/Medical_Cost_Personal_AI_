import os
import pandas as pd
import json
from flask import Flask, render_template, request, redirect, url_for, flash, Response
from dotenv import load_dotenv
from utils.supabase_db import fetch_data, save_data
import io
from utils.ml_engine import predict_insurance_charges

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-key-12345")

@app.route('/')
def index():
    """Main dashboard page."""
    try:
        # Fetching data for visualization
        data = fetch_data("insurance")
        df = pd.DataFrame(data)
        
        # Pass all data to the frontend for advanced visual manipulations
        if not df.empty:
            chart_data = df.to_dict(orient='records')
        else:
            chart_data = []

        return render_template('index.html', chart_data=json.dumps(chart_data))
    except Exception as e:
        flash(f"Database error: {str(e)}", "error")
        return render_template('index.html', chart_data="{}")

@app.route('/analysis', methods=['GET', 'POST'])
def analysis():
    """ML Analysis results and prediction form."""
    prediction = None
    if request.method == 'POST':
        try:
            # We assume a form is posted with insurance features
            input_data = {
                "age": int(request.form.get("age", 0)),
                "sex": request.form.get("sex", "male"),
                "bmi": float(request.form.get("bmi", 0.0)),
                "children": int(request.form.get("children", 0)),
                "smoker": request.form.get("smoker", "no"),
                "region": request.form.get("region", "southwest")
            }
            
            # Predict
            charges = predict_insurance_charges(input_data)
            prediction = round(charges, 2)
            
            # Save back to database
            input_data["charges"] = prediction
            save_data("insurance", input_data)
            flash("Prediction successful and saved to database!", "success")
            
        except Exception as e:
            flash(f"Error during prediction: {str(e)}", "error")

    # Fetch recent data to display (newest is on top via API)
    data = fetch_data("insurance")
    return render_template('analysis.html', prediction=prediction, data=data[:10] if data else [])

@app.route('/export')
def export_data():
    """Exporting data to CSV list."""
    try:
        data = fetch_data("insurance")
        df = pd.DataFrame(data)
        
        # Write to CSV in memory
        output = io.StringIO()
        df.to_csv(output, index=False)
        output.seek(0)
        
        return Response(
            output, 
            mimetype="text/csv",
            headers={"Content-Disposition": "attachment;filename=insurance_data.csv"}
        )
    except Exception as e:
        flash(f"Export error: {str(e)}", "error")
        return redirect(url_for('index'))

@app.route('/data')
def database_view():
    """View to show the full database."""
    try:
        data = fetch_data("insurance")
    except Exception as e:
        flash(f"Database error: {str(e)}", "error")
        data = []
    return render_template('data.html', data=data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
