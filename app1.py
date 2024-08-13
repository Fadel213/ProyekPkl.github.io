from flask import Flask, render_template, send_file, jsonify
import mysql.connector
from io import BytesIO
import pandas as pd

app = Flask(__name__)

# Database connection details
DB_CONFIG = {
    'host': 'x-e.h.filess.io',
    'database': 'sertifikat_cheesemood',
    'user': 'sertifikat_cheesemood',
    'password': 'a3d775699a18566273a5f5072be7c09d96f29b6c',
    'port': 3305
}

def get_db_connection():
    connection = mysql.connector.connect(**DB_CONFIG)
    return connection

# Route for serving the main page
@app.route('/')
def index():
    return render_template('PKL_web.html')

# Route to fetch Excel data from the database
@app.route('/data/book1')
def get_data():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT filedata FROM files WHERE name = 'excel' AND filename = 'Book1.xlsx'"
    cursor.execute(query)
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    
    if result:
        excel_data = BytesIO(result['filedata'])
        try:
            df = pd.read_excel(excel_data)
            data = df.to_dict(orient='records')
            return jsonify(data)
        except Exception as e:
            return jsonify({'error': f'Error processing Excel file: {str(e)}'}), 500
    else:
        return jsonify({'error': 'File not found'}), 404

# Route for serving certificate files from the database
@app.route('/data/<path:filename>')
def data(filename):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT filedata FROM files WHERE filename = %s AND name = 'certificate'"
    cursor.execute(query, (filename,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    
    if result:
        file_data = BytesIO(result['filedata'])
        return send_file(file_data, as_attachment=True, attachment_filename=filename)
    else:
        return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
