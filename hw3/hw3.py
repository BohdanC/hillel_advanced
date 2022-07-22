from flask import Flask, render_template, Response
from faker import Faker
from webargs.flaskparser import use_kwargs
import requests
import random
import string
import csv
import pandas as pd

from data_validation import student_args, bitcoin_rate_args
from forex_python.converter import CurrencyCodes


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


@app.route("/students")
@use_kwargs(student_args, location='query')
def generate_students(count):
    csv_columns = ['Name','Surname','Email','Password','Birthdate']
    csv_file = "students.csv"

    data = []
    student = {}
    fake = Faker()
    for i in range(count):
        student = dict(
            Name=fake.first_name(),
            Surname=fake.last_name(),
            Password=fake.password(),
            Birthdate=fake.date_of_birth(minimum_age=17, maximum_age=40)
        )
        student.update(Email=student['Name'].lower() + "." + student['Surname'].lower() + "@gmail.com")
        data.append(student)


    with open (csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile,fieldnames=csv_columns)
        writer.writeheader()
        for i in data:
            writer.writerow(i)

    df = pd.read_csv('students.csv')
    return df.to_html(header='true')

    # count should be as input GET parameter
    # first_name, last_name, email, password, birthday
    # save to csv and show on web page
    # set limit as 1000


@app.route("/bitcoin_rate")
@use_kwargs(bitcoin_rate_args, location="query")
def get_bitcoin_rate(currency):
    url = 'https://bitpay.com/api/rates'
    res = requests.get(url)
    if res.status_code != 200:
        return Response('ERROR: smthing went wrong', status=res.status_code)
    result = res.json()
    value = None
    for item in result:
        if item['code'] == currency:
            value = item['rate']
            break
    return f'BTC value in {currency} = {str(value)} {CurrencyCodes().get_symbol(currency)}'
    # https://bitpay.com/api/rates
    # /bitcoin_rate?currency=UAH
    # input parameter currency code
    # default is USD
    # return value currency of bitcoin
    # * https://bitpay.com/api/
    # * return symbol of input currency code
    # * add one more input parameter count and multiply by currency (int)



app.run(debug=True)