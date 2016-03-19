from flask import Flask,render_template
import pyqrcode,json
from flask import jsonify, request
import random,string
from pymongo import MongoClient
import pymongo
import random
import requests

application = Flask(__name__)

@application.route('/login',methods=['POST'])
def login():
	aadhaarID = request.json['id']
	password = request.json['password']
	cfiClient = MongoClient()
	#analyticsClient = MongoClient()
	cfiDB = cfiClient['cfi']
	userCollection  = cfiDB['user']
	query = dict()
	query['aadhaarID'] = aadhaarID	
	userObject = userCollection.find_one(query)	
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
	monumentCollection  = cfiDB['monuments']
	monumentCursor = monumentCollection.find()	
	for monumentObject in monumentCursor:
		entry = dict()
		entry['photo'] = monumentObject['photoURL']
		entry['name'] = monumentObject['monumentName']
		entry['id'] = monumentObject['monumentId']
		response.append(monumentObject)
	return jsonify(response), 200

@application.route('/booking',methods=['POST'])
def booking():
	dbObject = dict()
	dbObject['userID'] = request.json['userId']
	visitorList = list()
	visitors = request.json['visitors']	
	response = dict() 
	cfiClient = MongoClient()
	#analyticsClient = MongoClient()
	cfiDB = cfiClient['cfi']
	userCollection  = cfiDB['user']
	responseList = list()	
	dbList = list()
	for entry in visitors :
		userId = entry['id']	
		query = dict()
		query["aadhaarID"] = userID
		userObject = userCollection.find_one(query)		
		responseEntry = dict()		
		dbEntry = dict()		
		if not userID :
			responseEntry[userID] = "false"
		else :
			if entry['userName'] == userObject['userName']:
				responseEntry[userID] = "true"
				dbEntry['userID'] = userID
				dbEntry['userName'] = entry['userName']
				dbList.append(dbEntry)
			else :
				responseEntry[userID] = "false"
		responseList.append(responseEntry)
	dbObject['visitors'] = responseList
	response['status'] = responseList
	ticketID = 'GOV - ' + str(random.getrandbits(6))	
	response['ticketID'] = ticketID	
	dbObject['ticketID'] = ticketID	
	#query = dict()
	#query['aadhaarID'] = request.json['userId']
	#userObject = userCollection.findOne(query)
	#label = 	
	QRcodebase64string = callFunction(ticketID)
	response['QRcode'] = QRcodebase64string
	dbObject['QRcode'] = QRcodebase64string
	cfiClient = MongoClient()
	#analyticsClient = MongoClient()
	cfiDB = cfiClient['cfi']
	dbObject['monumentName'] = request.json['monumentName']
	monumentCollection  = cfiDB['tickets']
	monumentsCollection.insert_one(dbObject)
	return jsonify(response), 200
				
if __name__ == '__main__':
    application.debug = True
    application.run(host = '0.0.0.0')
