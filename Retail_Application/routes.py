from Retail_Application import app,db
from flask import render_template,request, json, Response, redirect, flash, url_for, session
import pymongo
from bson.objectid import ObjectId
import random
from datetime import datetime

from Retail_Application.models import CustomerDetails,UserStore, AccountDetails, AccountStatus, Address
from Retail_Application.forms import LoginForm, CustomerRegister, RegisterForm, CustomerSearch, CustomerSearch2,CustomerUpdate, CustomerDelete, CustomerStatus
from Retail_Application.forms import AccountCreation, AccountSearch, DepositForm, WithdrawForm, AccountSearch2, TransferForm, AccountDelete


#################  HOME   ###################

@app.route("/")
@app.route("/index")
@app.route("/home/")
@app.route("/home/<login>",methods=['GET','POST'])
@app.route("/home/<username>",methods=['GET','POST'])
@app.route("/home/<login>/<username>",methods=['GET','POST'])
def index(login=True,username=""):
    if session.get('username'):
        username    =   session.get('username')
    if(login!=False and username!=""):
        return render_template("index.html", login=True,username=username )
    else:
        return render_template("index.html", login=False )


#################  LOGIN   ###################

@app.route("/login", methods=['GET', 'POST'])
def login():
    if session.get('username'):
        return redirect(url_for('index',login=True,username=session.get('username')))

    form=LoginForm()
    if form.validate_on_submit():
        username    =   form.username.data
        password    =   form.password.data
        userstore   =   UserStore.objects(username=username).first()
        if userstore and userstore.password==password:
            flash(f"{userstore.username},You are successfully logged in !!", "success")
            session['username']=userstore.username
            return render_template('index.html',login=True,username=session.get('username'))
        else:
            flash("Sorry something went wrong!!", "danger")
    return render_template("login.html", title="Login", form=form)


#################  LOGOUT   ###################

@app.route("/logout")
def logout():
    session['username']=False
    return render_template('index.html',login=False,username=session['username'])
    

#################  CREATE CUSTOMER   ###################


@app.route("/createCustomer", methods=['POST','GET'])
def createCustomer():
    form = CustomerRegister()
    if form.validate_on_submit():
        customer_ssn_id     = random.randint(300000001, 600000000)
        customer_id         = random.randint(100000000,300000000)
        customer_name       = form.customer_name.data
        age                 = form.age.data
        address_line1       = form.address_line1.data
        address_line2       = form.address_line2.data
        city                = form.city.data
        state               = form.state.data
        address1=address_line1+", "+address_line2+", "+city+", "+state
        

        customer=CustomerDetails.objects(customer_name=customer_name).first()
        if customer:
            flash(f"{customer.customer_name} Customer is already registered  !!", "danger")
            return redirect(url_for('index',login=True))

        customerdetails = CustomerDetails(customer_ssn_id=customer_ssn_id, customer_id=customer_id, customer_name=customer_name, age=age, address=address1)
        customerdetails.save()
        address=Address(customer_id=customer_id, address_line1=address_line1, address_line2=address_line2, city=city, state=state)
        address.save()
        customerstatus=CustomerStatus(customer_ssn_id=customer_ssn_id, customer_id=customer_id, status="Active", message="Customer created successfully")
        customerstatus.save()
        
        flash(f"Customer {customerdetails.customer_name} creation initiated successfully !","success")
        return redirect(url_for('index',login=True))
    return render_template("createCustomer.html", title="Create Customer Screen", form=form, createCustomer=True, customerstatus=True,login=True)

#################  UPDATE CUSTOMER   ###################

