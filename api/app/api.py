from flask import Flask, jsonify, request
import polars as pl
from datetime import datetime, timedelta
from deltalake import DeltaTable

app = Flask(__name__)


storage_options = {
    "AWS_ACCESS_KEY_ID": "minioadmin",
    "AWS_SECRET_ACCESS_KEY": "minioadmin",
    "AWS_ENDPOINT_URL": "http://minio:9000",
    "AWS_ALLOW_HTTP": "true",
    "AWS_S3_ALLOW_UNSAFE_RENAME": "true",
    "AWS_EC2_METADATA_DISABLED": "true"
}

@app.route('/api/latest-readings', methods=['GET'])
def get_latest_readings():
    cutoff_time = request.args.get('cutoff_time')
    print("isto é cutof999999", cutoff_time)
    try:
        table_path = "s3://patients/health_readings"
        dt = DeltaTable(table_path, storage_options=storage_options)
        health_readings = (pl.DataFrame(dt.to_pyarrow_table())
            .with_columns(pl.col("timestamp").str.to_datetime("%Y-%m-%dT%H:%M:%S.%f").alias("timestamp"))  # Converte o timestamp de string para datetime
            .filter(pl.col("timestamp") >= pl.lit(cutoff_time).str.to_datetime("%Y-%m-%dT%H:%M:%S.%f"))  # Aplica o filtro de cutoff
            .sort(by="timestamp", descending=True)
            .unique(subset=["id_utente"], keep="first"))
        
        table_path = "s3://patients/patients_data"
        dt = DeltaTable(table_path, storage_options=storage_options)
        patients_data =pl.DataFrame(dt.to_pyarrow_table())

        table_path = "s3://patients/patient_status"
        dt = DeltaTable(table_path, storage_options=storage_options)
        patients_status = pl.DataFrame(dt.to_pyarrow_table())

        result = health_readings.join(patients_data, left_on="id_utente", right_on="id", how="full")
        result = result.join(patients_status, on="id_utente", how="full") 
        return jsonify(result.to_dicts())

    except Exception as e:
        import traceback
        app.logger.error(f"API Error: {str(e)}")
        app.logger.debug(traceback.format_exc())
        return jsonify({"error": str(e)}), 500


@app.route('/api/sensor-readings', methods=['POST'])
def add_sensor_reading():
    try:
        # Recebe o JSON do request
        data = request.json        
        # Converte o JSON para um DataFrame do Polars
        dt = pl.DataFrame(data['readings'])
        
        # Caminho da tabela Delta no S3
        table_path = "s3://patients/health_readings"
        
        dt.write_delta(
            table_path,
            storage_options=storage_options,
            mode="append"
        )
        
        # Retorna uma resposta de sucesso
        return jsonify({"status": "success", "message": "Reading added successfully"})
    except Exception as e:
        # Loga o erro e retorna uma resposta de erro
        app.logger.error(f"Error adding reading: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# New routes to fetch data from specific DeltaTables
@app.route('/api/health-readings')
def get_health_readings():
    try:
        cutoff_time = (datetime.now() - timedelta(hours=24)).strftime("%Y-%m-%dT%H:%M:%S.%f")
        table_path = "s3://patients/health_readings"
        dt = DeltaTable(table_path, storage_options=storage_options)
        data = (pl.DataFrame(dt.to_pyarrow_table())
            .with_columns(pl.col("timestamp").str.to_datetime("%Y-%m-%dT%H:%M:%S.%f").alias("timestamp"))  # Converte o timestamp de string para datetime
            .filter(pl.col("timestamp") >= pl.lit(cutoff_time).str.to_datetime("%Y-%m-%dT%H:%M:%S.%f"))  # Aplica o filtro de cutoff
            .sort(by="timestamp", descending=True)
            .unique(subset=["id_utente"], keep="first"))
        return jsonify(data.to_dicts())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/patients-data')
def get_patients_data():
    try:
        table_path = "s3://patients/patients_data"
        dt = DeltaTable(table_path, storage_options=storage_options)
        data = (pl.DataFrame(dt.to_pyarrow_table())
            .with_columns(pl.col("created_at").str.to_datetime("%Y-%m-%dT%H:%M:%S.%f").alias("timestamp")))
        return jsonify(data.to_dicts())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/patients-status')
def get_patients_status():
    try:
        table_path = "s3://patients/patient_status"
        dt = DeltaTable(table_path, storage_options=storage_options)
        data = pl.DataFrame(dt.to_pyarrow_table())
        return jsonify(data.to_dicts())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/patient/<int:patient_id>/details')
def get_patient_details(patient_id):
    try:
        # Fetch last 24 hours of readings for this patient
        cutoff_time = (datetime.now() - timedelta(hours=24)).strftime("%Y-%m-%dT%H:%M:%S.%f")
        
        # Get health readings
        table_path = "s3://patients/health_readings"
        dt = DeltaTable(table_path, storage_options=storage_options)
        health_readings = (pl.DataFrame(dt.to_pyarrow_table())
            .filter(pl.col("id_utente") == patient_id)
            .with_columns(pl.col("timestamp").str.to_datetime("%Y-%m-%dT%H:%M:%S.%f"))
            .filter(pl.col("timestamp") >= pl.lit(cutoff_time).str.to_datetime("%Y-%m-%dT%H:%M:%S.%f"))
            .sort("timestamp")
        )
        health_readings = health_readings.with_columns(
            pl.col("timestamp").dt.strftime("%H:%M").alias("timestamp")
        )
        # Get patient name from patients_data
        table_path = "s3://patients/patients_data"
        dt = DeltaTable(table_path, storage_options=storage_options)
        patients_data = pl.DataFrame(dt.to_pyarrow_table())
        table_path = "s3://patients/patient_status"
        dt = DeltaTable(table_path, storage_options=storage_options)
        patients_status = pl.DataFrame(dt.to_pyarrow_table())

        result = patients_data.join(patients_status, left_on="id", right_on="id_utente", how="full")
        # Find the patient by ID
        patient_info = result.filter(pl.col("id") == patient_id).select(["nome", "cama", "quarto", "setor", "unidade"]).to_dicts()
        
        # Combine health readings and patient name
        patient_info = patient_info[0]

        return jsonify({
            "patient_info": patient_info,
            "readings": health_readings.to_dicts()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
