"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os 
from datetime import datetime
from flask import Flask, request, jsonify, url_for 
from flask import Flask, jsonify, request
from flask_jwt_simple import JWTManager, jwt_required, create_jwt, get_jwt_identity
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Medicalstaff, Treatment, Patient, Diagnostic
#from models import Person 

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'carenow' 
jwt = JWTManager(app)
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

# Provide a method to create access tokens. The create_jwt()
# function is used to actually generate the token

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

# <---login--->

@app.route('/login', methods=['POST'])
def login():
    
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    params = request.get_json()
    email = params.get('email', None)
    password = params.get('password', None)
    
    if not email:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400
    user = Medicalstaff.query.filter_by(email=email).one_or_none()
    
    if user is None:
        return jsonify({"msg": "not found"}), 404

    if user.password != password:
        return jsonify({"msg": "Bad username or password"}), 401

    ret = {'jwt': create_jwt(identity=user.id)}
    return jsonify(ret), 200

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
            last_name=body['last_name'], 
            username=body['username'],
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



@app.route('/treatment', methods=['POST', 'GET'])
@jwt_required
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
            doctor_id=get_jwt_identity(),
            patient_id=body['patient_id'],
            name=body['name'],
            date=datetime.strptime(body['date'], "%m-%d-%Y"),
            hospital=body['hospital'],
            room=body['room'],
            covidtest=body['covidtestresult'],
            status=body['status'],
            notes=body['notes'],
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
@jwt_required
def handle_patient():
    """
    Create person and retrieve all users
    """
    # POST request

    if request.method == 'POST':
        body = request.get_json()
        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)
        if (
            'first_name' not in body or
            'last_name' not in body or
            'date' not in body or
            'birth_date' not in body or
            'gender' not in body or
            'address' not in body or
            'email' not in body or
            'phone_number' not in body or 
            'id_number' not in body
        ):
            raise APIException('Please check your input', status_code=400)
        print(body['date'])
        user1 = Patient(
            date= datetime.strptime(body['date'], "%m-%d-%Y"),
            first_name=body['first_name'],
            last_name=body['last_name'],
            birth_date = datetime.strptime(body['birth_date'], "%m-%d-%Y"),
            gender = body['gender'],
            address = body['address'],
            email = body['email'],
            phone_number = body['phone_number'],
            id_number = body['id_number'],
            doctor_id = get_jwt_identity()
        )
        try: 
            db.session.add(user1)
            db.session.commit()
            return jsonify(user1.serialize()), 201
        except Exception as error:
            db.session.rollback()
            print(error)
            return "bad request", 400
    # GET request
    if request.method == 'GET':
        all_people = Patient.query.filter_by(doctor_id=get_jwt_identity()).all()
        all_people = list(map(lambda x: x.serialize(), all_people))
        return jsonify(all_people), 200
    return "Invalid Method", 404


@app.route('/diagnostic', methods=['POST', 'GET'])
@jwt_required
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
            name=body['name'],
            date_time=datetime.strptime(body['date_time'], "%m-%d-%Y"),
            status=body['status'],
            covidtestresult=body['covidtestresult'],
            symptoms =body['symptoms'],
            admission =body['admission'],
            notes=body['notes'],
            prescription=body['prescription'],
            total_cost=body['total_cost'],
            treatment_id=body["treatment_id"]
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
