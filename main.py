import os
from flask import Flask, send_file

app = Flask('ParkMaster')

@app.route('/')
def root():
	return '<h1>Welcome to Park Master!</h1>'

@app.route('/capture')
def capture():
	os.system('raspistill -o caps/cap.png')
	return send_file('caps/cap.png')
