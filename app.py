from flask import Flask, render_template, request, redirect, flash, url_for

app = Flask(__name__)

api_key = "api-key"

@app.route('/', methods=['GET','POST'])
def dashboard():
    if request.method == "POST":
        city = request.form['city']
        session['city'] = city
        return render_template('dashboard.html')
    
    response = requests.get(api_key)