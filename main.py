from typing import Union
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import dotenv_values

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["GET"],
    allow_headers=["*"],
)

@app.get("/denuncias")
def get_all_records(street_category: Union[str, None] = None):

    config = dotenv_values(".env")

    uri = f"mongodb+srv://{config['MONGO_USER']}:{config['MONGO_PASS']}@cluster0.8jwuy6u.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client.get_database(f"{config['DB_NAME']}")

    denuncia_collection = db.get_collection(f"{config['COLL_NAME']}")

    denuncia_json = {
        "denuncias": []
    }

    if street_category:
        for denuncia in denuncia_collection.find({ "street_category": street_category }):
            denuncia_json["denuncias"].append({
                'street_category': denuncia['street_category'], 
                'image_url': denuncia['image_url'], 
                'street_coords': {'lat': denuncia['street_coords']['lat'], 'lng': denuncia['street_coords']['lng']}, 
                'opt_address': denuncia['opt_address'], 
                'opt_user_comment': denuncia['opt_user_comment'], 
                'upload_date': denuncia['upload_date']
            })
       
        return denuncia_json
    
    else:
        for denuncia in denuncia_collection.find():
            denuncia_json["denuncias"].append({
                'street_category': denuncia['street_category'], 
                'image_url': denuncia['image_url'], 
                'street_coords': {'lat': denuncia['street_coords']['lat'], 'lng': denuncia['street_coords']['lng']}, 
                'opt_address': denuncia['opt_address'], 
                'opt_user_comment': denuncia['opt_user_comment'], 
                'upload_date': denuncia['upload_date']
            })
        
        return denuncia_json

