# -*- coding: utf-8 -*-
##
#   Created on Mon Dec 27 07:26:45 2021

#   @author: thors
import os
import http
import logging
import ntsqltasks.userdbTasks as userTask
import ntsqltasks.appdbTasks as appTask
import re
from datetime import datetime, timedelta, timezone
from flask import Flask,flash, redirect, render_template, request, url_for, session, make_response, json, jsonify, Blueprint
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message,Mail
import string
from werkzeug.security import generate_password_hash, check_password_hash
import random
import smtplib
import bcrypt
from dotenv import load_dotenv


hashed_pw = generate_password_hash("yourpassword123")
print(hashed_pw)

#from johndeere.cgibin.app import app as jd

app = Flask(__name__, static_folder='templates/assets',
            template_folder='templates/html')
#app.register_blueprint(jd)


app.secret_key = "jdss88"

app.config['SERVER_NAME']= '127.0.0.1:5000'
#app.config['SERVER_NAME'] = 'spray-safely.test:5000'
# app.config['SESSION_COOKIE_DOMAIN'] = '.test'

app.config["SECURITY_PASSWORD_SALT"] = "b1.634ja9sdvhz"
app.config["MAIL_DEFAULT_SENDER"] = "noreply@spray-safely.com"
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_DEBUG"] = False
app.config["MAIL_USERNAME"] = "spraysafely.email@gmail.com"
#app.config["MAIL_PASSWORD"] = "lmcwabjagkuzvboh" "swzwpwctclpzmoep"
app.config["MAIL_PASSWORD"] = "swzwpwctclpzmoep"
app.config["SECURITY_PASSWORD_PEPPER"] = "aG93ZGVycyBhcmUgeW91IGRv"

 


debug = True







#   ************************************************************
#   ** Helping Procedures **
#   ************************************************************




def createAppJson(username, key):
    print("🛠️ createAppJson() function started")  # Step 1: Debug Start

    debugFile = nt_debug_write_file("createAppJson_Exception")
    try:
        print(f"🔹 Processing createAppJson for user: {username}")

        # Create database connection
        connection = userTask.create_db_connection()
        if not connection:
            print("❌ Error: Database connection failed")
            return None

        # Get userID from the username
        sql_query = userTask.select_userID_by_username_query()
        userID_result = userTask.execute_select_query_vals(connection, sql_query, [username])

        if not userID_result:
            print("❌ Error: No userID found for this username")
            return None

        userID = userID_result[0][0]
        print(f"✅ Retrieved userID: {userID}")

        # Get orgIDs from userID
        sql_query = userTask.select_orgIDs_by_userID_query()
        orgIDs = userTask.execute_select_query_vals(connection, sql_query, [userID])

        if not orgIDs:
            print("❌ Error: No organization IDs found for this user")
            return None

        print(f"✅ Retrieved orgIDs: {orgIDs}")

        formatted_apps = []
        for org_tuple in orgIDs:
            orgID = org_tuple[0]
            print(f"🔹 Processing applications for OrgID: {orgID}")

            sql_query = userTask.select_past_applications_by_orgID_query()
            past_apps = userTask.execute_select_query_vals(connection, sql_query, [orgID]) or []

            sql_query = userTask.select_current_applications_by_orgID_query()
            current_apps = userTask.execute_select_query_vals(connection, sql_query, [orgID]) or []

            sql_query = userTask.select_future_applications_by_orgID_query()
            future_apps = userTask.execute_select_query_vals(connection, sql_query, [orgID]) or []

            appList = past_apps + current_apps + future_apps

            print(f"✅ Retrieved {len(appList)} applications for OrgID: {orgID}")

            # Process each application
            for app in appList:
                try:
                    farmName = app[0]
                    fieldName = app[1]
                    appID = app[2]
                    appType = app[3]
                    startTime = app[4]
                    endTime = app[5]

                    sql_query_rei = userTask.select_REI_time_from_application_query()
                    reitime = userTask.execute_select_query_vals(connection, sql_query_rei, [appID])[0][0]

                    print("REI:",reitime)

                    new_date = endTime + timedelta(hours=int(reitime))
                    expires_on_formatted = new_date.strftime('%B %d, %Y at %I:%M:%S %p')
                    reiExp = expires_on_formatted

                    sql_query = userTask.select_app_geometry_by_appID_query()
                    geometry_result = userTask.execute_select_query_vals(connection, sql_query, [appID])




                    appTimeType = app[10]

                    print("geometry_result:",geometry_result)



                    if not geometry_result:
                        print(f"❌ Error: No geometry found for AppID {appID}")
                        continue

                    geometry = eval(geometry_result[0][0])  # Convert string to Python object

                    sql_query = userTask.select_tank_mix_name_by_tank_mixID_query()
                    tankMixName = userTask.execute_select_query_vals(connection, sql_query, [app[9]])[0][0]

                    sql_query = userTask.select_tank_mix_carrier_by_tank_mixID_query()
                    carrier = userTask.execute_select_query_vals(connection, sql_query, [app[9]])[0]

                    sql_query = userTask.select_tank_mix_products_by_tank_mixID_query()
                    products = userTask.execute_select_query_vals(connection, sql_query, [app[9]])

                    appProperties = {
                        "FarmName": farmName,
                        "FieldName": fieldName,
                        "AppType": appType,
                        "StartTime": str(startTime),
                        "EndTime": str(endTime),
                        "REIExp": reiExp,
                        "TankMixName": tankMixName,
                        "Carrier": carrier,
                        "Products": products,
                        "AppTimeType": appTimeType,
                    }

                    appInstance = { 
                        'type': 'Feature',
                        'id': appID,
                        'properties': appProperties,
                        'geometry': geometry
                    }

                    formatted_apps.append(appInstance)

                except Exception as e:
                    print(f"❌ Exception processing AppID {appID}: {e}")
                    continue

        # Create JSON structure
        jsonFilePath = 'public_html/cgi-bin/misc/json/'
        jsonFileName = f'pestappsJSON_{key}.js'
        jsonFile = os.path.join(jsonFilePath, jsonFileName)

        if not os.path.exists(jsonFilePath):
            print(f"⚠️ Directory '{jsonFilePath}' does not exist. Creating it now...")
            os.makedirs(jsonFilePath, exist_ok=True)  # Creates directory if it does not exist

        try:

            with open(jsonFile, "w") as jsonFileW:
                jsonData = json.dumps({'type': 'FeatureCollection', 'features': formatted_apps}, indent=2)
                jsonFileW.write(jsonData)
            # with open(jsonFile, "w") as jsonFileW:
            #     jsonData = json.dumps({'type': 'FeatureCollection', 'features': []})  # Dummy data for now
            #     jsonFileW.write(jsonData)

            print(f"✅ JSON File Created Successfully: {jsonFile}")
            return jsonFileName
        
        except Exception as e:
            print(f"❌ Exception in createAppJson: {e}")
            return None

    except Exception as e:
        logging.exception(e)
        print(f"❌ Exception in createAppJson: {e}")
        return None































