import boto3
import uuid
import os
import json

def lambda_handler(event, context):
    try:
        # Entrada
        tenant_id = event['body']['tenant_id']
        pelicula_datos = event['body']['pelicula_datos']
        nombre_tabla = os.environ["TABLE_NAME"]
        
        # Proceso
        uuidv4 = str(uuid.uuid4())
        pelicula = {
            'tenant_id': tenant_id,
            'uuid': uuidv4,
            'pelicula_datos': pelicula_datos
        }
        
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(nombre_tabla)
        response = table.put_item(Item=pelicula)
        
        # Generar log estandarizado para ejecución exitosa
        log_info = {
            "tipo": "INFO",
            "log_datos": pelicula
        }
        print(json.dumps(log_info)) # Imprime el JSON en CloudWatch
        
        # Salida
        return {
            'statusCode': 200,
            'pelicula': pelicula,
            'response': response
        }
        
    except Exception as e:
        # Generar log estandarizado para errores
        log_error = {
            "tipo": "ERROR",
            "log_datos": {
                "mensaje_error": str(e),
                "evento_recibido": event
            }
        }
        print(json.dumps(log_error)) # Imprime el JSON de error en CloudWatch
        
        return {
            'statusCode': 500,
            'mensaje': 'Ocurrió un error al procesar la solicitud',
            'error': str(e)
        }