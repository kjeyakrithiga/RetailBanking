from Retail_Application import app,db
from werkzeug.security import generate_password_hash, check_password_hash
from mongoengine import *
import datetime


class UserStore(db.Document):
    username     =   db.StringField( unique=True )
    password    =   db.StringField( )
    created_at = db.DateTimeField(default=datetime.datetime.utcnow)

      

class CustomerDetails(db.Document):
    customer_ssn_id   =   db.IntField(unique=True)
    customer_id       =   db.IntField(unique=True)
    customer_name     =   db.StringField( max_length=100 )
    age               =   db.IntField()
    address           =   db.StringField(max_length=200)
    date              =   db.DateTimeField(default=datetime.datetime.utcnow)
    

class AccountDetails(db.Document):
    customer_id     =   db.IntField()
    account_id      =   db.IntField()
    account_type    =   db.StringField( max_length=100 )
    deposit_amount  =   db.IntField()
    date              =   db.DateTimeField(default=datetime.datetime.utcnow)


class CustomerStatus(db.Document):
    customer_ssn_id=db.IntField()
    customer_id=db.IntField()
    status=db.StringField()
    message=db.StringField()
    date              =   db.DateTimeField(default=datetime.datetime.utcnow)
    
class AccountStatus(db.Document):
    customer_id=db.IntField()
    account_id=db.IntField()
    account_type=db.StringField()
    account_status=db.StringField()
    message=db.StringField()
    date              =   db.DateTimeField(default=datetime.datetime.utcnow)
    




    


class Address(db.Document):
    customer_id=db.IntField()
    address_line1= db.StringField()
    address_line2=db.StringField()
    city=db.StringField()
    state=db.StringField()