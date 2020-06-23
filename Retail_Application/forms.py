from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from Retail_Application.models import UserStore, CustomerDetails,CustomerStatus,AccountDetails

class LoginForm(FlaskForm):
    username   = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6,max=15)])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    username   = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(),Length(min=6,max=15)])
    password_confirm = PasswordField("Confirm Password", validators=[DataRequired(),Length(min=6,max=15), EqualTo('password')])
    submit = SubmitField("Register Now")

class CustomerRegister(FlaskForm):
    customer_name = StringField("Customer Name", validators=[DataRequired(),Length(min=6,max=15)])
    age = StringField("Age", validators=[DataRequired(), Length(min=3,max=3)])
    address_line1 = StringField("Address Line1", validators=[DataRequired(),Length(min=2,max=55)])
    address_line2 = StringField("Address Line2", validators=[DataRequired(),Length(min=2,max=55)])
    city = StringField("City", validators=[DataRequired(),Length(min=2,max=55)])
    state = StringField("State", validators=[DataRequired(),Length(min=2,max=55)])
    submit = SubmitField("Register Now")

class CustomerSearch(FlaskForm):
    customer_name = StringField("Customer Name", validators=[DataRequired(),Length(min=6,max=15)])
    submit = SubmitField("Search customer")

class CustomerSearch2(FlaskForm):
    customer_ssn_id = IntegerField("Customer SSN ID")
    customer_id = IntegerField("Customer ID")
    submit = SubmitField("Search customer")

class CustomerUpdate(FlaskForm):
    customer_name=StringField("Customer Name")
    age = StringField("Age")
    city = StringField("City")
    submit = SubmitField("Update now")

class CustomerDelete(FlaskForm):
    submit = SubmitField("Delete now")

class AccountDelete(FlaskForm):
    submit = SubmitField("Delete now")

class AccountCreation(FlaskForm):
    customer_id = IntegerField("ReEnter the Customer ID", validators=[DataRequired()])
    account_type = StringField("Account Type", validators=[DataRequired()])
    deposit_amount = IntegerField("Deposit Amount", validators=[DataRequired()])    
    submit = SubmitField("Register Now")

class AccountSearch(FlaskForm):
    customer_id = IntegerField("Customer ID")
    account_id = IntegerField("Account ID")
    submit = SubmitField("Search account")

class AccountSearch2(FlaskForm):
    customer_id = IntegerField("Customer ID")
    account_id = IntegerField("Account ID")
    submit_withdraw = SubmitField("Withdraw")
    submit_deposit = SubmitField("Deposit")


class DepositForm(FlaskForm):
    deposit = IntegerField("Deposit Amount")
    submit = SubmitField("Deposit")

class WithdrawForm(FlaskForm):
    withdraw = IntegerField("Withdraw Amount")
    submit = SubmitField("Withdraw")

class TransferForm(FlaskForm):
    sender_account_id= IntegerField("Sender Account ID")
    receiver_account_id=IntegerField("Receiver Account ID")
    transfer_amount=IntegerField("Enter amount to be Transfered")
    submit = SubmitField("Submit")