#   ************************************************************
#   ** Debug Function **
#   ************************************************************



def nt_debug_write_file(funct_Str):
    from datetime import datetime

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    time = current_time.replace(':', '')

    save_Path = 'debug_Log'

    # ✅ Check and create directory if missing
    if not os.path.exists(save_Path):
        os.makedirs(save_Path)

    file_name = f'debugSS_Flask_{funct_Str}_{time}.txt'
    file = os.path.join(save_Path, file_name)

    debugFile = open(file, "w")

    return debugFile




#   ************************************************************
#   *** GENERATE EMAIL CONFIRMATIONS ***
#   ************************************************************
def generate_token(email):
    serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])
    return serializer.dumps(email, salt=app.config["SECURITY_PASSWORD_PEPPER"])


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])
    try:
        email = serializer.loads(
            token, salt=app.config["SECURITY_PASSWORD_PEPPER"], max_age=expiration
        )
        return email
    except Exception:
        return False
    
def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=app.config["MAIL_DEFAULT_SENDER"],
    )
    mail = Mail(app)
    mail.send(msg)

#   ************************************************************
#   **** MAIN FLASK PROCEDURE ****
#   ************************************************************


#   ************************************************************
#   *** MAIN PAGE PROCEDURE ***
#   ************************************************************
@app.route('/')
def homePage():
    return render_template('index.html')


#   ************************************************************
#   *** LOGIN PAGE PROCEDURE ***
#   ************************************************************
@app.route('/login')
def loginPage():
    # return render_template('login.html')
    if 'username' in session:
        username = session['username']
        return redirect(url_for('userMain',  username=username))
    else:
        return render_template('login.html')


#   ************************************************************
#   *** LOGOUT PROCEDURE ***
#   ************************************************************
@app.route('/logout')
def logout():
    # logout user and return login.html
    if 'username' in session:
        session.clear()
        #response = make_response(render_template('login.html'))
        #response.set_cookie('username')
        #reponse.set_cookie('json')
        
        #return redirect(url_for('login'))
        #return response
    
    return redirect('/login', code=302)


#   ************************************************************
#   *** SAVE NEW FARM PROCEDURE ***
#   ************************************************************

@app.route('/saveNewFarm', methods=['POST'])
def saveNewFarm():
    # TODO: Add more error handling for bad data, etc?

    username = session['username']
    
    farmName = request.form['farmName']
    farmStatus = request.form['farmStatus']
    farmOrg = request.form['farmOrg']

    connection = userTask.create_db_connection()

    # Check if farm name already exists for this user and organization
    sql_query = userTask.select_farmID_by_username_and_farm_name_query()
    farmID = userTask.execute_select_query_vals(connection, sql_query, [username, farmName])
    if farmID:
        return "Success: False, Duplicate farm name"

    # Get the orgID for the organization name specified and for the user that is currently logged in
    sqlOrgQuery = userTask.select_orgID_by_username_and_org_name_query()
    orgID = userTask.execute_select_query_vals(connection, sqlOrgQuery, [username, farmOrg])[0][0]


    # Insert Farm into the database
    sqlInsertFarmQuery = userTask.insert_Farm()
    vals = [farmName, None, orgID, None, farmStatus]
    insertQueryResponse = userTask.execute_insert_update_delete_query(connection, sqlInsertFarmQuery, vals)

    connection.close()
    # Check if the insert query was successful
    return_message = ""
    if(str(insertQueryResponse).isdigit()):
        saveSuccess = 'True'
        return_message = 'Farm rowID: ' + str(insertQueryResponse)
    else:
        saveSuccess = 'False'
        return_message = str(insertQueryResponse)
    
    return return_message + ' farm saved correctly: ' + saveSuccess


#   ************************************************************
#   *** SAVE NEW FIELD PROCEDURE ***
#   ************************************************************

