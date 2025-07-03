import requests
from flask import Flask, render_template, request, redirect, flash, url_for, session
app = Flask(__name__)
app.secret_key = 'q92fj!f0f9a#q0v@d1f' #this is need for the session in lines 13,14 cuz flask encrypts to verify data integrity
API_KEY = '42cde0c47c9e6b1e75515d281cc65587'

#api_url = 'https://api.openweathermap.org/data/2.5/weather?zip={zip code},{country code}&appid={API_KEY}'
@app.route('/', methods=['GET','POST'])
@app.route('/dashboard', methods=['GET','POST'])
def dashboard():
    if request.method == "POST":
        zip_code = request.form['zip_code']
        country_code = request.form['country_code']
        session['zip_code'] = zip_code
        session['country_code'] = country_code
        return redirect(url_for('results'))
    return render_template('dashboard.html')
    
    #response = requests.get(api_url)

@app.route('/results')
def results():
    zip_code = session.get('zip_code')
    country_code = session.get('country_code')
    if not zip_code or not country_code:
        return redirect(url_for('dashboard'))
    response = requests.get('https://api.openweathermap.org/data/2.5/weather?zip='+zip_code+','+country_code+'&appid='+API_KEY)

    weather_data = response.json()
    return render_template('results.html', data=weather_data, zipcode=zip_code, countrycode=country_code)