@app.route("/updateCustomer/", methods=['POST', 'GET'])
@app.route("/updateCustomer/<cn>/", methods=['POST', 'GET'])
def updateCustomer(cn):
    #keys=request.args.get('cn')
    #flash(f"keys : {cn}","danger")
    customers = CustomerDetails.objects.all()
    addressobj=Address.objects.all()
    form = CustomerUpdate()
    if form.validate_on_submit():
        customer_name     = cn
        for cus in customers:
            if cus.customer_name==customer_name:
                print(cus.customer_name)
                cid=cus.customer_id
                customerstatus=CustomerStatus.objects(customer_ssn_id=cus.customer_ssn_id).first()
                if(customerstatus):
                    customerstatus.status="Active"
                    customerstatus.message="Customer Update completed"
                else:
                    customerstatus=CustomerStatus(customer_ssn_id=cus.customer_ssn_id,status="Active",message="Customer Update completed")
                customerstatus.save()
        customerdb=CustomerDetails.objects(customer_name=customer_name).first()
        address=Address.objects(customer_id=cid).first()
        address.city=form.city.data
        address.save()
        for add in addressobj:
            if add.customer_id==cid:
                address1=add.address_line1+" ,"+add.address_line2+", "+add.city+", "+add.state
                customerdb.address=address1


        customerdb.customer_name=form.customer_name.data
        customerdb.age      =form.age.data
        customerdb.save()
        flash(f"{customerdb.customer_name} Customer updated !!", "success")
        return redirect(url_for('index',login=True))
    return render_template("updateCustomer.html", title="Customer Update",form=form,login=True, customers=customers, cn=cn, addressobj=addressobj, customerupdate=True )

#################  DELETE CUSTOMER   ###################

@app.route("/deleteCustomer/", methods=['POST', 'GET'])
@app.route("/deleteCustomer/<cn>", methods=['POST', 'GET'])
def deleteCustomer(cn):
    customers = CustomerDetails.objects.all()
    form = CustomerDelete()
    if form.validate_on_submit():
        customer_name     = cn
        customers=CustomerDetails.objects.all()
        for cus in customers:
            if cus.customer_name==customer_name:
                print(cus.customer_name)
                customerstatus=CustomerStatus.objects(customer_ssn_id=cus.customer_ssn_id).first()
                customerstatus=CustomerStatus(customer_ssn_id=cus.customer_ssn_id,status="Active",message="Customer Delete completed")
                customerstatus.save()
        customerdb=CustomerDetails.objects(customer_name=customer_name).first()
        flash(f"Customer Name: {cn} ","success")

        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["Retail_Bank"]
        mycol = mydb["customer_details"]

        myquery = { "customer_name": cn }

        if(mycol.delete_one(myquery)):
            flash(f"success ","success")
        else:
            flash(f"failure ","danger")

        flash(" Customer Deleted !!", "success")
        return redirect(url_for('index' ,login=True))
    return render_template("deleteCustomer.html", title="Customer Deleted", form=form, customers=customers, cn=cn, customerdelete=True ,login=True)


#################  CUSTOMER SEARCH   ###################


@app.route("/customersearch/", methods=['POST','GET'])
@app.route("/customersearch/<d>", methods=['POST','GET'])
def customersearch(d):
    form1 = CustomerSearch()
    if form1.validate_on_submit():
        customer_name     = form1.customer_name.data
        customerdb=CustomerDetails.objects(customer_name=customer_name).first()

        if customerdb:
            flash(f"{customerdb.customer_name} Customer found !!", "success")
            if(d=='1'):
                return redirect(url_for('deleteCustomer', cn=customerdb.customer_name ,login=True))
            else:
                return redirect(url_for('updateCustomer', cn=customerdb.customer_name ,login=True))
        else:
            flash("Sorry customer not found!!", "danger")
    return render_template("customersearch.html", title="Customer Search", form1=form1, customersearch=True  ,login=True)


#################  CREATE ACCOUNT   ###################
@app.route("/createAccount", methods=['POST','GET'])
def createAccount():
    form1=CustomerSearch()
    if form1.validate_on_submit():
        customer_name=form1.customer_name.data
        customer=CustomerDetails.objects(customer_name=customer_name).first()
    
        if customer:
            form2 = AccountCreation()
            return render_template("createAccount.html", title="Create account Screen", form2=form2, cid=customer.customer_id, accountcreation=True)
    
    form2 = AccountCreation()
    if form2.validate_on_submit():
        customer_id = form2.customer_id.data
        account_id     =random.randint(600000001,999999999)
        account_type       = form2.account_type.data
        deposit_amount    = form2.deposit_amount.data

        account=AccountDetails.objects(account_id=account_id).first()
        if account:
            flash(f"Account with ID {account.account_id} already exist  !!", "danger")
            return redirect(url_for('index' ,login=True))

        accountdb = AccountDetails(customer_id=customer_id, account_id=account_id, account_type=account_type, deposit_amount=deposit_amount)
        accountdb.save()

        accountstatus=AccountStatus(customer_id=customer_id, account_id=account_id, account_type=account_type, account_status="Active", message="Account creation complete")
        accountstatus.save()


        flash(f"Account with ID {accountdb.account_id} is successfully created !","success")
        return redirect(url_for('index',login=True))
    return render_template("customersearch.html", title="Enter the Customer Name", form1=form1, customersearch=True,login=True)




















