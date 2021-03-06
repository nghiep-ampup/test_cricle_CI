import smartcar
import os

from flask import Flask, redirect, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)
CORS(app)

# global variable to save our access_token
access = None

client = smartcar.AuthClient(
    client_id=os.environ.get('CLIENT_ID'),
    client_secret=os.environ.get('CLIENT_SECRET'),
    redirect_uri=os.environ.get('REDIRECT_URI'),
    scope=['required:read_vehicle_info', 'read_vin', 'required:read_location', 'read_battery', 'read_charge'],
    test_mode=True
)


@app.route('/login', methods=['GET'])
def login():
    auth_url = client.get_auth_url(
        single_select={'vin': '0SCAUDI037A5ADB1C'}
    )
    return redirect(auth_url)


@app.route('/', methods=['GET'])
def index():

    return 'index page'


@app.route('/exchange', methods=['GET'])
def exchange():
    code = request.args.get('code')

    # access our global variable and store our access tokens
    global access
    # in a production app you'll want to store this in some kind of
    # persistent storage
    access = client.exchange_code(code)
    return jsonify(access), 200


@app.route('/vehicle', methods=['GET'])
def vehicle():
    # access our global variable to retrieve our access tokens
    global access
    # the list of vehicle ids
    vehicle_ids = smartcar.get_vehicle_ids(
        access['access_token'])['vehicles']

    # instantiate the first vehicle in the vehicle id list
    vehicle = smartcar.Vehicle(vehicle_ids[0], access['access_token'])

    info = vehicle.info()
    print(info)

    return jsonify(info)


if __name__ == '__main__':
    # do some thing
    app.run(port=8000)
