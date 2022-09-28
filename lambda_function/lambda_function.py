import boto3
from meraki import snapshot,webex
from time import sleep
import json
import requests


client=boto3.client('rekognition')

global estado

def delete_faces(lista):
    client=boto3.client('rekognition')
    response = client.delete_faces(
    CollectionId='First_collection',
    FaceIds= lista)
    print("Borrado exitoso")
    
def listar_faces():
    client=boto3.client('rekognition')
    response = client.list_faces(
        CollectionId='First_collection',
        MaxResults=10)
    print(response['Faces'])
    for i in response['Faces']:
        print ( "FaceId: ", i['FaceId'], "   corresponde a: ", i['ExternalImageId']) 
        
def open_image(url):
    global estado
    sleep(0.5)
    #urllib.request.urlretrieve(url,'imagen.png')
    response = requests.get(url)
    print(response)
    if str(response) == '<Response [200]>':
        bytes = response.content
        print('Pasando bytes a Rekognition')
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
        response=client.search_faces_by_image(CollectionId='First_collection',
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
#listar_faces()
#snapshot()
#search_faces(ruta_imagen_comparar)

def search_faces_by_id(listaIds):
    global estado
    print("Buscando match para los rostros encontrados")
    personas = []
    if listaIds != []:
        for id in listaIds:
            response = client.search_faces(CollectionId='First_collection',FaceId=id, MaxFaces=1, FaceMatchThreshold=60)
            print(response )
            if response['FaceMatches'] != []:    
                faceMatched = response['FaceMatches'][0]['Face']['ExternalImageId']
                similarity = response['FaceMatches'][0]['Similarity']
                personas.append([faceMatched, similarity])
                print(faceMatched,similarity)
                estado = "Se encontró similitud"
                webex(personas)
            else:
                personas = "Hay rostros, pero no se encontró match"
                estado = "Index detectó rostros, pero no hay match con alguno"
        delete_faces(listaIds)
    return personas                            

def index_faces(bytes): 
    global estado
    print("Buscando rostros en la imagen")
    face_id_list = [] 
    try:
        response = client.index_faces(CollectionId='First_collection', Image = {'Bytes': bytes},
        ExternalImageId='grupales', DetectionAttributes=['DEFAULT'], MaxFaces=5, QualityFilter='AUTO') 
        print(response)
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
    except:
        print("Error en Index_faces")
        estado = "Error en Index_faces"
        pass

def lambda_handler(event, context):
    global estado
    url_imagen = snapshot()
    open_image(url_imagen)
    #listar_faces()
    mensaje = {'estado: ': estado, 'url_snapshot: ': url_imagen}
    return {
        'statusCode': 200,
        'body': json.dumps(mensaje)}