@app.route("/acc_delete", methods=['POST','GET'])
def acc_delete():
    form = AccountSearch()
    if form.validate_on_submit():
        customer_id     = form.customer_id.data
        account_id = form.account_id.data
        if customer_id or account_id:
            return redirect(url_for("deleteAccount", customer_id=customer_id, account_id=account_id ,login=True))
        else:
            flash("Sorry account not found!!", "danger")
    return render_template("account_search.html", title="Account Search", form=form, accountsearch=True  ,login=True)



@app.route("/deleteAccount/", methods=['POST', 'GET'])
def deleteAccount():
    customer_id=int(request.args.get('customer_id'))
    account_id=int(request.args.get('account_id'))
    accounts = AccountDetails.objects.all()
    form = AccountDelete()
    if form.validate_on_submit():
        accounts=AccountDetails.objects.all()
        for acc in accounts:
            print("hi")
            if acc.account_id==account_id:
                print("hi")
                accountstatus=AccountStatus.objects(account_id=account_id).first()
                accountstatus=AccountStatus(account_id=account_id,account_status="Active",message="Account Delete completed")
                accountstatus.save()
                accountdb=AccountDetails.objects(account_id=account_id).first()
                flash(f"Account ID : {account_id} ","success")

                myclient = pymongo.MongoClient("mongodb://localhost:27017/")
                mydb = myclient["Retail_Bank"]
                mycol = mydb["account_details"]

                myquery = { "account_id": account_id }

                if(mycol.delete_one(myquery)):
                    flash(f"success ","success")
                else:
                    flash(f"failure ","danger")

                flash(" Account Deleted !!", "success")
                return redirect(url_for('index' ,login=True))
            

            elif acc.customer_id==customer_id:
                accountstatus=AccountStatus.objects(customer_id=customer_id).first()
                accountstatus=AccountStatus(customer_id=customer_id,account_status="Active",message="Account Delete completed")
                accountstatus.save()
                accountdb=AccountDetails.objects(customer_id=customer_id).first()
                flash(f"Account ID : {customer_id} ","success")

                myclient = pymongo.MongoClient("mongodb://localhost:27017/")
                mydb = myclient["Retail_Bank"]
                mycol = mydb["account_details"]

                myquery = { "customer_id": customer_id }

                if(mycol.delete_one(myquery)):
                    flash(f"success ","success")
                else:
                    flash(f"failure ","danger")

                flash(" Account Deleted !!", "success")
                return redirect(url_for('index' ,login=True))
    return render_template("deleteAccount.html", title="Account Deleted", form=form, accounts=accounts, customer_id=customer_id, account_id=account_id, accountdelete=True ,login=True)



@app.route("/view_account_status",methods=['POST','GET'])
def view_account_status():
    account = AccountStatus.objects.all()
    return render_template("view_account_status.html", title="Account Status", account=account, viewaccountstatus=True  ,login=True)

@app.route("/view_customer_status",methods=['POST','GET'])
def view_customer_status():
    customers = CustomerStatus.objects.all()
    return render_template("view_customer_status.html", title="Customer Status", customers=customers, viewcustomerstatus=True ,login=True)

