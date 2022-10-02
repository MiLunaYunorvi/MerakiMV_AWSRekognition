import boto3
from meraki import snapshot,webex, formato_webex
from meraki import collect_name
from time import sleep
import json
import requests

client=boto3.client('rekognition')
global estado


def delete_faces(lista):
    try:
        client=boto3.client('rekognition')
        response = client.delete_faces(
        CollectionId=collect_name,
        FaceIds= lista)
        print("Borrado exitoso")
    except:
        pass
    
def listar_faces():
    client=boto3.client('rekognition')
    response = client.list_faces(
        CollectionId= collect_name,
        MaxResults=10)
    print(response['Faces'])
    for i in response['Faces']:
        print ( "FaceId: ", i['FaceId'], "   corresponde a: ", i['ExternalImageId']) 
        
def open_image(url):
    global estado
    sleep(0.5)
    #urllib.request.urlretrieve(url,'imagen.png')
    response = requests.get(url)
    if str(response) == '<Response [200]>':
        bytes = response.content
        print('IMAGEN CARGADA, PASANDO BYTES A REKOGNITION')
        index_faces(bytes)
    else:
        estado = 'Error en el snapshot'
        print("error de snapshot")
        pass

def search_faces(bytes):
    global estado
    client=boto3.client('rekognition')
    threshold = 40
    try:
        response=client.search_faces_by_image(CollectionId=collect_name,
                                    Image={'Bytes': bytes},
                                    FaceMatchThreshold=threshold,
                                    MaxFaces= 3)
        print(response)
        if response['FaceMatches'] != []:
        #print(response)
            faceMatches=response['FaceMatches']
            print ('Matching faces')
            for match in faceMatches:
                    persona = match['Face']['ExternalImageId']
                    print ('FaceId:' + match['Face']['ExternalImageId'])
                    print ('Similarity: ' + "{:.2f}".format(match['Similarity']) + "%")
        else:
            persona = "NO DETECTO A NADIE"
        webex(persona)
    except:
        estado = 'No se encontraron rostros en la imagen'


def search_faces_by_id(listaIds):
    global estado
    client=boto3.client('rekognition')
    print("BUSCANDO MATCH PARA LOS ROSTROS ENCONTRADOS: ")
    personas = []
    desconocidos = 0
    if listaIds != []:
        for id in listaIds:
            response = client.search_faces(CollectionId=collect_name,FaceId=id, MaxFaces=1, FaceMatchThreshold=60)
            if response['FaceMatches'] != []:    
                faceMatched = response['FaceMatches'][0]['Face']['ExternalImageId']
                similarity = response['FaceMatches'][0]['Similarity']
                personas.append([faceMatched, similarity])
                print(faceMatched,similarity)
                estado = "Se encontró similitud"
            else:
                desconocidos= desconocidos+1
        if personas != []:
            print("DE {} PERSONAS SE RECONOCIÓ A LAS SIGUIENTES: ".format(str(len(listaIds))))
            mensaje_f = formato_webex(personas)
            webex(mensaje_f)
        else:
            estado = "Index detectó rostros, pero no hay match con alguno"
            print("NO SE ENCONTRÓ NINGÚN MATCH")
            webex("Se detectaron rostros desconocidos, no hay similitud en la base de datos.")
    delete_faces(listaIds)
    return personas                           

def index_faces(bytes): 
    global estado
    client=boto3.client('rekognition')
    print("BUSCANDO ROSTROS CON INDEX_FACES")
    face_id_list = [] 
    response = client.index_faces(CollectionId=collect_name, Image = {'Bytes': bytes}, ExternalImageId='grupales', DetectionAttributes=['DEFAULT'], MaxFaces=5, QualityFilter='MEDIUM') 
    print('index ',response)
    FaceRecords = response['FaceRecords']
    if FaceRecords != []:
        estado = "Se encontraron rostros"
        for i in FaceRecords:
            face_id = i['Face']['FaceId']
            face_id_list.append(face_id)
        print(face_id_list)
        search_faces_by_id(face_id_list)
    else:
        print("No se detectaron rostros")
        estado = "No hay rostros en la imagen"
        delete_faces(face_id_list)

def lambda_handler(event, context):
    global estado
    url_imagen = snapshot()
    open_image(url_imagen)
    mensaje = {'estado: ': estado, 'url_snapshot: ': url_imagen}
    return {
        'statusCode': 200,
        'body': json.dumps(mensaje)}

