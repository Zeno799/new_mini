import os
import cv2
import time
import pytesseract
from flask import Flask, send_from_directory

app = Flask('ParkMaster')

pytesseract.pytesseract.tesseract_cmd = f'/usr/bin/tesseract-ocr'

def read_license_plate(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print("Error: Image not loaded correctly.")
        return None

    blurred = cv2.GaussianBlur(img, (5, 5), 0)
    _, binary_image = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    custom_config = r'--oem 3 --psm 6'
    plate_text = pytesseract.image_to_string(binary_image, config=custom_config)

    plate_text = ''.join(e for e in plate_text if e.isalnum())

    print(f"Detected License Plate Text: {plate_text}")

    # cv2.imshow("Original Image", img)
    # cv2.imshow("Processed Image", binary_image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    return plate_text

plate_times = {}

@app.route('/')
def root():
	return '<h1>Welcome to Park Master!</h1>'

@app.route('/capture')
def capture():
    os.system('raspistill -o caps/numplate.jpg')  # uncomment this to run on the raspi
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