@app.route('/saveNewField', methods=['POST'])
def saveNewField():

    username = session['username']
    
    farmName = request.form['farmName']
    fieldName = request.form['fieldName']
    geometry = request.form['geometry']

    connection = userTask.create_db_connection()

    # Check if field name already exists on this farm for this user and organization
    sql_query = userTask.select_fieldID_by_username_and_farm_name_and_field_name_query()
    fieldID = userTask.execute_select_query_vals(connection, sql_query, [username, farmName, fieldName])
    if fieldID:
        return "Success: False, Duplicate field name"

    # Get the farmID for the farm name specified and the user that is currently logged in
    sql_query = userTask.select_farmID_by_username_and_farm_name_query()
    farmID = userTask.execute_select_query_vals(connection, sql_query, [username, farmName])[0][0]


    # Insert Farm into the database
    sqlInsertFarmQuery = userTask.insert_Field()
    vals = [fieldName, farmID, None, geometry]
    insertQueryResponse = userTask.execute_insert_update_delete_query(connection, sqlInsertFarmQuery, vals)

    connection.close()
    # Check if the insert query was successful
    return_message = ""
    if(str(insertQueryResponse).isdigit()):
        saveSuccess = 'True'
        return_message = 'Field rowID: ' + str(insertQueryResponse)
    else:
        saveSuccess = 'False'
        return_message = str(insertQueryResponse)
    
    return return_message + ' field saved correctly: ' + saveSuccess



#   ************************************************************
#   *** SAVE NEW APPLICATOR PROCEDURE ***
#   ************************************************************





@app.route('/saveNewApplicator', methods=['POST'])
def saveNewApplicator():
    try:
        username = session.get('username')
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        orgName = request.form.get('orgName')

        connection = userTask.create_db_connection()
        if not connection:
            return jsonify({"success": False, "message": "Database connection failed!"}), 500

        # Get orgID
        sql_query = userTask.select_orgID_by_username_and_org_name_query()
        orgID_result = userTask.execute_select_query_vals(connection, sql_query, [username, orgName])

        print("Org Query Result:", orgID_result)  # Debugging line



        if not orgID_result:
            return jsonify({"success": False, "message": "Organization not found!"}), 400
        orgID = orgID_result[0][0]

        # Check if applicator exists
        sql_query = userTask.select_applicatorID_by_firstName_and_lastName_and_orgID_query()
        applicatorID_result = userTask.execute_select_query_vals(connection, sql_query, [firstName, lastName, orgID])

        print("Executing query:", sql_query, "with values:", [username, orgName])
        print("Current session username:", session.get('username'))



        if applicatorID_result:
            return jsonify({"success": False, "message": "Duplicate applicator name exists!"}), 400

        # Insert Applicator
        sql_query = userTask.insert_Applicator()
        applicatorID = userTask.execute_insert_update_delete_query1(connection, sql_query, [firstName, lastName, None, None, None, None])
        if not applicatorID:
            return jsonify({"success": False, "message": "Error inserting applicator!"}), 500
        
        print("Inserted Applicator ID:", applicatorID)


        # Link Applicator to Organization
        sql_query = userTask.insert_Applicator_Org_Info()
        insertQueryResponse = userTask.execute_insert_update_delete_query(connection, sql_query, [applicatorID, orgID])
        connection.close()

        if str(insertQueryResponse).isdigit():
            return jsonify({"success": True, "message": "Applicator added successfully!"}), 200
        else:
            return jsonify({"success": False, "message": f"Failed to link applicator to org: {insertQueryResponse}"}), 500
    except Exception as e:
        return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500






#   ************************************************************
#   *** SAVE NEW TANK MIX PROCEDURE ***
#   ************************************************************

@app.route('/saveNewTankMix', methods=['POST'])
def saveNewTankMix():

    username = session['username']


    tankMixName = request.form['tankMixName']
    carrierName = request.form['carrierName']
    carrierRate = request.form['carrierRate']
    carrierUnits = request.form['carrierUnits']
    productDetails = json.loads(request.form['productDetails'])


    try:
        connection = userTask.create_db_connection()


        ### Check if tank mix name already exists for this user

        sql_query = userTask.select_tankMixID_by_tankMix_name_and_username_query()
        userID = userTask.execute_select_query_vals(connection, sql_query, [tankMixName, username])
        if(userID):
            return "Success: False, Duplicate tank mix name"


        ### Insert Tank Mix Record
        sql_query = userTask.select_userID_by_username_query()
        userID = userTask.execute_select_query_vals(connection, sql_query, [username])[0][0]


        sql_query = userTask.insert_Tank_Mix()
        tankMixID = userTask.execute_insert_update_delete_query1(connection, sql_query, [tankMixName, userID])

        print("Inserted tankMixID:", tankMixID)



        #if(not tankMixID):
        #    return "Success: False, Failed to insert tank mix"

        
        ### Insert Tank Mix Carrier Record
        sql_query = userTask.select_carrierID_by_carrier_name_query()
        carrierID = userTask.execute_select_query_vals(connection, sql_query, [carrierName])[0][0]
        print("Inserted carrierID:", carrierID)
        sql_query = userTask.insert_Tank_Mix_Carrier()
        tankMixCarrierID = userTask.execute_insert_update_delete_query1(connection, sql_query, [tankMixID, carrierID, carrierRate, carrierUnits])

        print("Inserted tankMixCarrierID:", tankMixCarrierID)


        if(tankMixCarrierID is None):
            return "Success: False, Failed to link carrier with tank mix"

        ### Insert Tank Mix Product Records

        for key in productDetails:
            print(productDetails[key])

            productInfo = productDetails[key]

            productName = productInfo[0]
            productRate = productInfo[1]
            productUnits = productInfo[2]

            sql_query = userTask.select_productID_by_product_name_query()
            productID = userTask.execute_select_query_vals(connection, sql_query, [productName])[0][0]

            print("productID value:", productID)


            sql_query = userTask.insert_Tank_Mix_Product()
            tankMixProductID = userTask.execute_insert_update_delete_query(connection, sql_query, [tankMixID, productID, productRate, productUnits])
            if(tankMixProductID is None):
                return "Success: False, Failed to associate all products with tank mix"

        connection.close()
        return_message = ""
        saveSuccess = 'True'
        return_message = 'TankMix rowID: ' + str(tankMixID)
        return return_message + ' Tank Mix saved correctly: ' + saveSuccess

    except Exception as e:
        logging.exception(e)
        return("Success: False, Something went wrong while inserting Tank Mix")

    
 
