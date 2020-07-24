"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Medicalstaff, Treatment, Patient, Diagnostic
#from models import Person 

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# @app.route('/user', methods=['GET'])
# def handle_hello():

#     response_body = {
#         "msg": "Hello, this is your GET /user response "
#     }

#     return jsonify(response_body), 200

@app.route('/user', methods=['POST', 'GET'])
def handle_user():
    """
    Create person and retrieve all users
    """
    # POST request
    if request.method == 'POST':
        body = request.get_json()
        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)
        if 'email' not in body:
            raise APIException('You need to specify the email', status_code=400)
        if 'password' not in body:
            raise APIException('You need to specify the password', status_code=400)    
        user1 = User(email=body['email'], password=body['password'], is_active=True)
        db.session.add(user1)
        db.session.commit()
        return "ok", 200
    # GET request
    if request.method == 'GET':
        all_people = User.query.all()
        all_people = list(map(lambda x: x.serialize(), all_people))
        return jsonify(all_people), 200
    return "Invalid Method", 404

@app.route('/medicalstaff', methods=['POST', 'GET'])
def handle_medicalstaff():
    """
    Create person and retrieve all users
    """
    # POST request
    if request.method == 'POST':
        body = request.get_json()
        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)
        if 'email' not in body:
            raise APIException('You need to specify the email', status_code=400)
        if 'password' not in body:
            raise APIException('You need to specify the password', status_code=400)    
        user1 = Medicalstaff( 
            email=body['email'], 
            password=body['password'], 
            first_name=body['first_name'],
            last_name=body['last_name']
            )
        db.session.add(user1)
        db.session.commit()
        return "ok", 200
    # GET request
    if request.method == 'GET':
        all_people = Medicalstaff.query.all()
        all_people = list(map(lambda x: x.serialize(), all_people))
        return jsonify(all_people), 200
    return "Invalid Method", 404

# @app.route('/specialty', methods=['POST', 'GET'])
# def handle_specialty():
#     """
#     Create person and retrieve all users
#     """
#     # POST request
#     if request.method == 'POST':
#         body = request.get_json()
#         if body is None:
#             raise APIException("You need to specify the request body as a json object", status_code=400)
#         if 'name' not in body:
#             raise APIException('You need to specify the name', status_code=400)
#         user1 = Specialty(
#             name=body['name'],
#             doctor_id=body['doctor_id']
#             )
#         db.session.add(user1)
#         db.session.commit()
#         return "ok", 200
#     # GET request
#     if request.method == 'GET':
#         all_people = Specialty.query.all()
#         all_people = list(map(lambda x: x.serialize(), all_people))
#         return jsonify(all_people), 200
#     return "Invalid Method", 404

@app.route('/treatment', methods=['POST', 'GET'])
def handle_treatment():
    """
    Create person and retrieve all users
    """
    # POST request
    if request.method == 'POST':
        body = request.get_json()
        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)
        if 'name' not in body:
            raise APIException('You need to specify the name', status_code=400)
        user1 = Treatment(
            doctor_id=body['doctor_id'],
            patient_id=body['patient_id'],
            diagnostic_id=body['diagnostic_id'],
            name=body['name'],
            status=body['status'],
            address=body['address'],
            phone_number=body['phone_number'],
            room_number=body['room_number'],
            email=body['email'],
            start_date=['start_date'],
            end_date=['end_date']
            )
        db.session.add(user1)
        db.session.commit()
        return "ok", 200
    # GET request
    if request.method == 'GET':
        all_people = Treatment.query.all()
        all_people = list(map(lambda x: x.serialize(), all_people))
        return jsonify(all_people), 200
    return "Invalid Method", 404

@app.route('/patient', methods=['POST', 'GET'])
def handle_patient():
    """
    Create person and retrieve all users
    """
    # POST request
    if request.method == 'POST':
        body = request.get_json()
        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)
        if 'first_name' not in body:
            raise APIException('You need to specify the first name', status_code=400)
        if 'last_name' not in body:
            raise APIException('You need to specify the last name', status_code=400)       
        user1 = Patient(
            date=body['date'],
            first_name=body['first_name'],
            last_name=body['last_name'],
            birth_date =body['birth_date'],
            gender =['gender'],
            address =['address'],
            phone_number =['phone_number'],
            id_number =['id_number']
            )
        db.session.add(user1)
        db.session.commit()
        return "ok", 200
    # GET request
    if request.method == 'GET':
        all_people = Patient.query.all()
        all_people = list(map(lambda x: x.serialize(), all_people))
        return jsonify(all_people), 200
    return "Invalid Method", 404


@app.route('/diagnostic', methods=['POST', 'GET'])
def handle_diagnostic():
    """
    Create person and retrieve all users
    """
    # POST request
    if request.method == 'POST':
        body = request.get_json()
        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)
        if 'name' not in body:
            raise APIException('You need to specify the name', status_code=400)
        user1 = Diagnostic(
            patient_id=body['patient_id'],
            datetime=body['datetime'],
            status=body['status'],
            covidtest=body['covidtest'],
            symptoms =body['symptoms'],
            reasonforadmi =body['reasonforadmi'],
            notes=body['notes'],
            prescription=body['prescription'],
            totalcost=body['totalcost'],
            )
        db.session.add(user1)
        db.session.commit()
        return "ok", 200
    # GET request
    if request.method == 'GET':
        all_people = Diagnostic.query.all()
        all_people = list(map(lambda x: x.serialize(), all_people))
        return jsonify(all_people), 200
    return "Invalid Method", 404

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
