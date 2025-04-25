import random
from datetime import datetime, timedelta
import polars as pl
from faker import Faker
import os
import json
from minio import Minio
from minio.error import S3Error

# Initialize Faker for generating realistic fake data
fake = Faker('pt_PT')

# MinIO client configuration
minio_client = Minio(
    "localhost:9000",
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=False
)

# Storage options for Delta Lake with MinIO
storage_options = {
    "AWS_ACCESS_KEY_ID": "minioadmin",
    "AWS_SECRET_ACCESS_KEY": "minioadmin",
    "AWS_ENDPOINT_URL": "http://localhost:9000",
    "AWS_ALLOW_HTTP": "true",
    "AWS_S3_ALLOW_UNSAFE_RENAME": "true",
    "AWS_EC2_METADATA_DISABLED": "true"
}

def ensure_bucket_exists(bucket_name="patients"):
    try:
        if not minio_client.bucket_exists(bucket_name):
            print(f"Creating bucket '{bucket_name}'...")
            minio_client.make_bucket(bucket_name)
            
            # Definir política de acesso público ao bucket
            policy = {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Principal": {"AWS": "*"},
                        "Action": ["s3:GetBucketLocation", "s3:ListBucket", "s3:ListBucketMultipartUploads"],
                        "Resource": [f"arn:aws:s3:::{bucket_name}"]
                    },
                    {
                        "Effect": "Allow",
                        "Principal": {"AWS": "*"},
                        "Action": ["s3:GetObject", "s3:PutObject", "s3:DeleteObject", "s3:AbortMultipartUpload", "s3:ListMultipartUploadParts"],
                        "Resource": [f"arn:aws:s3:::{bucket_name}/*"]
                    }
                ]
            }
            minio_client.set_bucket_policy(bucket_name, json.dumps(policy))
            print(f"Bucket '{bucket_name}' created and configured successfully")
        else:
            print(f"Bucket '{bucket_name}' already exists")
    except Exception as e:
        print(f"Error with bucket operations: {e}")
        raise

def generate_patient_data(num_patients=10):
    # Listas para armazenar os dados
    ids = []
    nomes = []
    generos = []
    datas_nascimento = []
    tipos_sanguineos = []
    pesos = []
    alturas = []
    telefones = []
    enderecos = []
    created_ats = []

    for i in range(num_patients):
        # Primeiro definimos o gênero
        genero = random.choice(['M', 'F'])
        
        # Geramos o nome apropriado baseado no gênero
        if genero == 'M':
            nome = fake.name_male()
        else:
            nome = fake.name_female()
        
        # Adicionamos os dados às listas
        ids.append(i + 1)
        nomes.append(nome)
        generos.append(genero)
        datas_nascimento.append(fake.date_of_birth(minimum_age=18, maximum_age=90).strftime('%Y-%m-%d'))
        tipos_sanguineos.append(random.choice(['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-']))
        pesos.append(round(random.uniform(45.0, 120.0), 2))
        alturas.append(round(random.uniform(1.50, 2.00), 2))
        telefones.append(fake.phone_number())
        enderecos.append(fake.address().replace('\n', ', '))
        created_ats.append(datetime.now().isoformat())

    data = {
        'id': ids,
        'nome': nomes,
        'genero': generos,
        'data_nascimento': datas_nascimento,
        'tipo_sanguineo': tipos_sanguineos,
        'peso': pesos,
        'altura': alturas,
        'telefone': telefones,
        'endereco': enderecos,
        'created_at': created_ats
    }
    
    return pl.DataFrame(data)

def generate_patient_status(num_patients=20):
    data = {
        'id_utente': list(range(1, num_patients + 1)),
        'unidade': [random.choice(['Cardiologia', 'Cuidados Intensivos', 'Medicina Interna']) for _ in range(num_patients)],
        'setor': [random.choice(['A', 'B', 'C']) for _ in range(num_patients)],
        'quarto': [random.randint(1, 10) for _ in range(num_patients)],
        'cama': [random.randint(1, 4) for _ in range(num_patients)],
        'data_hora': [datetime.now().isoformat() for _ in range(num_patients)]
    }
    return pl.DataFrame(data)

def save_to_delta(df, table_path):
    try:
        # Adiciona novos dados à tabela existente ou cria uma nova
        df.write_delta(
            table_path,
            mode="append",
            storage_options=storage_options
        )
        print(f"Successfully saved data to Delta table at '{table_path}'")
    except Exception as e:
        print(f"Error saving to Delta table: {e}")

def main():
    try:
        # Ensure bucket exists before proceeding
        ensure_bucket_exists()

        # Generate patient data
        patients_df = generate_patient_data(num_patients=20)
        status_df = generate_patient_status(num_patients=20)
        print("patneicnte:", patients_df)
        print("status:", status_df)
        # Save to Delta tables
        save_to_delta(patients_df, "s3://patients/patients_data")
        save_to_delta(status_df, "s3://patients/patient_status")
        
        print("Patient data generation completed successfully")
    except Exception as e:
        print(f"Error in main execution: {e}")

if __name__ == "__main__":
    main()