#   ************************************************************
#   *** SAVE NEW APPLICATION PROCEDURE ***
#   ************************************************************

@app.route('/saveNewApplication', methods=['POST'])
def saveNewApplication():

    username = session['username']

    farmName = request.form['farmName']
    fieldName = request.form['fieldName']
    applicator = request.form['applicator'].split(", ")

    applicatorLast = applicator[0]
    applicatorSecondPortion = applicator[1].split(" - ")
    applicatorFirst = applicatorSecondPortion[0]
    applicatorOrg = applicatorSecondPortion[1]

    date = request.form['date']
    endTime = request.form['endTime']
    endDateTime = date + "T" + endTime + ":00.000Z"

    tankMixName = request.form['tankMixName']
    appType = request.form['appType']
    equipmentName = request.form['equipmentName']


    try:
        connection = userTask.create_db_connection()

        sql_query = userTask.select_fieldID_by_username_and_farm_name_and_field_name_query()
        fieldID = userTask.execute_select_query_vals(connection, sql_query, [username, farmName, fieldName])[0][0]


        sql_query = userTask.select_orgID_by_username_and_org_name_query()
        orgID = userTask.execute_select_query_vals(connection, sql_query, [username, applicatorOrg])[0][0]

        sql_query = userTask.select_applicatorID_by_firstName_and_lastName_and_orgID_query()
        applicatorID = userTask.execute_select_query_vals(connection, sql_query, [applicatorFirst, applicatorLast, orgID])[0][0]


        sql_query = userTask.select_tankMixID_by_tankMix_name_and_username_query()
        tankMixID = userTask.execute_select_query_vals(connection, sql_query, [tankMixName, username])[0][0]


        sql_query = userTask.select_field_geometry_by_fieldID_query()
        fieldGeometry = userTask.execute_select_query_vals(connection, sql_query, [fieldID])[0][0]


        sql_query = userTask.insert_Application()

        

        vals = [fieldID, applicatorID, tankMixID, None, endDateTime, None, appType, equipmentName, None, None, fieldGeometry]
        insertQueryResponse = userTask.execute_insert_update_delete_query(connection, sql_query, vals)


        connection.close()
        return_message = ""
        if(str(insertQueryResponse).isdigit()):
            saveSuccess = 'True'
            return_message = 'Application rowID: ' + str(insertQueryResponse)


            from random import randint
            key = randint(0,999999)
            jsonFile = createAppJson(username,key)
            session['jsonFile'] = jsonFile

        else:
            saveSuccess = 'False'
            return_message = str(insertQueryResponse)
        
        return return_message + ' application saved correctly: ' + saveSuccess

    except Exception as e:
        logging.exception(e)
        return("Success: False, Something went wrong while saving application")


#   ************************************************************
#   *** EDIT EXISTING APPLICATION PROCEDURE ***
#   ************************************************************

@app.route('/editApplication', methods=['POST'])
def editApplication():

    username = session['username']

    appID = request.form['appID']

    farmName = request.form['farmName']
    fieldName = request.form['fieldName']
    applicator = request.form['applicator'].split(", ")

    applicatorLast = applicator[0]
    applicatorSecondPortion = applicator[1].split(" - ")
    applicatorFirst = applicatorSecondPortion[0]
    applicatorOrg = applicatorSecondPortion[1]

    date = request.form['date']
    endTime = request.form['endTime']
    endDateTime = date + "T" + endTime + ":00.000Z"

    tankMixName = request.form['tankMixName']
    appType = request.form['appType']
    equipmentName = request.form['equipmentName']


    try:
        connection = userTask.create_db_connection()

        sql_query = userTask.select_fieldID_by_username_and_farm_name_and_field_name_query()
        fieldID = userTask.execute_select_query_vals(connection, sql_query, [username, farmName, fieldName])[0][0]


        sql_query = userTask.select_orgID_by_username_and_org_name_query()
        orgID = userTask.execute_select_query_vals(connection, sql_query, [username, applicatorOrg])[0][0]

        sql_query = userTask.select_applicatorID_by_firstName_and_lastName_and_orgID_query()
        applicatorID = userTask.execute_select_query_vals(connection, sql_query, [applicatorFirst, applicatorLast, orgID])[0][0]


        sql_query = userTask.select_tankMixID_by_tankMix_name_and_username_query()
        tankMixID = userTask.execute_select_query_vals(connection, sql_query, [tankMixName, username])[0][0]


        sql_query = userTask.select_field_geometry_by_fieldID_query()
        fieldGeometry = userTask.execute_select_query_vals(connection, sql_query, [fieldID])[0][0]


        sql_query = userTask.update_application_by_appID_query()

        

        vals = [fieldID, applicatorID, tankMixID, None, endDateTime, None, appType, equipmentName, None, None, fieldGeometry, appID]
        queryResponse = userTask.execute_insert_update_delete_query(connection, sql_query, vals)


        connection.close()
        return_message = ""
        if(str(queryResponse).isdigit()):
            saveSuccess = 'True'
            return_message = 'Application rowID: ' + str(queryResponse)


            from random import randint
            key = randint(0,999999)
            jsonFile = createAppJson(username,key)
            session['jsonFile'] = jsonFile

        else:
            saveSuccess = 'False'
            return_message = str(queryResponse)
        
        return return_message + ' application edited correctly: ' + saveSuccess

    except Exception as e:
        logging.exception(e)
        return("Success: False, Something went wrong while editing application")





