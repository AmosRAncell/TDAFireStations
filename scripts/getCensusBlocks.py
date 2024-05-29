import requests
import os
import json
import numpy as np

# ----- User Input -----
CITY_NAME = 'AtlantaClaytonCounty'
FIPS_STATE = '13'
FIPS_COUNTY = '063'

OBJ_ID_CHUNK_SIZE = 250

OUT_FOLDER = os.path.join(os.getcwd(),'..','data',f'Chunks_{CITY_NAME}')
OUT_FILE = '{CITY_NAME}_Chunk{ChunkNum}.json'
ERROR_FILE = f'ErrorObjectIds_{CITY_NAME}.csv'
# ----------------------

params = {
	'where':f"COUNTY='{FIPS_COUNTY}' AND STATE='{FIPS_STATE}'",
	'f':'json',
	'returnIdsOnly':'true'
}

url = "https://services2.arcgis.com/FiaPA4ga0iQKduv3/arcgis/rest/services/US_Census_Blocks_v1/FeatureServer/0/query"

print(f'Making API request for {CITY_NAME}')
response = requests.get(url,params=params)

if response.status_code == 200:
	# only reason to use the np array here is bc i'm lazy to convert the ints to strings
	objIds = np.array(response.json()['objectIds'],dtype='str')
else :
	print('Error getting the object IDs!')
	print(f'Error {response.status_code}: {response.text}')
	raise ValueError

print(f'{len(objIds)} objectIds returned. First five are: {objIds[:5]}')

def chunks(arr,size):
	for i in range(0,len(arr),size):
		yield arr[i:i+size]

numChunks = len(objIds)//OBJ_ID_CHUNK_SIZE+1

for i,ids in enumerate(chunks(objIds,OBJ_ID_CHUNK_SIZE)):
	if i%10 == 0:
		print(f'downloading chunk {i}/{numChunks}')
	r = requests.get(url+f"?where=1=1&f=json&outFields=GEOID&objectIds={','.join(ids)}")
	if r.status_code == 200:
		fileName = OUT_FILE.format(CITY_NAME=CITY_NAME,ChunkNum=i)
		with open(os.path.join(OUT_FOLDER,fileName),'w+') as f:
			json.dump(r.json(),f,indent=4)
	else :
		print(f'Error getting data for chunk {i}')
		print(f"Error {r.status_code}: {r.json()['error']}")
		with open(os.path.join(OUT_FOLDER,ERROR_FILE),'a+') as f:
			f.write('\n'.join(ids))
			f.write('\n')
