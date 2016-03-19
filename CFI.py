from flask import Flask,render_template
import pyqrcode,json
from flask import jsonify
import random,string
from datetime import datetime
from flask.ext.cors import cross_origin
from flask import request
from flask.ext.pymongo import PyMongo
from functools import wraps
from flask.ext.bcrypt import Bcrypt
from bson.objectid import ObjectId

app = Flask(__name__)
mongo = PyMongo(app)
bcrypt=Bcrypt(app)
# cors = CORS(app, resources={r"*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        data = request.get_json(force=True)
        if not check_status(data['authkey'],data['usertype']):
            return jsonify(error="Login Required"),403
        return f(*args, **kwargs)
    return decorated_function


# chars='0123456789!@#$%^&*()_-+=`;,.?/<>}{[]|\aAbcdefghijklmnopqrstuvwxyzBCDEFGHIJKLMNOPQRSTUVWXZY'
@app.route('/register',methods=['GET','POST'])
@cross_origin(origin='*', headers=['Content- Type', 'Authorization'])
def register():
    try:
        data=request.get_json(force=True)
        print data
        user=mongo.db.find_one({'adhaarId': data['adhaarId']})
        if user is None:
            mongo.db.insert({'adhaarId': data['adhaarId'],'password':bcrypt.generate_password_hash(data['password']),'name':data['name'],'gender':data['gender']})
            return jsonify(success=json.dumps(user)),201
    except Exception as e:
        print str(e)
        return jsonify(error=str(e)),500

@app.route('/login',methods=['POST'])
def login():
    try:
        data=request.get_json(force=True)
        user= mongo.db.find_one({'adhaarId':data['adhaarId']})
        if user is not None:
            if bcrypt.check_password_hash(user['password'],data['password']):
                userData={}
                userData['name']=user['name']
                userData['gender']=user['gender']
                return jsonify(success='logged in',user=json.dumps(userData)),200
    except Exception as e:
        print str(e)
        return jsonify(error=str(e)),500




@app.route('/qrgenerate/<id>')
def authenticate():
    try:
        data=request.get_json(force=True)
        monument=mongo.db.groups.find_one({"_id":ObjectId(str(id))})
        if monument is not None:
            data['authUrl']=monument['authUrl']
            data['twoFactor']=monument['twoFactor']
            data['params']=monument['params']
            code=pyqrcode.create(json.dumps(data))
            passcode=courseid+"_"+facid+"_.png"
            code.png(passcode,scale=10)
            return render_template("scan.html",image=passcode)
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)