#   ************************************************************
#   *** DELETE EXISTING APPLICATION PROCEDURE ***
#   ************************************************************

@app.route('/deleteApplication', methods=['POST'])
def deleteApplication():
    username = session['username']
    appID = request.form['appID']

    try:
        connection = userTask.create_db_connection()

        sql_query = userTask.delete_application_by_appID_query()
        queryResponse = userTask.execute_insert_update_delete_query(connection, sql_query, [appID])


        connection.close()
        return_message = ""
        if(str(queryResponse).isdigit()):
            saveSuccess = 'True'
            return_message = 'Application rowID: ' + str(queryResponse)

            from random import randint
            key = randint(0,999999)
            jsonFile = createAppJson(username,key)
            session['jsonFile'] = jsonFile

        else:
            saveSuccess = 'False'
            return_message = str(queryResponse)
        
        return return_message + ' application deleted correctly: ' + saveSuccess

    except Exception as e:
        logging.exception(e)
        return("Success: False, Something went wrong while deleting application")




def date_handler(obj): 
    if isinstance(obj, datetime):
        return obj.isoformat()
    else:
        return None

@app.route('/getApplicationDetailsByID', methods=['GET'])
def getApplicationDetailsByID():
    appID = request.args['appID']
    connection = userTask.create_db_connection()

    sql_query = userTask.select_application_details_by_appID_query()
    applicationDetails = userTask.execute_select_query_vals(connection, sql_query, [appID])

    connection.close()

    result = json.dumps(applicationDetails, default=date_handler)
    return result



#   ************************************************************
#   *** Check if the logged in user has edit access ***
#   ************************************************************
@app.route('/checkEditAccess')
def checkEditAccess():
    return jsonify(session['hasEditAccess'])




#   ************************************************************
#   *** USER MAIN LOAD PROCEDURE ***
#   ************************************************************










@app.route('/userMain')
def userMain():
    if 'username' not in session:
        print("❌ Error: User not logged in, redirecting to login page")
        return redirect(url_for('login'))

    username = session['username']
    print(f"✅ User '{username}' logged in successfully")

    key = random.randint(1000, 9999)
    jsonFile = createAppJson(username, key)

    if jsonFile:
        print(f"✅ Storing JSON file in session: {jsonFile}")
        session['jsonFile'] = jsonFile  # ✅ Ensure JSON filename is stored in session
    else:
        print("❌ Error: JSON file was not created")
        session['jsonFile'] = None  # Prevent 'None' error

    connection = userTask.create_db_connection()
    sql_query = userTask.select_userID_by_username_query()
    userID = userTask.execute_select_query_vals(connection,sql_query,[username])[0][0]
    sql_query = userTask.select_organization_owner_by_userID_query()
    orgowner = userTask.execute_select_query_vals(connection,sql_query,[userID])[0][0]

    return render_template('user_Main.html', orgowner=orgowner)
    #return render_template('user_Main.html', username=username)




















#   ************************************************************
#   *** GET DROPDOWN DATA FOR ADD APPLICATION MODAL PROCEDURES *
#   ************************************************************
@app.route('/getAllFarmNames', methods=['GET'])
def getAllFarmNames():
    username = session['username']
    connection = userTask.create_db_connection()

    sql_query = userTask.select_all_farm_names_by_username_query()
    all_farm_names = userTask.execute_select_query_vals(connection, sql_query, [username])

    connection.close()

    result = json.dumps(all_farm_names)
    return result


@app.route('/getAllFieldNames', methods=['GET'])
def getAllFieldNames():

    username = session['username']
    farmName = request.args['farmName']
    connection = userTask.create_db_connection()

    sql_query = userTask.select_all_field_names_by_farm_name_and_username_query()
    all_field_names = userTask.execute_select_query_vals(connection, sql_query, [username, farmName])

    connection.close()

    result = json.dumps(all_field_names)
    return result


@app.route('/getAllOrgNames', methods=['GET'])
def getAllOrgNames():

    username = session['username']
    connection = userTask.create_db_connection()

    sql_query = userTask.select_all_org_names_by_username_query()
    all_org_names = userTask.execute_select_query_vals(connection, sql_query, [username])

    connection.close()

    result = json.dumps(all_org_names)
    return result


@app.route('/getAllApplicatorNames', methods=['GET'])
def getAllApplicatorNames():

    username = session['username']
    connection = userTask.create_db_connection()

    sql_query = userTask.select_all_applicator_names_by_username_query()
    all_applicator_names = userTask.execute_select_query_vals(connection, sql_query, [username])

    connection.close()

    result = json.dumps(all_applicator_names)
    return result


@app.route('/getAllTankMixNames', methods=['GET'])
def getAllTankMixNames():
    connection = userTask.create_db_connection()
    username = session['username']

    sql_query = userTask.select_all_tank_mix_names_by_username_query()
    all_tank_mix_names = userTask.execute_select_query_vals(connection, sql_query, [username])

    connection.close()

    result = json.dumps(all_tank_mix_names)
    return result



@app.route('/getAllCarrierNames', methods=['GET'])
def getAllCarrierNames():
    connection = userTask.create_db_connection()

    sql_query = userTask.select_all_carrier_names_query()
    all_carrier_names = userTask.execute_select_query(connection, sql_query)
    result = json.dumps(all_carrier_names)
    return result




