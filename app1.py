from flask import Flask, request, render_template
from io import BytesIO
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import zipfile
from app2 import insert_file_to_db

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-certificates', methods=['POST'])
def generate_certificates():
    # Get the uploaded Excel file
    file = request.files['excel']
    
    # Save Excel file to a buffer
    excel_buffer = BytesIO()
    file.save(excel_buffer)
    excel_buffer.seek(0)
    
    # Upload the Excel file to the database
    insert_file_to_db(excel_buffer.getvalue(), file.filename, 'excel')
    
    df = pd.read_excel(excel_buffer)
    certificates = []

    for name in df['Name']:  # Assuming the column with names is labeled 'Name'
        img = Image.open("static/images.png")  # Path to the uploaded certificate template
        draw = ImageDraw.Draw(img)
        
        # Define the font and size
        font = ImageFont.truetype("arial.ttf", 80)  # Adjust the font path and size as needed
        
        # Calculate text position
        text_bbox = font.getbbox(name)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        x = (img.width - text_width) / 2
        y = 740 # Adjust this value based on where you want the name to appear
        
        # Add text to image
        draw.text((x, y), name, font=font, fill="black")
        
        # Save to buffer
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        
        certificates.append((buffer.getvalue(), f'certificate_{name}.png'))
    
    # Upload each certificate to the database
    for cert_data, cert_name in certificates:
        insert_file_to_db(cert_data, cert_name, 'certificate')

    return "Certificates generated and uploaded to the database."

if __name__ == '__main__':
    app.run(debug=True)
