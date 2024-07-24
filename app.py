from flask import Flask, request, send_file, render_template
from io import BytesIO
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import zipfile

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/PKL_web')
def web_pkl():
    return render_template('PKL_web.html')

@app.route('/generate-certificates', methods=['POST'])
def generate_certificates():
    file = request.files['excel']
    df = pd.read_excel(file)
    df = pd.read_excel(file, engine='openpyxl')
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
        
        certificates.append(buffer)

    # Create a ZIP file containing all certificates
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        for idx, cert_buffer in enumerate(certificates):
            zip_file.writestr(f'certificate_{idx + 1}.png', cert_buffer.getvalue())
    zip_buffer.seek(0)

    return send_file(zip_buffer, mimetype='application/zip', download_name='certificates.zip', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
