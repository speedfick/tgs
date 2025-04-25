from flask import Flask, render_template, jsonify
from flask_cors import CORS
import requests
from datetime import datetime, timedelta
app = Flask(__name__)
CORS(app)

@app.route('/')
def dashboard():
    return render_template('dashboard.html')


@app.route('/patient/<int:id>/details')
def graficos(id):
    try:
        response = requests.get(f'http://api:5000/api/patient/{id}/details')
        response.raise_for_status()
        patient_data = response.json()
        print(jsonify(patient_data))
        # Convert the data to JavaScript-friendly format
        return render_template('patientDetails.html', 
                             patient_data=patient_data)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500



@app.route('/leituras', methods=['GET'])
def latest_readings():
    try:
        cutoff_time = (datetime.now() - timedelta(seconds=60)).strftime("%Y-%m-%dT%H:%M:%S.%f")
        cuttof={
            'cutoff_time':cutoff_time
        }
        
        # Faz uma requisição ao endpoint externo
        response = requests.get('http://api:5000/api/latest-readings',cuttof)
        response.raise_for_status()  # Levanta um erro se a requisição falhar
        data = response.json()  # Extrai os dados JSON da resposta
    except requests.exceptions.RequestException as e:
        # Trata possíveis erros da requisição
        return jsonify({"error": str(e)}), 500

    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
