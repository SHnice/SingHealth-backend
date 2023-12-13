from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS,cross_origin
from flask_bcrypt import Bcrypt  
from bson import ObjectId 
# from flask.json import JSONEncoder

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['MONGO_URI'] = 'mongodb+srv://arsal0344:03444800061@cluster0.u6h8hwf.mongodb.net/healthdb?retryWrites=true&w=majority'
mongo = PyMongo(app)
bcrypt = Bcrypt(app)  

@app.route('/get-doctors', methods=['GET'])
@cross_origin()
def get_doctors():
    doctors_collection = mongo.db.doctors
    doctors = list(doctors_collection.find({}, {'_id': 1, 'name': 1, 'email': 1}))

    # Convert ObjectId to string representation
    for doctor in doctors:
        doctor['_id'] = str(doctor['_id'])

    return jsonify(doctors)

@app.route('/register-doctor', methods=['POST'])
@cross_origin()
def register_doctor():
    # Get data from the request
    data = request.get_json()

    # Extract doctor information
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    # Hash the password before storing it
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Validate data (you can add more validation as needed)

    # Insert the doctor data into MongoDB with the hashed password
    doctors_collection = mongo.db.doctors  # 'doctors' is the name of the collection
    doctor_id = doctors_collection.insert_one({
        'name': name,
        'email': email,
        'password': hashed_password
    }).inserted_id

    # Return a response
    response = {
        'message': 'Doctor registered successfully',
        'doctor_id': str(doctor_id)
    }

    return jsonify(response)


# Define the edit-doctor endpoint
@app.route('/edit-doctor/<string:doctor_id>', methods=['PUT'])
@cross_origin()
def edit_doctor(doctor_id):
    # Get data from the request
    data = request.get_json()

    # Extract updated doctor information
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')  # Add more fields as needed

    # Update the doctor data in MongoDB
    doctors_collection = mongo.db.doctors
    doctors_collection.update_one({'_id': ObjectId(doctor_id)}, {'$set': {'name': name, 'email': email, 'password': password}})

    # Return a response
    response = {
        'message': 'Doctor updated successfully'
    }

    return jsonify(response)

# Define the delete-doctor endpoint
@app.route('/delete-doctor/<string:doctor_id>', methods=['DELETE'])
@cross_origin()
def delete_doctor(doctor_id):
    # Delete the doctor from MongoDB
    doctors_collection = mongo.db.doctors
    result = doctors_collection.delete_one({'_id': ObjectId(doctor_id)})

    # Check if the doctor was successfully deleted
    if result.deleted_count == 1:
        response = {
            'message': 'Doctor deleted successfully'
        }
    else:
        response = {
            'message': 'Doctor not found'
        }

    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