@app.route('/getREIExpiration', methods=['GET'])
def getREIExpiration():
    connection = userTask.create_db_connection()
    sql_query = userTask.select_product_name_and_tank_mix_query()
    all_tank_mix_names = userTask.execute_select_query_vals(connection, sql_query, [session['username']])

    connection.close()

    result = json.dumps(all_tank_mix_names)
    return result


@app.route('/getAllProductNames', methods=['GET'])
def getAllProductNames():
    connection = userTask.create_db_connection()

    sql_query = userTask.select_all_product_names_query()
    all_product_names = userTask.execute_select_query(connection, sql_query)

    connection.close()

    result = json.dumps(all_product_names)
    return result








#   ************************************************************
#   *** USER MAIN POST/GET PROCEDURE ***
#   ************************************************************
@app.route('/userMain/dataLinkConnect', methods=['POST', 'GET'])
def userMain_DataLink():
    debugFile = nt_debug_write_file("datalinkConnect_Exception")

    import urllib.parse

    # Debug Start #
    if debug == True:
        file = nt_debug_write_file("userMain_Post")  # nt
        file.write("start of procedure:" + "\n")  # nt
    # Debug End #

    try:
        if request.method == 'POST':
            # Debug Start #
            if debug == True:
                file.write("start of post:" + "\n")  # nt
            # Debug End #

            acctType = request.form.get('accountType')

            # Debug Start #
            if debug == True:
                file.write("acctType: " + repr(acctType) + "\n")  # nt
            # Debug End #

            #username = request.form['usernameLbl']
            #username = request.cookies.get('username')
            username = session['username']

            # Debug Start #
            if debug == True:
                file.write("username: " + repr(username) + "\n")  # nt
            # Debug End #

            if acctType == '2':  # john deere operations center
                #redirect_Url = 'http://127.0.0.1:5000/jdaccess/?username=' + username
                #redirect_Url = 'http://jd-test.spray-safely.test:5000/jdaccess/?username=' + username
                redirect_Url = 'https://johndeere.spray-safely.com/' + username
                #redirect_Url = 'https://johndeere.spray-safely.com/'

                # Debug Start #
                if debug == True:
                    file.write("redirect Url: " +
                               repr(redirect_Url) + "\n")  # nt
                # Debug End #

                #response = make_response(redirect(redirect_Url))
                #response.set_cookie('username', username)
                # return response
                return redirect(redirect_Url, code=302)
            # Debug Start #
            if debug == True:
                file.close()
            # Debug End #

    except Exception as e:
        logging.exception(e)
        # Debug Start #
        if debug == True:
            debugFile.write("error - " + repr(e) + "\n")
            debugFile.close()
        # Debug End #

        
 



@app.route('/getAppJson', methods=['GET'])
def getAppJson():
    jsonFileName = session.get('jsonFile')

    if not jsonFileName:
        print("❌ Error: No JSON file found in session")
        return jsonify({"error": "No JSON file found"}), 400

    jsonDir = os.path.join("public_html/cgi-bin/misc/json/", jsonFileName)

    if not os.path.exists(jsonDir):
        print(f"❌ Error: JSON file does not exist: {jsonDir}")
        return jsonify({"error": "JSON file does not exist"}), 400

    try:
        with open(jsonDir, "r") as fileJSON:
            jsonData = json.load(fileJSON)
            return jsonify(jsonData)

    except Exception as e:
        print(f"❌ Error reading JSON file: {e}")
        return jsonify({"error": "Failed to read JSON"}), 500





















@app.route('/invitePage')
def inviteUserPage():
    return render_template('invite.html')

@app.route('/changePasswordPage')
def changePasswordPage():
    return render_template('changePassword.html')




from werkzeug.security import generate_password_hash, check_password_hash
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)  # Initialize Flask-Bcrypt


    
@app.route('/changePassword', methods=['POST', 'GET'])
def changePassword():
    try:
        message = None
        messagefail = None

        form = request.form
        currentPassword = form['current password']
        newPassword = form['password']

        connection = userTask.create_db_connection()

        username = session['username']
        sql_query = userTask.select_userID_by_username_query()
        userID = userTask.execute_select_query_vals(connection, sql_query, [username])[0][0]

        # Get hashed password from database
        sql_query = userTask.check_password_by_user_id_query()
        stored_hashed_password = userTask.execute_select_query_vals(connection, sql_query, [userID])[0][0]

        print("Stored Hashed Password:", stored_hashed_password)

        # Determine hash type and verify password
        if stored_hashed_password.startswith("$2b$"):  # Bcrypt format
            password_valid = bcrypt.check_password_hash(stored_hashed_password, currentPassword)
        else:  # Werkzeug format
            password_valid = check_password_hash(stored_hashed_password, currentPassword)

        if password_valid:
            # Hash the new password before storing it (Always use bcrypt for new passwords)
            hashed_new_password = bcrypt.generate_password_hash(newPassword).decode('utf-8')

            sql_query = userTask.update_UserPassword_byID()
            userTask.execute_insert_update_delete_query(connection, sql_query, [hashed_new_password, userID])

            # ✅ Redirect to login page with success message
            flash("✅ Password successfully changed, please log in with new password.", "success")
            return redirect(url_for("loginPage"))
        else:
            messagefail = "❌ Incorrect current password"

    except Exception as e:
        messagefail = "❌ Something went wrong: " + repr(e)

    finally:
        if connection:
            connection.close()

    # Return to the change password page if there's an error
    return render_template("changePassword.html", form=form, message=messagefail)






    
