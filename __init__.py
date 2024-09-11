from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from flask import jsonify
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)                                                                                                                  
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html') #Comm2
  
@app.route("/contact/")
def MaPremiereAPI():
     return render_template("contact.html")

@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def monhistogramme():
    return render_template("histogramme.html")

@app.route('/commits/')
def show_commits():
    url = 'https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits'
    response = requests.get(url)
    commits_data = response.json()
    commits_minutes = []

    for commit in commits_data:
        commit_date = commit['commit']['author']['date']
        # Appelle la fonction extract_minutes pour récupérer les minutes
        minutes = extract_minutes(commit_date)
        commits_minutes.append(minutes.get_json()['minutes'])  # Convertir en JSON et extraire les minutes
    
    return jsonify(commits_minutes=commits_minutes)

@app.route('/commits_graphique/')
def commits_graphique():
    return render_template('commits_graphique.html')


@app.route('/extract-minutes/<date_string>')
def extract_minutes(date_string):
        date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
        minutes = date_object.minute
        return jsonify({'minutes': minutes})

if __name__ == "__main__":
  app.run(debug=True)