@app.route("/accountsearch", methods=['POST','GET'])
def accountsearch():
    form = AccountSearch()
    flag=0
    if form.validate_on_submit():
        customer_id     = form.customer_id.data
        account_id = form.account_id.data
        accounts=AccountDetails.objects.all()
        for acc in accounts:
            if acc.customer_id==customer_id or acc.account_id==account_id:
                return render_template("view_account.html", title="Account Found", accounts=accounts, customer_id=customer_id, account_id=account_id, accountsearch=True  ,login=True)
        else:
            flash("Sorry account not found!!", "danger")
    return render_template("account_search.html", title="Account Search", form=form, accountsearch=True  ,login=True)


@app.route("/customersearch2", methods=['POST','GET'])
def customersearch2():
    form = CustomerSearch2()
    if form.validate_on_submit():
        customer_ssn_id = form.customer_ssn_id.data
        customer_id     = form.customer_id.data
        customers=CustomerDetails.objects.all()
        address=Address.objects.all()
        for cus in customers:
            if cus.customer_id==customer_id or cus.customer_ssn_id==customer_ssn_id:
                return render_template("view_customer.html", title="Customer Found", address=address, customers=customers, customer_id=customer_id, customer_ssn_id=customer_ssn_id, customersearch2=True ,login=True )
        else:
            flash("Sorry customer not found!!", "danger")
    return render_template("customer_search2.html", title="Customer Search", form=form, customersearch2=True ,login=True )



@app.route("/acc_dep", methods=['POST','GET'])
def acc_dep():
    form = AccountSearch()
    if form.validate_on_submit():
        customer_id     = form.customer_id.data
        account_id = form.account_id.data
        if customer_id or account_id:
            return redirect(url_for("deposit", customer_id=customer_id, account_id=account_id ,login=True))
        else:
            flash("Sorry account not found!!", "danger")
    return render_template("account_search.html", title="Account Search", form=form, accountsearch=True  ,login=True)


@app.route("/deposit", methods=['POST', 'GET'])
def deposit():
    customer_id=request.args.get('customer_id')
    account_id=request.args.get('account_id')
    accounts = AccountDetails.objects.all()
    form = DepositForm()
    if form.validate_on_submit():
        for acc in accounts:
            if acc.account_id==int(account_id):
                accountstatus=AccountStatus.objects(account_id=acc.account_id).first()
                accountstatus.account_status="Active"
                accountstatus.message="Account Update completed"
                accountstatus.save()
                accountdb=AccountDetails.objects(account_id=account_id).first()
                accountdb.deposit_amount=accountdb.deposit_amount+form.deposit.data
                accountdb.save()
            elif acc.customer_id==int(customer_id):
                accountstatus=AccountStatus.objects(customer_id=acc.customer_id).first()
                accountstatus.account_status="Active"
                accountstatus.message="Account Update completed"
                accountstatus.save()
                accountdb=AccountDetails.objects(customer_id=customer_id).first()
                accountdb.deposit_amount=accountdb.deposit_amount+form.deposit.data
                accountdb.save()
        flash(" Account updated !!", "success")
        return redirect(url_for('index' ,login=True))
    return render_template("deposit.html", title="Deposit Amount", form=form, accounts=accounts, customer_id=int(customer_id), account_id=int(account_id), deposit=True  ,login=True)


@app.route("/acc_withdraw", methods=['POST','GET'])
def acc_withdraw():
    form = AccountSearch()
    if form.validate_on_submit():
        customer_id     = form.customer_id.data
        account_id = form.account_id.data
        if customer_id or account_id:
            return redirect(url_for("withdraw", customer_id=customer_id, account_id=account_id,login=True))
        else:
            flash("Sorry account not found!!", "danger")
    return render_template("account_search.html", title="Account Search", form=form, accountsearch=True ,login=True)


