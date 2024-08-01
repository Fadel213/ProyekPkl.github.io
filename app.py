from flask import Flask, render_template, send_from_directory, jsonify
import os
import pandas as pd

app = Flask(__name__)

# Route for serving the main page
@app.route('/')
def PKL_web():
    return render_template('PKl_web.html')

# Route to fetch Excel data
@app.route('/data/book1')
def get_data():
    excel_path = os.path.join('data', 'Book1.xlsx')
    df = pd.read_excel(excel_path)
    data = df.to_dict(orient='records')
    return jsonify(data)

# Route for serving static files in data directory
@app.route('/data/<path:filename>')
def data(filename):
    return send_from_directory('data', filename)

if __name__ == '__main__':
    app.run(debug=True)
