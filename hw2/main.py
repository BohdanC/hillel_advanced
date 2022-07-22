from flask import Flask

import random
import string
import pandas as pd


app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/random_password")
def generate_password():
    n = random.randint(10,20)
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(n))
    return password



@app.route("/avr_data")
def get_avr_data():
    data = pd.read_csv('hw.csv')
    avr_h = data[' Height(Inches)'].mean()
    avr_w = data[' Weight(Pounds)'].mean()
    return f'Середній ріст: {str(round(avr_h, 3))}</br>Середня вага: {str(round(avr_w, 3))}'


app.run(debug=True)