import pickle
import os, math, random, datetime
import boto3

# Configurar las credenciales de acceso
ACCESS_KEY = 'AKIA2JHUK4EGBAMYAYFY'
SECRET_KEY = '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'
DATASET_PATH = 's3://anyoneai-datasets/queplan_insurance/'

# Crear una conexión al servicio S3
s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)


# Descargar el archivo desde S3
BUCKET_NAME = "anyoneai-datasets"
prefix = "queplan_insurance/"

# Listar objetos en el directorio
response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=prefix)

# Imprimir los nombres de los objetos
for obj in response['Contents']:
    print(obj['Key'])

with open('queplan_insurance.pkl', 'wb') as f:
    # s3.download_fileobj(BUCKET_NAME, prefix + "queplan_insurance.pkl", f)
    pickle.dump(response, f)    

# def download_pdf_from_s3(bucket_name, s3_file_name, local_file_name):
#     s3.download_file(bucket_name, s3_file_name, local_file_name)

# # Uso de la función
# download_pdf_from_s3('my_bucket', 'path/to/myfile.pdf', 'myfile.pdf')