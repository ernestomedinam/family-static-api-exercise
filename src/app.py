"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

initial_members = [{
    "first_name": "John",
    "age": 33,
    "lucky_numbers": [7, 13, 22]
}, {
    "first_name": "Jane",
    "age": 35,
    "lucky_numbers": [10, 14, 3]
}, {
    "first_name": "Jimmy",
    "age": 5,
    "lucky_numbers": [1]
}]

# create the jackson family object
jackson_family = FamilyStructure("Jackson")
for member in initial_members:
    jackson_family.add_member(member)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/member', methods=['POST'])
@app.route('/members', methods=['GET', 'POST']) # ideal
@app.route('/member/<int:member_id>', methods=['GET', 'DELETE'])
@app.route('/members/<int:member_id>', methods=['GET', 'DELETE']) # ideal
def handle_members(member_id=None):
    # this is how you can use the Family datastructure by calling its methods
    if request.method == 'GET':
        # if GET was requested on /members
        if member_id is None:
            members = jackson_family.get_all_members()
            return jsonify([member.serialize() for member in members]), 200
        # if GET is requested on member(s)/member_id:
        member = jackson_family.get_member(member_id)
        return jsonify(member.serialize()), 200
    if request.method == 'DELETE':
        # delete is always requested on member(s)/member_id:
        jackson_family.delete_member(member_id)
        # return jsonify([]), 204 <- this is ideal response for delete requests
        return jsonify({"done": True}), 200
    # if method is POST...
    new_member = jackson_family.add_member(request.json)
    return jsonify(new_member.serialize()), 200 # 201

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