@app.route('/invite', methods=['POST', 'GET'])
def inviteUser():
    import random
    
    message=None
    messagefail=None
    try:
        form = request.form
        
        connection = userTask.create_db_connection()
        sql_query = userTask.select_userID_by_username_query()
        
        try:
            emailalreadysent = userTask.execute_select_query_vals(connection,sql_query,[form['email']])[0][0]
            print("emailalreadysent:",emailalreadysent)
            if emailalreadysent > 0:
                emailalreadysent = True
        except Exception as e:
            emailalreadysent = False
            
        if(emailalreadysent is False):
            
            editaccess = form['checkbox']
            
            #GENERATE PASSWORD AND STORE CREDENTIALS TO DATABASE
            characters = string.ascii_letters + string.digits + '!@#$%^&*()'
            password = ''.join(random.choice(characters) for i in range(12))
            

             # ✅ **Hash the Password** before storing it in the database
            hashed_password = generate_password_hash(password)

            token = generate_token(form['email'])
            passwordtoken = generate_token(password)
            confirm_url = url_for("loginPageConfirmation", token=token, _external=True)
            html = render_template("emailinvite.html", confirm_url=confirm_url, password=password)
            subject = "Please confirm your email"
            
            
            
            send_email(form['email'], subject, html)
        
            
            sql_query = userTask.insert_User()
            
            
           
            if editaccess == '1':
                userTask.execute_insert_update_delete_query(connection,sql_query,[form['email'],form['email'],hashed_password,'Active','1','0','0'])
            else:
                userTask.execute_insert_update_delete_query(connection,sql_query,[form['email'],form['email'],hashed_password,'Active','0','0','0'])
                
        

            if not connection or not connection.is_connected():
                print("⚠️ Connection lost. Reconnecting...")
                connection = userTask.create_db_connection()

            cursor = connection.cursor()
            sql_query1 = """
                SELECT SQL_NO_CACHE User_ID 
                FROM User_Info 
                WHERE Email = %s;
            """
    
            cursor.execute(sql_query1, (form['email'],))
            newaccuserid_result = cursor.fetchone()  # Fetch only one result

            if newaccuserid_result:
                newaccuserid = newaccuserid_result[0]  # Extract the `User_ID`
                print(f"✅ New User ID Retrieved: {newaccuserid}")
            else:
                print("❌ Error: User ID not found for the given email.")
                return render_template("invite.html", message="❌ User not found in database.")
            

            if not connection or not connection.is_connected():
                print("⚠️ Connection lost. Reconnecting...")
                connection = userTask.create_db_connection()

            cursor = connection.cursor()

            # SQL Query to Fetch Org_ID
            sql_query = """
                SELECT SQL_NO_CACHE c.Org_ID 
                FROM User_Info AS a 
                JOIN User_Org_Info AS b ON a.User_ID = b.User_ID
                JOIN Org_Info AS c ON b.Org_ID = c.Org_ID
                WHERE a.Username = %s AND c.Org_Name = %s;
            """

            cursor.execute(sql_query, (session.get('username'), form.get('organizationName')))
            orgID_result = cursor.fetchone()

            if orgID_result:
                orgID = orgID_result[0]
                print(f"✅ Organization ID Retrieved: {orgID}")
            else:
                print("❌ Organization not found. Check the organization name.")
                return render_template("invite.html", message="❌ Organization not found.")
                    
            
            
            

            
            sql_query = userTask.insert_UserOrg()
            result = userTask.execute_insert_update_delete_query(connection,sql_query,[newaccuserid,orgID])
            
            message = 'Email Successfully Sent'
            return redirect(url_for("loginPage"))
        else:
            messagefail = "User is already registered, or hasn't confirmed email"
    except Exception as e:
        messagefail = "Something went wrong:" + repr(e)
    
    connection.close()
    
    return render_template("invite.html", form=form, message=messagefail)
    #return render_template("invite.html", form=form, successmessage=message, message=messagefail)


























    
@app.route('/confirm/<token>')
def loginPageConfirmation(token):
    email = confirm_token(token)
    if not email:
        return render_template("login.html", message="Invalid or expired confirmation link!")

    connection = userTask.create_db_connection()
    sql_query = userTask.select_userID_by_username_query()
    user_record = userTask.execute_select_query_vals(connection, sql_query, [email])

    if not user_record:
        return render_template("login.html", message="User not found!")

    user_id = user_record[0][0]
    sql_update = userTask.update_IsConfirmed_query()
    userTask.execute_insert_update_delete_query(connection, sql_update, [1, user_id])

    connection.close()
    return redirect("/login", code=302)


@app.route('/getOrganizationNames', methods=['GET','POST'])
def getOrgNames():
    connection = userTask.create_db_connection()
    username = session['username']
    
    sql_query = userTask.select_all_org_names_by_username_query()
    all_org_names = userTask.execute_select_query_vals(connection, sql_query,[username])
    

    connection.close()

    result = json.dumps(all_org_names)
    return result


#   ************************************************************
#   *** USER LOGIN AND CREATE NEW USER PROCEDURE ***
#   ************************************************************


from flask import request, render_template, session, redirect, url_for
import logging



from flask import flash  # Import flash for messages

