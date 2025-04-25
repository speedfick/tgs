import time
import random
from datetime import datetime
import requests
import json
from faker import Faker

fake = Faker('pt_PT')

# Configuração da API
API_URL = "http://api:5000"

def generate_reading(id_utente):
    """Gera uma leitura simulada para um paciente."""
    now = datetime.now()
    
    # Gerar valores aleatórios para os sinais vitais
    temperatura = round(random.uniform(35.5, 38.5), 1)
    batimento = random.randint(60, 100)
    oxigenio = random.randint(95, 100)
    pulsacao = random.randint(60, 100)
    
    return {
        "id_utente": id_utente,
        "timestamp": now.isoformat(),
        "temperatura": temperatura,
        "batimento_cardiaco": batimento,
        "oxigenio": oxigenio,
        "pulsacao": pulsacao
    }

def send_readings_to_api(readings):
    """Envia as leituras para a API de uma vez."""
    try:
        response = requests.post(
            f"{API_URL}/api/sensor-readings",
            data=json.dumps({"readings":readings}),
            headers={'Content-Type': 'application/json'}
        )
        if response.status_code == 200:
            print("Leituras enviadas com sucesso!")
        else:
            print(f"Erro ao enviar leituras: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Erro na comunicação com a API: {e}")

def main():
    # Lista de IDs de pacientes para simular
    patient_ids = list(range(1, 21))  # 20 pacientes
    
    print("Iniciando simulação de sensores...")
    
    while True:
        # Gerar e criar a lista de leituras para todos os pacientes
        readings = [generate_reading(patient_id) for patient_id in patient_ids]
        
        # Enviar todas as leituras para a API em uma única solicitação
        send_readings_to_api(readings)
        
        # Aguardar antes da próxima rodada de leituras
        time.sleep(5)

if __name__ == "__main__":
    main()
