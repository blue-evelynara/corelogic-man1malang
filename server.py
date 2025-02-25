from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)
MONGODB_URI="mongodb+srv://evelynara:corelogic@cluster0.8vlos.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DB_NAME = "corelogic"
COLLECTION_NAME = "sic"
client = MongoClient(MONGODB_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

@app.route('/save',methods=["POST"])
def save_data():
    data = request.get_json()
    lux = data.get("Cahaya")
    distance = data.get("Jarak")
    
    simpan = {"Cahaya":lux,"Jarak":distance}
    collection.insert_one(simpan)
    
    return jsonify({"message":"success"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=2000)