@app.route("/withdraw", methods=['POST', 'GET'])
def withdraw():
    customer_id=request.args.get('customer_id')
    account_id=request.args.get('account_id')
    accounts = AccountDetails.objects.all()
    form = WithdrawForm()
    if form.validate_on_submit():
        for acc in accounts:
            if acc.account_id==int(account_id):
                accountdb=AccountDetails.objects(account_id=account_id).first()
                withdraw=form.withdraw.data
                accountdb.deposit_amount=accountdb.deposit_amount-withdraw
                if accountdb.deposit_amount<5000:
                    accountdb.deposit_amount=accountdb.deposit_amount+withdraw
                    flash(f"Not enough balance for withdrawal.... Your current balance is {accountdb.deposit_amount}", "danger")
                    return redirect(url_for("index" ,login=True))
                accountstatus=AccountStatus.objects(account_id=acc.account_id).first()
                accountstatus.account_status="Active"
                accountstatus.message="Account Update completed"
                accountstatus.save()
                accountdb.save()
            elif acc.customer_id==int(customer_id):
                accountdb=Accountdb.objects(customer_id=customer_id).first()
                withdraw=form.withdraw.data
                accountdb.deposit_amount=accountDetails.deposit_amount-withdraw
                if accountdb.deposit_amount<5000:
                    accountdb.deposit_amount=accountdb.deposit_amount+withdraw
                    flash(f"Not enough balance for withdrawal.... Your current balance is {accountdb.deposit_amount}", "danger")
                    return redirect(url_for("index" ,login=True))
                accountstatus=AccountStatus.objects(customer_id=acc.customer_id).first()
                accountstatus.account_status="Active"
                accountstatus.message="Account Update completed"
                accountstatus.save()
                accountdb.save()
        flash(" Account updated !!", "success")
        return redirect(url_for('index' ,login=True))
    return render_template("withdraw.html", title="Withdraw Amount", form=form, accounts=accounts, customer_id=int(customer_id), account_id=int(account_id), withdraw=True ,login=True)



@app.route("/transferamount", methods=['POST', 'GET'])
def transferamount():
    form = TransferForm()
    if form.validate_on_submit():
        sender_account_id     = form.sender_account_id.data
        receiver_account_id = form.receiver_account_id.data
        transfer_amount = form.transfer_amount.data
        accounts = AccountDetails.objects.all()
        for acc in accounts:
            if acc.account_id==sender_account_id:
                for acc2 in accounts:
                    if acc2.account_id==receiver_account_id:
                        acc.deposit_amount=acc.deposit_amount-transfer_amount
                        if acc.deposit_amount<5000:
                            acc.deposit_amount=acc.deposit_amount+transfer_amount
                            flash(f"Not enough balance to make the transaction.... Your current balance is {acc.deposit_amount}", "danger")
                            return redirect(url_for("index" ,login=True))
                        acc2.deposit_amount=acc2.deposit_amount+transfer_amount
                        acc.save()
                        acc2.save()
                        flash("Amount transfer successful", "success")
                        return render_template("view_after_transfer.html", accounts=accounts, sender_account_id=sender_account_id, receiver_account_id=receiver_account_id,login=True)
                else:
                    flash("Sorry receiver account not found!!", "danger")
                    return redirect(url_for("index" ,login=True))
        else:
            flash("Sorry sender account not found!!", "danger")
            return redirect(url_for("index" ,login=True))
    return render_template("transfer_amount.html", title="Account Search", form=form, transferamount=True ,login=True)



@app.route("/register", methods=['POST','GET'])
def register():
    if session.get('username'):
        return redirect(url_for('index',login=True,username=session.get('username')))
    form = RegisterForm()
    if form.validate_on_submit():

        username       = form.username.data
        password    = form.password.data

        userstore = UserStore(username=username, password=password)
        
        userstore.save()
        users = UserStore.objects.all()
        return render_template("user.html",users=users,login=True)
        flash("You are successfully registered!","success")
        return redirect(url_for('index',login=True))
    return render_template("register.html", title="Register", form=form, register=True,login=True)

@app.route("/user")
def user():
    return render_template("user.html",login=True)

'''@app.route("/api/")
@app.route("/api/<idx>")
def api(idx=None):
    if(idx == None):
        jdata = courseData
    else:
        jdata = courseData[int(idx)]
    
    return Response(json.dumps(jdata), mimetype="Retail_Application/json")
'''












@app.route("/checking", methods=['GET','POST'])
def checking():
    if request.method=='POST':
        username=request.form["username"]
        password=request.form["password"]
        print(username,password)
        return render_template("index.html",login=True)
    else:
        return redirect(url_for('login'))




