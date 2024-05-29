import os
import pandas as pd
import geopandas as gpd

# ----- User Input -----
CHUNK_FOLDER = os.path.join(os.getcwd(),'..','data','Chunks_AtlantaClaytonCounty')

OUT_FOLDER = os.path.join(os.getcwd(),'..','data')
OUT_FILE = 'censusBlocks_AtlantaClaytonCounty.geojson'
# -----------------------

fNames = os.listdir(CHUNK_FOLDER)

data = []
for i,fName in enumerate(fNames):
	if not fName.endswith('.json'):
		continue
	if i%50 == 0:
		print(f"Loaded in {i}/{len(fNames)} jsons")
	df = gpd.read_file(os.path.join(CHUNK_FOLDER,fName))
	data.append(df)

data = pd.concat(data)
data.to_file(os.path.join(OUT_FOLDER,OUT_FILE))
