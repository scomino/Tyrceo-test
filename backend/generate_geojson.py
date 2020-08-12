import pymysql.cursors
import pandas as pd
import requests, json

host = "35.187.55.190"
user_name="candidate"
password="Fbps9Y7MhKQa4XPxjYo8"
db_name="test"
query_sql = "Select data.pokemon, data.score, coordinates.latitude,coordinates.longitude from data inner join data_at_coordinate ON data.id = data_at_coordinate.id_data INNER JOIN coordinates ON data_at_coordinate.id_coordinate = coordinates.id where data.pokemon in ('Bulbasur', 'Bulbasaur', 'Charmander','Squirtle','Squirtel') AND data.score >=0.5"

def get_connection(host,user_name,password,db_name):
    connection = pymysql.connect(host=host,
                                user=user_name,
                                password=password,
                                db=db_name,
                                cursorclass=pymysql.cursors.DictCursor)

    return connection                            

def sql_to_df(sql,connection):
    df = pd.read_sql_query(sql,connection)
    connection.close()
    return df

def df_to_geojson(df):
    pokemon_colors = {
    'Bulbasaur' : '#817D40',
    'Bulbasur' : '#817D40',
    'Charmander': '#FF2D00',
    'Squirtle': '#07AAF4',
    'Squirtel': '#07AAF4',
    }
    geojson = {'type':'FeatureCollection', 'features':[]}
    for _, row in df.iterrows():
        feature = {'type':'Feature',
                    'properties':{
                        'marker-color':''
                    },
                    'geometry': {
                        'type':'Point',
                        'coordinates':[]
                    }
                }

        feature['properties']['marker-color'] = pokemon_colors[row['pokemon'].capitalize().strip()]                        
        feature['geometry']['coordinates'] = [row['longitude'],row['latitude']]
        geojson['features'].append(feature)

    geojson_str = json.dumps(geojson, indent=2)
    with open('backend/points.geojson', 'w') as output_file:
        output_file.write(geojson_str)

connection = get_connection(host,user_name,password,db_name)
df = sql_to_df(query_sql,connection)
df_to_geojson(df)


