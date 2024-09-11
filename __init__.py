from flask import Flask, render_template, jsonify
from datetime import datetime
from urllib.request import urlopen
import json
import requests

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route("/contact/")
def contact():
    return render_template("contact.html")

@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15  # Conversion de Kelvin en °C
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def monhistogramme():
    return render_template("histogramme.html")

# Route pour afficher les commits et leur distribution minute par minute
@app.route('/commits/')
def show_commits():
    url = 'https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits'
    response = requests.get(url)
    commits_data = response.json()
    commits_by_minute = {}

    # Extraire les minutes des dates de commits
    for commit in commits_data:
        commit_date = commit['commit']['author']['date']
        minutes = datetime.strptime(commit_date, '%Y-%m-%dT%H:%M:%SZ').minute

        # Compter les commits par minute
        if minutes in commits_by_minute:
            commits_by_minute[minutes] += 1
        else:
            commits_by_minute[minutes] = 1

    # Préparer les données sous forme de tableau pour le graphique
    chart_data = [[minute, count] for minute, count in sorted(commits_by_minute.items())]

    return render_template('commits_graphique.html', chart_data=chart_data)

# Route pour afficher le graphique des commits
@app.route('/commits_graphique/')
def commits_graphique():
    return render_template('commits_graphique.html')

# Route pour extraire les minutes d'une date
@app.route('/extract-minutes/<date_string>')
def extract_minutes(date_string):
    date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
    minutes = date_object.minute
    return jsonify({'minutes': minutes})

if __name__ == "__main__":
    app.run(debug=True)
