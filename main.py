import os
import cv2
import time
import vertexai
from vertexai.generative_models import GenerativeModel, Part
from flask import Flask, send_from_directory

app = Flask('ParkMaster')

def read_license_plate(image_path):
	vertexai.init(project=project_id, location="us-central1")

  model = GenerativeModel("gemini-1.5-flash-001")

  image_file_uri = f'caps/numplate.jpg'
  image_file = Part.from_uri(image_file_uri, mime_type="image/png")

  prompt = "you are an ocr, extract text"

  contents = [
      image_file,
      prompt,
  ]

  response = model.generate_content(contents)
  plate_text = response.text

    return plate_text

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
