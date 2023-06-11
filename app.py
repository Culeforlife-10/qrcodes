from flask import Flask, render_template, request
import qrcode
from io import BytesIO
import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
import os
from PIL import Image
from PIL import ImageDraw
app = Flask(__name__)

def remove(string):
    return string.replace(" ", "")


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_qrcode', methods=['GET', 'POST'])
def generate_qrcode():
    if request.method == 'POST':
        name = request.form['name']
        club_name = request.form['club_name']
        zone = request.form['zone']
        meal_type = request.form['meal_type']
        name=remove(name)
        print(name)
        data = f'{name},{club_name},{zone},{meal_type}'
        print(data)

        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        qrcode_img = qr.make_image()
        zones=os.listdir('static/')
        print(zones)
        if zone in zones:
            clubs=os.listdir(f'static/{zone}')
            if club_name in clubs:
                qrcode_img.save(f"static/{zone}/{club_name}/{club_name}_{name}_{zone}.png")
                img = Image.open(f"static/{zone}/{club_name}/{club_name}_{name}_{zone}.png")
                I1 = ImageDraw.Draw(img)
                I1.text((10, 10), f"{club_name}_{name}", fill=0)
                img.save(f"static/{zone}/{club_name}/{club_name}_{name}_{zone}.png")
            else:
                os.mkdir(f'static/{zone}/{club_name}')
                qrcode_img.save(f"static/{zone}/{club_name}/{club_name}_{name}_{zone}.png")
                qrcode_img.save(f"static/{zone}/{club_name}/{club_name}_{name}_{zone}.png")
                img = Image.open(f"static/{zone}/{club_name}/{club_name}_{name}_{zone}.png")
                I1 = ImageDraw.Draw(img)
                I1.text((10, 10), f"{club_name}_{name}", fill=0)
                img.save(f"static/{zone}/{club_name}/{club_name}_{name}_{zone}.png")
        else: 
            if zone not in zones:
                os.mkdir(f'static/{zone}')
                os.mkdir(f'static/{zone}/{club_name}')
                qrcode_img.save(f"static/{zone}/{club_name}/{club_name}_{name}_{zone}.png")
                qrcode_img.save(f"static/{zone}/{club_name}/{club_name}_{name}_{zone}.png")
                img = Image.open(f"static/{zone}/{club_name}/{club_name}_{name}_{zone}.png")
                I1 = ImageDraw.Draw(img)
                I1.text((10, 10), f"{club_name}_{name}", fill=0)
                img.save(f"static/{zone}/{club_name}/{club_name}_{name}_{zone}.png")

        return render_template('qrcode.html', qr_data=data, qr_image=f'{zone}/{club_name}/{club_name}_{name}_{zone}.png')

    return render_template('generate_qrcode.html')

@app.route('/upload_qrcode', methods=['GET', 'POST'])
def upload_qrcode():
    if request.method == 'POST':
        qr_code = request.files['qr_code']
        qr_code_img = cv2.imdecode(np.fromstring(qr_code.read(), np.uint8), cv2.IMREAD_UNCHANGED)

        decoded_qr_codes = pyzbar.decode(qr_code_img)
        if decoded_qr_codes:
            qr_data = decoded_qr_codes[0].data.decode('utf-8')
            qr_data_list = qr_data.split(',')
            name = qr_data_list[0]
            club_name = qr_data_list[1]
            zone = qr_data_list[2]
            meal_type = qr_data_list[3]
            print(qr_data_list)

            return render_template('qrcode_details.html', name=name, club_name=club_name, zone=zone, meal_type=meal_type)

    return render_template('upload_qrcode.html')

@app.route('/scan_qrcode',methods=['GET','POST'])
def scan_qrcode():
    if request.method=='POST':
        name=request.values.get('name')
        clubName=request.values.get('clubName')
        zone=request.values.get('zone')
        meal_type=request.values.get('meal_type')
        print(name,clubName,zone,meal_type)
    return render_template('scan_qrcode1.html')

if __name__ == '__main__':
    app.run()