@app.route("/user/create", methods=["POST"])
def create_user():
    try:
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        new_org = request.form.get("new_org")  # "yes" or "no"

        if not username or not email or not password:
            flash("⚠️ All fields are required.", "warning")
            return redirect(request.referrer)  # Stay on the same page

        # ✅ Ensure database connection is available before proceeding
        connection = userTask.create_db_connection()
        if not connection:
            flash("❌ Database Connection Failed.", "danger")
            return redirect(request.referrer)

        # ✅ Check if the username or email already exists
        sql_query = userTask.select_userID_by_username_query()
        existing_user = userTask.execute_select_query_vals(connection, sql_query, [username])
        if existing_user:
            flash("❌ Username already taken.", "danger")
            return redirect(request.referrer)

        sql_query = userTask.select_userID_by_email_query()
        existing_email = userTask.execute_select_query_vals(connection, sql_query, [email])
        if existing_email:
            flash("❌ Email is already registered.", "danger")
            return redirect(request.referrer)

        # ✅ Hash the password
        hashed_password = generate_password_hash(password)

        # ✅ Insert the new user and get User_ID
        user_id = userTask.create_user(connection, username, email, hashed_password)

        if not user_id or not isinstance(user_id, int):  # Ensure it's a valid integer
            flash("❌ Error: User could not be created.", "danger")
            return redirect(request.referrer)

        print(f"✅ User created successfully with ID: {user_id}")

        # ✅ If the user is creating a new organization
        if new_org == "yes":
            # ✅ Create a new organization
            new_org_id = userTask.insert_org(connection, f"{username}'s Organization")

            if not new_org_id:
                flash("❌ Failed to create organization.", "danger")
                return redirect(request.referrer)

            # ✅ Link the user to the organization as an Org Owner
            sql_query = userTask.insert_UserOrg()
            userTask.execute_insert_update_delete_query(connection, sql_query, [user_id, new_org_id])

            print(f"✅ Organization created with ID: {new_org_id} and assigned to user {user_id}")

        else:
            # ✅ If the user is not creating an org, prevent sign-up & show message
            flash("⚠️ You must be invited by an existing Organization Owner.", "warning")
            return redirect(request.referrer)

        # ✅ Ensure the connection is properly closed before redirecting
        connection.close()
        flash("✅ Account created successfully! You can now log in.", "success")
        return redirect(url_for("loginPage"))

    except Exception as e:
        logging.exception(e)
        flash(f"⚠️ An unexpected error occurred: {e}", "danger")
        return redirect(request.referrer)

    finally:
        if connection:
            connection.close()  # ✅ Ensure database connection is closed properly






@app.route('/userlogin', methods=['POST'])
def userLogin():
    try:
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            return render_template('login.html', message="⚠️ Email and Password are required.")

        connection = userTask.create_db_connection()
        if not connection:
            return render_template('login.html', message="❌ Database Connection Failed.")

        # Fetch user details from the database
        sql_query = userTask.select_hashed_password_query()
        user_result = userTask.execute_select_query_vals(connection, sql_query, [email])

        if not user_result:
            return render_template('login.html', message="❌ Incorrect Email or Password.")

        userID, stored_hashed_password = user_result[0]

        # 🔹 Detect if stored hash is bcrypt (bcrypt hashes start with "$2b$")
        if stored_hashed_password.startswith("$2b$"):
            password_valid = bcrypt.check_password_hash(stored_hashed_password, password)
        else:
            # 🔹 Fallback to werkzeug security hash check (for old users)
            password_valid = check_password_hash(stored_hashed_password, password)

        if not password_valid:
            return render_template('login.html', message="❌ Incorrect Email or Password.")

        # Check if email is confirmed
        sql_query = userTask.select_is_confirmed_by_userID_query()
        is_confirmed = userTask.execute_select_query_vals(connection, sql_query, [userID])[0][0]

        if is_confirmed != 1:
            return render_template('login.html', message="⚠️ User has not confirmed Email Address.")

        # Fetch username and access level
        sql_query = userTask.select_username_and_access_level_by_userID_query()
        username_access = userTask.execute_select_query_vals(connection, sql_query, [userID])

        if username_access:
            username, edit_access = username_access[0]
            session['username'] = username
            session['hasEditAccess'] = edit_access
            return redirect(url_for('userMain', username=username))

        return render_template('login.html', message="⚠️ An unexpected error occurred. Please try again.")

    except Exception as e:
        logging.exception(e)
        return render_template('login.html', message="⚠️ An unexpected error occurred.")
















def generate_temp_password():
    """Generate a random temporary password"""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(10))

@app.route("/forgotPassword")
def forgot_password():
    return render_template("forgotPassword.html")


from flask_mail import Mail, Message
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)
# Initialize Flask-Mail with the app's config
mail = Mail(app)

@app.route("/sendPasswordReset", methods=["POST"])
def send_password_reset():
    email = request.form["email"]

    # Create a database connection
    connection = userTask.create_db_connection()
    if not connection:
        flash("Database connection failed!", "error")
        return redirect("/forgotPassword")

    # Check if the email exists in the database
    user_query = userTask.select_user_by_email_query()
    user = userTask.execute_select_query_vals(connection, user_query, [email])

    if not user:
        flash("Email not found. Please enter a registered email.", "error")
        return redirect("/forgotPassword")

    # Generate a temporary password
    def generate_temp_password():
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(10))

    temp_password = generate_temp_password()

    # Hash the temporary password before storing it
    hashed_password = bcrypt.generate_password_hash(temp_password).decode('utf-8')

    # Update the database with the new hashed password
    update_query = userTask.update_user_password_query()
    userTask.execute_insert_update_delete_query(connection, update_query, [hashed_password, email])

    # Construct the email message
    subject = "Password Reset - Spray Safely"
    body = f"Your temporary password is: {temp_password}\n\nPlease log in and change it immediately."

    try:
        msg = Message(subject, recipients=[email])
        msg.body = body
        mail.send(msg)

        flash("Temporary password sent to your email.", "success")
        return redirect("/")

    except Exception as e:
        flash(f"Failed to send email: {e}", "error")
        return redirect("/forgotPassword")

    finally:
        connection.close()