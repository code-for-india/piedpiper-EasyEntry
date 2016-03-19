from flask import Flask,render_template
import pyqrcode,json
from flask import jsonify
import random,string
from pymongo import MongoClient
import pymongo
import requests

application = Flask(__name__)

@application.route('/login',methods=['POST'])
def login():
	aadhaarID = request.json['id']
	password = request.json['password']
	cfiClient = MongoClient()
	#analyticsClient = MongoClient()
	cfiDB = cfiClient['cfi']
	userCollection  = reachDB['user']
	query = dict()
	query['aadhaarID'] = aadhaarID	
	userObject = userCollection.findOne(query)	
	if not userObject :
		response = dict()
		response['status'] = "User Not found"
		return jsonify(response),403
	else:
		if password == userObject['password']:
			response = dict()
			response['userName'] = userObject['userName']
			response['aadhaarID'] = aadhaarID
			response['gender'] = userObject['gender']
			response['status'] = "Success"
			return jsonify(response),200
		else:
			response = dict()
			response['status'] = "Password Invalid"
			return jsonify(response),403

@application.route('/monumentslist',methods=['GET'])
def monumentsList():
	response = list()
	cfiClient = MongoClient()
	#analyticsClient = MongoClient()
	cfiDB = cfiClient['cfi']
	monumentCollection  = reachDB['monuments']
	monumentCursor = monumentCollection.find()	
	for monumentObject in monumentCursor:
		entry = dict()
		entry['photoURL'] =  		
		monumentObject['id']	

if __name__ == '__main__':
    application.debug = True
    application.run(host = '0.0.0.0')
