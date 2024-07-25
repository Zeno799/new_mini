import os
import cv2
import time
import vertexai
from vertexai.generative_models import GenerativeModel, Part
from flask import Flask, send_from_directory

app = Flask('ParkMaster')

def read_license_plate(image_path):
    genai.configure(api_key="AIzaSyD2-qNoo3rOhdnYkfkZl0n_GeaD3eGS6lc")

    model = genai.GenerativeModel('gemini-1.5-flash')
    sample_file = genai.upload_file(path=image_path,display_name="plate")
    file = genai.get_file(name=sample_file.name)

    response = model.generate_content(["pls read text from image", file ], stream=True)
    response.resolve()
    return response.text

plate_times = {}

@app.route('/')
def root():
	return '<h1>Welcome to Park Master!</h1>'

@app.route('/capture')
def capture():
    os.system('libcamera-jpeg -o caps/numplate.jpg')  # uncomment this to run on the raspi
    license_plate = read_license_plate(f"caps/numplate.jpg")
    os.rename('caps/numplate.jpg', f'caps/{license_plate}.jpg')
    result = f'<div><p>PLATE TEXT: {license_plate}</p></div>'
    if license_plate in plate_times:
        os.remove(f'caps/{license_plate}.jpg')
        result += f'<div><p>PLATE LAST SEEN: {time.time() - plate_times[license_plate]} seconds ago</p></div>'
    else:
        plate_times[license_plate] = time.time()
        result += f'<img src="/caps/{license_plate}.jpg">'
    return result

@app.route('/caps/<path:path>')
def fs_access(path):
    return send_from_directory('caps', path)
