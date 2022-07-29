import pandas as pd
import json 
import requests

def access_api(url_in):
    """
    Descripcion: función para obtener un JSON de la respuesta de la API
    
    INPUT: url de la API
    
    OUTPUT: regresa un python dictionary del JSON
    """
    
    # Endpoint
    endpoint_url =  url_in

    # Request
    res = requests.get(endpoint_url)
    
    #Data parsing
    results = json.loads(res.content)
    return results


url_api = 'https://api.stackexchange.com/2.2/search?order=desc&sort=activity&intitle=perl&site=stackoverflow'

#obtener la información de la API
response_json = access_api(url_api)


#dividir la información del JSON en 2, una lista contiene toda la información menos del Owner, y la otra contiene solo la información del owner 

info_list = []

owner_list = []


for id_, doc in enumerate(response_json['items']):
    #lista de las llaves quitando la del owner
    columns = set(doc.keys()) - set(['owner'])
    
    #obteniendo la informació general
    row_first_list = {key: doc[key] for key in columns}
    
    #asignando id
    row_first_list['id'] = id_
    
    #agregando la fila a la primera lista
    info_list.append(row_first_list)
    
    #obteniendo la información del dueño
    row_second_list = doc['owner'].copy()
    
    #asignando id
    row_second_list['id'] = id_
    
    #añadiendo fila
    owner_list.append(row_second_list)


#Creando DataFrames para obtener información más rápida
info_df = pd.DataFrame(info_list)
owner_df = pd.DataFrame(owner_list)


# 2. Obtener el número de respuestas contestadas y no contestadas

#no contestadas igual se puede obtener usando el true/false de la columna is_answered
non_contested = info_df[info_df.answer_count == 0].shape[0]

number_contested = info_df[info_df.answer_count > 0].shape[0]


# 3. Obtener la respuesta con menor número de vistas

#obteniendo el menor número de visitas y escogiendo las columnas que quiere obtener la información
view_count, link, _id = info_df[info_df['view_count'] == info_df['view_count'].min()][['view_count', 'link', 'id']].values.tolist()[0]

# 4. Obtener la respuesta más vieja y más actual

#obteniendo la respuesta mas vieja y mas actual y escogiendo las columnas que quiere obtener la información
min_date, link_min, id_min =  info_df[info_df['creation_date'] == info_df['creation_date'].min()][['creation_date', 'link', 'id']].values.tolist()[0]

max_date, link_max, id_max =  info_df[info_df['creation_date'] == info_df['creation_date'].max()][['creation_date', 'link', 'id']].values.tolist()[0]


# 5. Obtener la respuesta del owner que tenga una mayor reputación

#obteniendo el owner con mayor reputación y escogiendo las columnas que quiere obtener la información
user_id, reputation, link_ow, id_ow = owner_df[owner_df['reputation'] == owner_df['reputation'].max()][['user_id', 'reputation', 'link', 'id']].values.tolist()[0]

#accediendo a la info de la publicación de ese owner
link_answered = info_df[info_df['id'] == id_ow]['link'].values[0]

# 6. Imprimir en consola del punto 2 al 5

print('----------------------------------------------------------------------------------------------------------------------------------------')
print('El número de respuestas contestadas es: {}\nEl número de respuestas no contestadas es: {}'.format(number_contested, non_contested))
print('----------------------------------------------------------------------------------------------------------------------------------------\n\n\n')

print('La respuesta con menor número de visitas tiene id: {}\nEs del link: {}\nTiene: {} visitas'.format(_id, link, view_count))
print('----------------------------------------------------------------------------------------------------------------------------------------\n\n\n')

print('La respuesta más vieja tiene id: {}\nEs del link: {}\nTiene: {} visitas'.format(id_min, link_min, min_date))
print('----------------------------------------------------------------------------------------------------------------------------------------\n\n\n')

print('La respuesta más actual tiene id: {}\nEs del link: {}\nTiene: {} visitas'.format(id_max, link_max, max_date))
print('----------------------------------------------------------------------------------------------------------------------------------------\n\n\n')

print('El usuario con mayor reputación tiene el id: {}\nSu user id es: {}\nSu reputación es: {}\nSu link de usuario es:{}\nEl link de la respuesta es:{}'.format(id_ow, user_id, reputation, link_ow, link_answered))