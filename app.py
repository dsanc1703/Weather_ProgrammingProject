import requests, os
from flask import Flask, render_template, request, redirect, flash, url_for, session
app = Flask(__name__)
app.secret_key = os.urandom(24) #this is need for the session in lines 13,14 cuz flask encrypts to verify data integrity
API_KEY = '42cde0c47c9e6b1e75515d281cc65587'

#api_url = 'https://api.openweathermap.org/data/2.5/weather?zip={zip code},{country code}&appid={API_KEY}'

users = []

@app.before_request
def loginauthentication():
    protected_sites = ['zipcode','dashboard','results']
    if request.endpoint in protected_sites and not session.get('logged_in'):
        return redirect(url_for('login'))

@app.route('/zipcode', methods=['GET','POST'])
def zipcode():
    if request.method == "POST":
        zip_code = request.form['zip_code']
        country_code = request.form['country_code']
        session['zip_code'] = zip_code
        session['country_code'] = country_code
        return redirect(url_for('results'))
    return render_template('zipcode.html')

@app.route('/results', methods=['GET'])
def results():
    zip_code = session.get('zip_code')
    country_code = session.get('country_code')
    print("Fetching weather data")
    response = requests.get(
        f'https://api.openweathermap.org/data/2.5/weather?zip={zip_code},{country_code}&appid={API_KEY}'
    )
    weather_data = response.json()
    return render_template('results.html', data=weather_data, zipcode=zip_code, countrycode=country_code)


@app.route('/', methods=['GET', 'POST'])
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        users.append({'username': username, 'password': password})
        flash("Successfully created account!")
        return redirect(url_for('login'))
    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        for user in users:
            if user['username'] == username and user['password'] == password:
                session['logged_in'] = True
                return redirect(url_for('zipcode'))
        flash("Invalid Username or Password")
    return render_template('login.html')


@app.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard.html')