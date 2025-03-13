import base64
import datetime
import json
import uuid
import logging
import http
import sys
import os
import math
#import ntsqltasks.userdbTasks as userTask
#import ntsqltasks.appdbTasks as appTask
#from ntsqltasks import userdbTasks_pcorg as userTask
#from ntsqltasks import appdbTasks_pcorg as appTask
from ntsqltasks import userdbTasks as userTask
from ntsqltasks import appdbTasks as appTask
#import pntbound.boundGen as boundary
from pntbound import boundGen as boundary
import zipfile
import shapefile
import shapely.geometry
import requests
import urllib.parse
import mysql.connector

from time import sleep
from io import BytesIO
from flask import Flask, render_template, request, redirect, session, make_response,Blueprint

#app = Blueprint('johndeere',__name__, subdomain="jd-test")
jd_app = Flask(__name__)
jd_app.secret_key = "jdss88"

SERVER_URL='http://127.0.0.1:5000'
#SERVER_URL='http://spray-safely.co
#SERVER_URL='http://jd-test.spray-safely.test:5000'
#SERVER_URL='https://myjohndeere.deere.com/mjd/my/login'

#DEBUG MODE - true = enabled ; false = disabled
debug = True


settings = {
    'apiUrl': 'https://sandboxapi.deere.com/platform',
    'clientId': '0oavn0rxbVDnQyEYd5d6',
    'clientSecret': 'ss5sefpFEJd0HhnhZZEpVVog7zkIPqIlI5oWqfOr',
    'wellKnown': 'https://signin.johndeere.com/oauth2/aus78tnlaysMraFhC1t7/.well-known/oauth-authorization-server',
    'callbackUrl': f"{SERVER_URL}/callback",
    'orgConnectionCompletedUrl': SERVER_URL,
    'scopes': 'ag3 eq2 files offline_access',
    'state': uuid.uuid1(),
    'idToken': '',
    'accessToken': '',
    'refreshToken': '',
    'apiResponse': '',
    'accessTokenDetails': '',
    'exp': ''
}


#   *   *   *   *   *   *   *   *   *   *   Local API Procedures   *   *   *   *   *   *   *   *   *   *
def populate(data):
    settings['clientId'] = data['clientId']
    settings['clientSecret'] = data['clientSecret']
    settings['wellKnown'] = data['wellKnown']
    settings['callbackUrl'] = data['callbackUrl']
    settings['scopes'] = data['scopes']
    settings['state'] = data['state']


#   *   *   *   *   *   *   *   *   *   *   Local DB Procedures   *   *   *   *   *   *   *   *   *   *
def check_JDOrgInfo_entry(ssOrgID,jdOrgID):
    # ****Debug Start****
    if(debug):
        file = nt_debug_write_file('checkJDOrgInfoEntry')
        file.write('checkEntry: '+ "\n")
    # ****Debug End****
    
    #UPDATED
    #THIS ORIGINALLY HAD SSORGID AND JDORGID
    sql = userTask.select_jd_org_name_by_orgID_and_JD_API_org_ID_query()
    
    # ****Debug Start****
    if(debug):
        file.write('sql - ' + str(sql) + "\n")
    # ****Debug End****
    
    #UPDATED
    #THIS ORIGINALLY HAD SSORGID AND JDORGID
    query = userTask.execute_select_query_vals(userTask.create_db_connection() ,sql,[ssOrgID,jdOrgID])
    
    # ****Debug Start****
    if(debug):
        file.write('query - ' + str(query) + "\n")
    # ****Debug End****
    
    if(len(query)<1):
        vals = (str(ssOrgID),str(jdOrgID),'','','','','','','')
        sqlInsert = userTask.insert_JDOrg()
        
        # ****Debug Start****
        if(debug):
            file.write('sql Insert - ' + str(sqlInsert) + "\n")
        # ****Debug End****
        

        entry = userTask.execute_insert_update_delete_query(userTask.create_db_connection(),sqlInsert,vals)
        
        # ****Debug Start****
        if(debug):
            file.write('entry - ' + str(entry) + "\n")
            file.write("\n" + 'insert entry ' + "\n")
        # ****Debug End****
        
    #UPDATED
    #ORIGINALLY WAS selectJDOrgName(ssOrgID,JDOrgID)
    sql = userTask.select_jd_org_name_by_orgID_and_JD_API_org_ID_query()
    
    # ****Debug Start****
    if(debug):
        file.write('sql - ' + str(sql) + "\n")
    # ****Debug End****
    
    #UPDATED
    query = userTask.execute_select_query_vals(userTask.create_db_connection(),sql,[ssOrgID,jdOrgID])
    
    # ****Debug Start****
    if(debug):
        file.write('query - ' + str(query) + "\n")
        file.close()
    # ****Debug End****    
        

def update_token_info(res,username=None):
  #Store Information to system Memory
    json_response = res.json()
    token = json_response['access_token']
    settings['accessToken'] = token
    settings['refreshToken'] = json_response['refresh_token']
    settings['exp'] = str(datetime.datetime.now() + datetime.timedelta(seconds=json_response['expires_in']))
    (header, payload, sig) = token.split('.')
    payload += '=' * (-len(payload) % 4)
    settings['accessTokenDetails'] = json.dumps(json.loads(base64.urlsafe_b64decode(payload).decode()), indent=4)
  #Store Token Information to User Database
    # ****Debug Start****
    if(debug):
        file = nt_debug_write_file('updateToken')
        file.write('jsonReponse: ' + repr(json_response) + "\n")
        file.write('username - ' + repr(username) + "\n")
    # ****Debug End****
    if username==None:
        username = session['username']
    
    accLvl = settings['scopes']
    tokenID = settings['idToken']
    accToken = settings['accessToken']
    refToken = settings['refreshToken']
    tokenExp = settings['exp']
    
    # ****Debug Start****
    if(debug):
        file.write('username: ' + repr(username) + "\n")
        file.write('accLvl: ' + repr(accLvl) + "\n")
        file.write('tokenID: ' + repr(tokenID) + "\n")
        file.write('accToken: ' + repr(accToken) + "\n")
        file.write('refToken: ' + repr(refToken) + "\n")
        file.write('tokenExp: ' + repr(tokenExp) + "\n")
    # ****Debug End****
    
    if username:
        #call for user identification query string
        userID_query = userTask.select_userID_by_username_query()
        #obtain user identification
        userID = userTask.execute_select_query_vals(userTask.create_db_connection(),userID_query,[username])
        
        # ****Debug Start****
        if (debug):
            file.write('userID: ' + repr(userID[0][0]) + "\n")
        # ****Debug End****
        
        #UPDATED FROM userTask.select_OrgID
        #call for organization identification query string
        orgID_query = userTask.select_OrgID_From_User_Org_Info()
        
        # ****Debug Start****
        if (debug):
            file.write('orgID_query: ' + repr(orgID_query) + "\n")
	    # ****Debug End****
	
        #UPDATED
        #obtain organization identification
        orgid = userTask.execute_select_query_vals(userTask.create_db_connection(),orgID_query,[str(userID[0][0])])
        # ****Debug Start****
        if (debug):
            file.write('orgID: ' + repr(orgID) + "\n")
	    # ****Debug End****
        orgID = orgid[0][0]

        # ****Debug Start****
        if (debug):
            file.write('orgID: ' + repr(orgID) + "\n")
        # ****Debug End****
        if orgID > 0:
            #UPDATED
            orgUpdate_query = userTask.update_JDAccess()
            
            # ****Debug Start****
            if (debug):
                file.write('orgUpdateQuery: ' + repr(orgUpdate_query) + "\n")
            # ****Debug End****
            
            #UPDATED
            userTask.execute_create_query_vals(userTask.create_db_connection(),orgUpdate_query,[accLvl,tokenID,accToken,refToken,tokenExp,str(orgID)])
        else:
            return 'no organization id acquired'
        
        # ****Debug Start****
        if (debug):
            file.close()
        # ****Debug End****
        
    else:
        return 'no username for available'


def update_jdOrgInfo(res, orgid):
    orgList =[]                             #list of organizations user has access to
    orgID = orgid
    # ****Debug Start****
    if (debug):
        file = nt_debug_write_file("update-orgInfo")
        file.write("update-orgInfo: " + "\n")  
        file.write("res - " + repr(res) + "\n")
        file.write("orgID - " + repr(orgID) + "\n")
    # ****Debug End****
    json_response = res.json()
    values = json_response['values']
    cnt = 0
    # ****Debug Start****
    if (debug):
        file.write("jsonResponse - " + repr(json_response) + "\n")
        file.write("values - " + repr(values) + "\n")
    # ****Debug End****
    for val in values:
        orgDict={}
        jdOrgID = val['id']
        jdOrgName = val['name']
    #    jdOrgType = val['links'][0]['rel']
        # ****Debug Start****
        if (debug):
            file.write("jdOrgID - " + repr(jdOrgID) + "\n")
            file.write("jdOrgName - " + repr(jdOrgName) + "\n")
            #file.write("jdOrgType - " + repr(jdOrgType) + "\n")
        # ****Debug End****
        #if org is main(self) then set jd org info in jd org info table
        if cnt == 0:
            orgType = 'Main'
        else:
            orgType = 'Connected'
        
        # ****Debug Start****
        if (debug):
            file.write("orgType - " + repr(orgType) + "\n")
        # ****Debug End****
        
        connection = userTask.create_db_connection()
        #check for entry
        check_JDOrgInfo_entry(str(orgID),str(jdOrgID))
        
        
        #UPDATED From select_JDOrgID(str(orgID),str(jdOrgID))
        #query if org already exists
        jdOrgID_query = userTask.select_jd_org_ID_by_orgID_and_JD_API_org_ID_query()
        #UPDATED
        jdOrg = userTask.execute_select_query_vals(connection,jdOrgID_query,[str(orgID),str(jdOrgID)])
        
        # ****Debug Start****
        if (debug):
            file.write("jdOrgID_query - " + repr(jdOrgID_query) + "\n")
            file.write("jdOrg - " + repr(jdOrg) + "\n")
            file.write("jdOrg Length - " + repr(len(jdOrg)) + "\n")
        # ****Debug End****
        
        if len(jdOrg) == 0:
            # ****Debug Start****
            if (debug):
                file.write("true"+"\n")
            # ****Debug End****
            
            #fetch sql query
            jdOrgInfo_query = userTask.insert_JDOrg()
            
            # ****Debug Start****
            if (debug):
                file.write("jdOrgInfo_query - " + repr(jdOrgInfo_query) + "\n")
            # ****Debug End****
            
            #set values to be passed
            vals = (str(orgID),str(jdOrgID),jdOrgName,orgType)
            #execute sql query
            userTask.execute_insert_update_delete_query(connection,jdOrgInfo_query,vals)            
        else:
            # ****Debug Start****
            if (debug):
                file.write("false"+"\n")
            # ****Debug End****
            
            #UPDATED
            #fetch sql query
            #was userTask.update_JDOrgName(str(jdOrgName),str(orgID))
            jdOrgName_query = userTask.update_JDOrgName()
            #was update_JDOrgID(str(jdOrgID),str(orgID))
            jdOrgID_query = userTask.update_jd_api_org_ID()
            #was userTask.update_JDOrgType(str(orgType),str(orgID),str(jdOrgID))
            jdOrgType_query = userTask.update_JDOrgType()
            
            # ****Debug Start****
            if (debug):
                file.write("jdOrgName_query - " + repr(jdOrgName_query) + "\n")
                file.write("jdOrgID_query - " + repr(jdOrgID_query) + "\n")
                file.write("jdOrgType_query - " + repr(jdOrgType_query) + "\n")
            # ****Debug End****
            
            #UPDATED
            #execute sql query
            userTask.execute_create_query_vals(connection,jdOrgName_query,[str(jdOrgName),str(orgID)])
            userTask.execute_create_query_vals(connection,jdOrgID_query,[str(jdOrgID),str(orgID)])
            userTask.execute_create_query_vals(connection,jdOrgType_query,[str(orgType),str(orgID),str(jdOrgID)])

        orgDict = {'jdOrgID': jdOrgID, 'jdOrgName':jdOrgName, 'jdOrgType':orgType}
        orgList.append(orgDict)
        cnt = cnt + 1
    
    # ****Debug Start****
    if (debug):
        file.write("orgList - " + repr(orgList) + "\n")
        file.close
    # ****Debug End****
    
    #return True
    return orgList

def update_jdSubInfo(res, orgid, jdOrgID):
    orgID = orgid
  #Parse Response
    subFilters = res['filters']
    subID = res['id']
    subName = res['displayName']
    subClientKey = res['clientKey']
    subToken = res['token']
    filterString = '"' + str(subFilters) + '"'
    # ****Debug Start****
    if (debug):
        file = nt_debug_write_file("update-SubInfo")
        file.write("update-SubInfo: " + "\n")  
        file.write("jdOrgID - " + repr(jdOrgID) + "\n")
        file.write("orgID - " + repr(orgID) + "\n")
        file.write("subID - " + repr(subID) + "\n")
        file.write("subName - " + repr(subName) + "\n")
        file.write("subClientKey - " + repr(subClientKey) + "\n")
        file.write("subToken - " + repr(subToken) + "\n")
        file.write("subFilters - " + str(subFilters) + "\n")
        file.write("filterString - " + filterString + "\n" )
    # ****Debug End****
    connection = userTask.create_db_connection()
  #Post data to jd_OrgInfo database
    #UPDATED
    sqlPost = userTask.update_JDSubToken()
    userTask.execute_create_query_vals(connection,sqlPost,[str(subToken),str(orgID),str(jdOrgID)])
    # ****Debug Start****
    if (debug):
        file.write("token Query - " + repr(sqlPost) + "\n")
    # ****Debug End****
    sqlPost=''
    sqlPost = userTask.update_JDSubClientKey()
    userTask.execute_create_query_vals(connection,sqlPost,[str(subClientKey),str(orgID),str(jdOrgID)])
    # ****Debug Start****
    if (debug):
        file.write("clientKey Query - " + repr(sqlPost) + "\n")
    # ****Debug End****
    #UPDATED
    sqlPost=''
    sqlPost = userTask.update_JDSubName()
    userTask.execute_create_query_vals(connection,sqlPost,[str(subName),str(orgID),str(jdOrgID)])
    # ****Debug Start****
    if (debug):
        file.write("name Query - " + repr(sqlPost) + "\n")
    # ****Debug End****
    #UPDATED
    sqlPost=''
    sqlPost = userTask.update_JDSubID()
    userTask.execute_create_query_vals(connection,sqlPost,[str(subID),str(orgID),str(jdOrgID)])
    # ****Debug Start****
    if (debug):
        file.write("id Query - " + repr(sqlPost) + "\n")
    # ****Debug End****
    #UPDATED I THINK NOT SURE ABOUT FILTER STRING
    sqlPost=''
    sqlPost = userTask.update_JDSubFilters()
    userTask.execute_create_query_vals(connection,sqlPost,[filterString,str(orgID),str(jdOrgID)])
    # ****Debug Start****
    if (debug):
        file.write("filters Query - " + str(sqlPost) + "\n")
    # ****Debug End****    
    sqlPost=''


#
def update_farm_info(farms, jdOrgID, orgid):
    orgID = orgid
    # ****Debug Start****
    if (debug):
        file = nt_debug_write_file("update-farmInfo")
        file.write("update-farmInfo: " + "\n")  
        file.write("farms - " + repr(farms) + "\n")
        file.write("jdOrgID - " + repr(jdOrgID) + "\n")
        file.write("orgID - " + repr(orgID) + "\n")
    # ****Debug End****

    values = farms['values']
    farmDict = {}
    farmList = []
    
    #extract info from json variable
    for val in values:
        jdFarmID = val['id']
        jdFarmName = val['name']
        
        # ****Debug Start****
        if (debug):
            file.write("jdFarmID - " + repr(jdFarmID) + "\n")
            file.write("jdFarmName - " + repr(jdFarmName) + "\n")
        # ****Debug End****
        
    #insert entry into database    
        
        connection = userTask.create_db_connection()

        #UPDATED
        #query database for entry existence
        #MEETING 4/12/2023
        farmEntry_query = userTask.select_FarmInstance()
        farmEntry = userTask.execute_select_query_vals(connection,farmEntry_query,[str(orgID),str(jdOrgID),str(jdFarmID)])
        # ****Debug Start****
        if (debug):
            file.write("farmEntry - " + repr(farmEntry) + "\n")
            file.write("farmEntry Len - " + repr(len(farmEntry)) + "\n")
        # ****Debug End****
        
        #check query for instance
        if len(farmEntry) == 0:
            #insert new entry into farm info database table
            #TODO: change Status, the last value in vals, to be properly populated
            
            #4/13/2023 Need to get JDORGID not JDAPIORGID AND INSERT
            JDOrgIdQuery = userTask.select_jd_org_ID_by_orgID_and_JD_API_org_ID_query()
            RegJDOrgID = userTask.execute_select_query_vals(connection,JDOrgIdQuery,[orgid,jdOrgID])
            RegJDOrgID = str(RegJDOrgID[0][0])
            vals = (str(jdFarmName),str(jdFarmID),str(orgID),str(RegJDOrgID),"")
            #FIX
            farmEntry_query = userTask.insert_Farm()
            #UPDATED
            userTask.execute_create_query_vals(connection,farmEntry_query,vals)
        else:
            #update existing farm entry by farm info table farm id
            farmID = farmEntry[0][0]
            entryName = farmEntry[0][1]
            #check if farmName has changed
            if entryName != jdFarmName:
                #UPDATED FROM userTask.update_Name
                updateFarmName_query = userTask.update_FarmName()
                userTask.execute_create_query_vals(connection,updateFarmName_query,[str(jdFarmName),str(farmID)])
        
    #compile farm info dictionary list
        farmDict = {'farmID':farmID, 'jdFarmName':jdFarmName, 'jdFarmID':jdFarmID}
        farmList.append(farmDict)
            
    #return farm info dictionary list
    
    # ****Debug Start****
    if (debug):
        file.write("farmList - " + repr(farmList) + "\n")
    # ****Debug End****
    
    return farmList


def update_field_info(fields,farmID,page=None):
    # ****Debug Start****
    if (debug):
        if page != None:
            file = nt_debug_write_file("update-fieldInfo_"+str(farmID)+"_pg"+str(page))
        else:
            file = nt_debug_write_file("update-fieldInfo_"+str(farmID))
        file.write("update-fieldInfo: " + "\n")  
        file.write("fields - " + repr(fields) + "\n")
        file.write("farmID - " + repr(farmID) + "\n")
    # ****Debug End****

    values = fields['values']
#    fieldDict = {}
#    fieldList = []
    
    # ****Debug Start****
    if (debug):
        file.write('values - ' + repr(values) + "\n")
    # ****Debug End****  
    
    #extract info from json variable
    for val in values:
        jdFieldID = val['id']
        jdFieldName = val['name']
        
        # ****Debug Start****
        if (debug):
            file.write("\n" + 'val - ' + repr(val) + "\n" )
            file.write("jdFieldID - " + repr(jdFieldID) + "\n")
            file.write("jdFieldName - " + repr(jdFieldName) + "\n")
        # ****Debug End****
        
    #insert entry into database    
        
        connection = userTask.create_db_connection()
        fieldEntry_query = ''
        fieldEntry = ''
        #query database for entry existence
        fieldEntry_query = userTask.select_FieldInstance()
        fieldEntry = userTask.execute_select_query_vals(connection,fieldEntry_query,[str(farmID),str(jdFieldID)])
        
        # ****Debug Start****
        if (debug):
            file.write("fieldEntry Query - " + repr(fieldEntry_query) + "\n")
            file.write("fieldEntry - " + repr(fieldEntry) + "\n")
            file.write("fieldEntry Len - " + repr(len(fieldEntry)) + "\n")
        # ****Debug End**** 
        
        #check query for instance
        if len(fieldEntry) == 0:
            #insert new entry into farm info database table
            #TODO: change Geometry, the last value in vals, to be properly populated
            vals = (str(jdFieldName),str(farmID),str(jdFieldID),"")
            fieldEntry_query = userTask.insert_Field()
            userTask.execute_insert_update_delete_query(connection,fieldEntry_query,vals)
            #UPDATED
            fieldInstance_query = userTask.select_FieldInstance()
            newEntry = userTask.execute_select_query_vals(connection,fieldInstance_query,[str(farmID),str(jdFieldID)])
            fieldID = newEntry[0][0]
            # ****Debug Start****
            if (debug):
                file.write("new entry - " + repr(newEntry) + "\n")
                file.write("fieldID - " + repr(fieldID) + "\n")
                file.write("jdFieldName - " + repr(jdFieldName) + "\n")
                file.write("farmID - " + repr(farmID) + "\n")
                file.write("jdFieldID - " + repr(jdFieldID) + "\n")
            # ****Debug End**** 
        else:
            #update existing farm entry by farm info table farm id
            fieldID = fieldEntry[0][0]
            entryName = fieldEntry[0][1]
            
            # ****Debug Start****
            if (debug):
                file.write("update field - True" + "\n")
                file.write("fieldID - " + repr(fieldID) + "\n")
                file.write("entryName - " + repr(entryName) + "\n")
                file.write("jdFieldName - " + repr(jdFieldName) + "\n")
            # ****Debug End****
            
            #check if farmName has changed
            if entryName != jdFieldName:
                #UPDATED
                updateFieldName_query = userTask.update_FieldName()
                # ****Debug Start****
                if (debug):
                    file.write("update fieldName - true " + "\n")
                    file.write("updateFieldQuery - " + repr(updateFieldName_query) + "\n")
                # ****Debug End****    
                #UPDATED
                userTask.execute_create_query_vals(connection,updateFieldName_query,[str(jdFieldName),str(fieldID)])


def post_org_res(res,orgID):
    response = res.json()
    values = response['values']
    # ****Debug Start****
    if (debug):
        file = nt_debug_write_file("post-org")
        file.write("post-org: " + "\n")  
        file.write("res - " + repr(res) + "\n")
        file.write("response - " + repr(response) + "\n")
        file.write("values - " + repr(values[0]) + "\n")
        for val in values:
            file.write("jdOrgID - " + repr(str(val['id'])) + "\n")
            file.write("jdOrgName - " + repr(str(val['name'])) + "\n")
        
        file.write("apiResponse - " + repr(settings['apiResponse']) + "\n")
        file.close()
    # ****Debug End****
    
    
#
def post_fieldOps_res(res,orgID):
    response = res.json()
    # ****Debug Start****
    if (debug):
        file = nt_debug_write_file("post-fieldOps")
        file.write("post-fieldOps: " + "\n")  
        file.write("res - " + repr(res) + "\n")
        file.write("response - " + repr(response) + "\n")
        file.write("apiResponse - " + repr(settings['apiResponse']) + "\n")
        file.close()
    # ****Debug End****



#
def post_farms_res(response,jdOrgID,orgID):
    #for farm in response['values']:
        #query if farms already exist
        #if not present insert farm with info
            #call insert procedure
        #if present check info and update accordingly
            #call update procedure    
    
    # ****Debug Start****
    if (debug):
        file = nt_debug_write_file("post-farms")
        file.write("post-farms: " + "\n")  
        file.write("res - " + repr(response) + "\n")
        file.write("response - " + repr(response) + "\n")
        file.write("apiResponse - " + repr(settings['apiResponse']) + "\n")
        file.close()
    # ****Debug End****

    

#
def post_fields_res(response,jdOrgID,jdFarmID,orgID):
    
    #for field in response['values']:
        #query if field already present
        #if not present insert new field
            #call insert procedure
        #if present check info and update accordingly
            #call update procedure
    
    # ****Debug Start****
    if (debug):
        file = nt_debug_write_file("post-fields")
        file.write("post-fields: " + "\n")  
        file.write("res - " + repr(response) + "\n")
        file.write("response - " + repr(response) + "\n")
        file.write("apiResponse - " + repr(settings['apiResponse']) + "\n")
        file.close()
    # ****Debug End****

    
def post_AppData(appRes,appJSON,orgID,JDAppID,appOrgID,geometry):
    #obtain application values from field operations and fieldops dataset 
    #and then store them to the application database
    
    # ****Debug Start****
    if (debug):
        file = nt_debug_write_file("post-application")
        file.write("post-application: " + "\n")
        file.write("orgID - " + repr(orgID) + "\n")
        file.write("jdAppID - " + repr(JDAppID) + "\n")
    # ****Debug End****
    
    #convert response to json
    appData = appRes.json()
    
    #parse appRes (fieldoperations response)
    appID = appData['id']
    #parse time from of of start and end date strings for rei calculation
    appStartDate = appData['startDate']     #**reformat
    appEndDate = appData['endDate']         #**reformat
    appOrgID = appJSON['OrgId']
    appJDFarmID = appJSON['FarmId']
    appJDFarmName = appJSON['FarmName']
    appJDFieldID = appJSON['FieldId']
    appJDFieldName = appJSON['FieldName']
    appTankMixName = appData['product']['name']
    appTankMix = appJSON['Product']['TankMix']
    appJDOrgID = appOrgID
    
    # ****Debug Start****
    if (debug):
        location = "MainData Parsed"
        file.write("location - " + repr(location) + "\n")
        file.write("appJDFarmID - " + repr(appJDFarmID) + "\n")
        file.write("appJDFieldID - " + repr(appJDFieldID) + "\n")
    # ****Debug End****
    
    if appTankMix == True:
        appProducts = appJSON['Product']['Components']
        products = []
        prod = {}
        # ****Debug Start****
        if (debug):
            location = "loop Products"
            file.write("location - " + repr(location) + "\n")
        # ****Debug End****
        cnt = 0
        for product in appProducts:
            if product['Carrier'] == True:
                appCarrier = product['Name']
                appCarrierRate = product['Rate']['Value']
                appCarrierUnits = product['Rate']['Unit']
                prod = {'Carrier':str(appCarrier),'Rate':str(appCarrierRate),'Units':str(appCarrierUnits)}
            else:
                appProductName = product['Name']
                appProductRate = product['Rate']['Value']
                appProductUnits = product['Rate']['Unit']
                prod = {'Product':str(appProductName),'Rate':str(appProductRate),'Units':str(appProductUnits)}
            
            products.insert(cnt,prod)
            cnt+=1
    #else:
        #write in parse for single product application
    
    appEquipSN = appJSON['MachineUsage']['1']['MachineSerial']
    
    # ****Debug Start****
    if (debug):
        location = "Connection to databases and insert application entry"
        file.write("location - " + repr(location) + "\n")
    # ****Debug End****
                
    #query user farmId with use of jd farm ID and ssOrgID
    #UPDATED
    connectionUser = userTask.create_db_connection()
    sqlFarmQuery = userTask.select_FarmID_byJDFarmIDssOrgID()
    ssFarmID = userTask.execute_select_query_vals(connectionUser,sqlFarmQuery,[str(appJDFarmID),str(orgID)])
    
    
    #query user field id with use of jd field ID and ssFarmID
    sqlFieldQuery = userTask.select_FieldID_byJDFieldIDssFarmID()
    ssFieldID = userTask.execute_select_query_vals(connectionUser,sqlFieldQuery,[str(appJDFieldID),str(ssFarmID[0][0])])
    
    # ****Debug Start****
    if (debug):
       file.write("ssFarmID query - " + repr(sqlFarmQuery) + "\n")
       file.write("ssFarmID - " + repr(ssFarmID) + "\n")
       file.write("ssFieldID query - " + repr(sqlFieldQuery) + "\n")
       file.write("ssFieldID - " + repr(ssFieldID) + "\n")
       file.write("products - " + repr(products) + "\n")
       file.write("appStartDate - " + repr(appStartDate) + "\n")
       file.write("appEndDate - " + repr(appEndDate) + "\n")
       file.write("appEquipSN - " + repr(appEquipSN) + "\n")
       file.write("jdAppID - " + repr(JDAppID) + "\n")
       file.write("geometry - " + repr(geometry) + "\n")
    # ****Debug End****
    
    #post application information to application database
    connectionApp = appTask.create_AppDB_Connection()
    #UPDATED
    #WAS .select_App_byOrgJDAppID(JDAppID,str(orgID))
    sqlApp_query = appTask.select_App_byOrgJDAppID_query()
    appState = appTask.execute_select_query_vals(connectionApp,sqlApp_query,[JDAppID,str(orgID)])
    if not appState:
        values = (appID,str(ssFieldID[0][0]),"Applicator_ID","Tank_Mix_ID","App_Type",str(appStartDate),str(appEndDate),"REI_Exp",str(appEquipSN),"Weather",str(JDAppID),str(geometry))
        sqlAppInsert_query = appTask.insert_Application()
        appStatus = appTask.execute_insert_update_delete_query(connectionApp,sqlAppInsert_query,values)
        # ****Debug Start****
        if (debug):
            file.write("appState - " + repr(appState) + "\n")
            file.write("values - " + repr(values) + "\n")
            file.write("sqlApp_query - " + repr(sqlApp_query) + "\n")
            file.write("appStatus - " + repr(appStatus) + "\n")
            if appStatus != None:
                location = "Application Entry Post Completed"
                file.write("location - " + repr(location) + "\n")
        # ****Debug End****
    else:
        # ****Debug Start****
        if (debug):
            file.write("entry already Exists - " + "\n")
            file.write("entry ID - " + repr(appState) + "\n")
        # ****Debug End****        
    
    # ****Debug Start****
    if (debug):
        file.close()
    # ****Debug End****


#   *   *   *   *   *   *   *   *   *   *   Local API helper Procedures   *   *   *   *   *   *   *   *   *   *
def compare_SubFilters(res,jdOrgID,fieldIDs,cropSeason):
    # procedure returns true if the subscription needs to be updated
    # and false if no updates are needed
    
    import numpy as np
    
    # ****Debug Start****
    if (debug):
        file = nt_debug_write_file("compareSubFilters")
        file.write("compareSubFilters: " + "\n")
        file.write('res - ' + repr(res) + "\n")
        file.write('resLen - ' + repr(len(res)) + "\n")
        file.write('resFilters - ' + repr(res['filters']) + "\n")
    # ****Debug End****
    
    resFilters = res['filters']
    jdOrgID = [str(jdOrgID)]
    cropSeason = [str(cropSeason)]
    
    #set local variables
    for i in range(len(resFilters)):
        resKey = resFilters[i]['key']
        resValues = resFilters[i]['values']
        # ****Debug Start****
        if (debug):
            file.write('resKey - ' + repr(resKey) + "\n")
            file.write('resValues - ' + repr(resValues) + "\n")
        # ****Debug End****
        if resKey == 'orgId':
            subOrgID = resValues
        elif resKey == 'fieldId':
            subFieldIDs = resValues
        elif resKey == 'cropSeason':
            subCropSeason = resValues
    
    #sort all variable arrays
    subOrgIDs_sort = np.sort(subOrgID)
    subFieldIDs_sort = np.sort(subFieldIDs)
    subCropSeason_sort = np.sort(subCropSeason)
    
    jdOrgID_sort = np.sort(jdOrgID)
    fieldIDs_sort = np.sort(fieldIDs)
    cropSeason_sort = np.sort(cropSeason)
    
    # ****Debug Start****
    if (debug):
        file.write("subOrgID - " + repr(subOrgID) + "\n")
        file.write("subFieldIDs - " + repr(subFieldIDs) + "\n")
        file.write("subCropSeason - " + repr(subCropSeason) + "\n")
        file.write("jdOrgID - " + repr(jdOrgID) + "\n")
        file.write("fieldIDs - " + repr(fieldIDs) + "\n")
        file.write("cropSeason - " + repr(cropSeason) + "\n")
    # ****Debug End****
    
    #compare local variable arrays to passed arrays
    if len(subOrgIDs_sort)==len(jdOrgID_sort):
        # ****Debug Start****
        if (debug):
            file.write("orgIDs len - True" + "\n")
        # ****Debug End****
        
        if (subOrgIDs_sort == jdOrgID_sort).all():
            # ****Debug Start****
            if (debug):
                file.write("orgIDs - True" + "\n")
            # ****Debug End****
            
            if len(subFieldIDs_sort)==len(fieldIDs_sort):
                # ****Debug Start****
                if (debug):
                    file.write("fieldIDS len - True" + "\n")
                # ****Debug End****
                
                if (subFieldIDs_sort == fieldIDs_sort).all():
                    # ****Debug Start****
                    if (debug):
                        file.write("fieldIDS - True" + "\n")
                    # ****Debug End****
                    
                    if len(subCropSeason_sort)==len(cropSeason_sort):
                        # ****Debug Start****
                        if (debug):
                            file.write("cropSeason len - True" + "\n")
                        # ****Debug End****
                        
                        if (subCropSeason_sort == cropSeason_sort).all():
                            # ****Debug Start****
                            if (debug):
                                file.write("cropSeason - True" + "\n")
                            # ****Debug End****
                            
                            return False
                        else:
                            # ****Debug Start****
                            if (debug):
                                file.write("cropSeason - False" + "\n")
                            # ****Debug End****
                            
                            return True
                    else:
                        # ****Debug Start****
                        if (debug):
                            file.write("cropSeason len - False" + "\n")
                        # ****Debug End****
                        
                        return True
                else:
                    # ****Debug Start****
                    if (debug):
                        file.write("fieldIDS - False" + "\n")
                    # ****Debug End****
                    
                    return True
            else:
                # ****Debug Start****
                if (debug):
                    file.write("fieldIDS len - False" + "\n")
                # ****Debug End****
                
                return True
        else:
            # ****Debug Start****
            if (debug):
                file.write("orgIDs - False" + "\n")
            # ****Debug End****
            
            return True
    else:
        # ****Debug Start****
        if (debug):
            file.write("orgIDs len - False" + "\n")
        # ****Debug End****
        
        return True
    # ****Debug Start****
    if (debug):
        file.close()
    # ****Debug End****
    
    
def parseZip(resShp,extract=None,directory=None):
    # ****Debug Start****
    if(debug):
        file = nt_debug_write_file('get_parseZip')
        file.write('resShp - ' + repr(resShp) + "\n")
        file.write('extract - ' + repr(extract) + "\n")
        file.write('directory - ' + repr(directory) + "\n")
    # ****Debug End****
    
    #check that variable is ok and parse fileNames from zipfile if true
    if resShp.ok:
        fileZip = zipfile.ZipFile(BytesIO(resShp.content))
        
        # ****Debug Start****
        if(debug):
            file.write('zipfile namelist - ' + repr(fileZip.namelist()) + "\n")
        # ****Debug End****
        
        #prior to jd issues 08/10/2022
        #jsonFile,dbfFile,prjFile,shpFile,shxFile = fileZip.namelist()
        #after jd issues 08/10/2022
        shpFile,shxFile,dbfFile,prjFile,jsonFile,cpgFile = fileZip.namelist()
        
        # ****Debug Start****
        if(debug):
            file.write('zip shapefile - ' + str(shpFile) + "\n")
            file.write('zip json - ' + str(jsonFile) + "\n")
            file.close()
        # ****Debug End****
        
        if extract == True and directory != None:
            fileZip.extractall(directory)
            shpDir = directory + "/" + shpFile
            jsonDir = directory + "/" + jsonFile
            return shpDir, jsonDir
        else:
            return fileZip
    else:
        # ****Debug Start****
        if(debug):
            file.write('resShp not ok ' + "\n")
            file.close()
        # ****Debug End****


#   *   *   *   *   *   *   *   *   *   *   Local API Call Procedures   *   *   *   *   *   *   *   *   *   *
def get_location_from_metadata(endpoint):
    response = requests.get(settings['wellKnown'])
    return response.json()[endpoint]


def get_oidc_query_string():
    query_params = {
        "client_id": settings['clientId'],
        "response_type": "code",
        "scope": urllib.parse.quote(settings['scopes']),
        "redirect_uri": settings['callbackUrl'],
        "state": settings['state'],
    }
    params = [f"{key}={value}" for key, value in query_params.items()]
    return "&".join(params)

def get_OAuth(code):
    try:
        # ****Debug Start****
        if(debug):
            file = nt_debug_write_file('get_OAuth')
            file.write('code - ' + repr(code) + "\n")
            location = 'header'
            file.write('location - '+location+"\n")
        # ****Debug End****
        
        headers = {
            'authorization': 'Basic ' + get_basic_auth_header().decode('utf-8'),
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        # ****Debug Start****
        if(debug):
            location = 'payload'
            file.write('location - '+location+"\n")
        # ****Debug End****
        
        payload = {
            'grant_type': 'authorization_code',
            'redirect_uri': settings['callbackUrl'],
            'code': code,
            'scope': settings['scopes']
        }
        
        # ****Debug Start****
        if(debug):
            file.write('headers - ' + str(headers) + "\n")
            file.write('payload - ' + str(payload) + "\n")
            location = 'res'
            file.write('location - '+location+"\n")
            file.close()
        # ****Debug End****
        
        res = requests.post(get_location_from_metadata('token_endpoint'), data=payload, headers=headers)
        
        return res
    except Exception as e:
        logging.exception(e)
        return render_error('Error Getting OAuth!')

def refreshAccessToken(username=None):
    try:
        headers = {
            'authorization': 'Basic ' + get_basic_auth_header().decode('utf-8'),
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        payload = {
            'grant_type': 'refresh_token',
            'redirect_uri': settings['callbackUrl'],
            'refresh_token': settings['refreshToken'],
            'scope': settings['scopes']
        }
        
        # ****Debug Start****
        if (debug):
            file = nt_debug_write_file("refreshAccessToken")
            file.write("refresh access token:" + "\n")
            file.write("headers - " + repr(headers) + "\n")
            file.write("payload - " + repr(payload) + "\n")
        # ****Debug End****
        
        res = requests.post(get_location_from_metadata('token_endpoint'), data=payload, headers=headers)
        
        # ****Debug Start****
        if (debug):
            file.write("response - " + repr(res) + "\n")
            file.write("res json - " + repr(res.json()) + "\n")
        # ****Debug End****
        if username==None:
            update_token_info(res)
        else:
            update_token_info(res,username)
        
        #return index()
    except Exception as e:
        logging.exception(e)
        return render_error('Error getting refresh token!')


def get_basic_auth_header():
    return base64.b64encode(bytes(settings['clientId'] + ':' + settings['clientSecret'], 'utf-8'))



def api_get(access_token, resource_url, addParameter, payload):
    # ****Debug Start****
    if (debug):
        file = nt_debug_write_file("api_get")
        file.write("api_get: " + "\n")
        file.write('access_token - ' + repr(access_token) + "\n")
        file.write('resource_url - ' + repr(resource_url) + "\n")
        file.write('addParameter - ' + repr(addParameter) + "\n")
        file.write('payload - ' + repr(payload) + "\n")
    
    headers = {
        'authorization': 'Bearer ' + access_token,
        'Accept': 'application/vnd.deere.axiom.v3+json'
    }
    if addParameter is not None:
        headers.update(addParameter)
    
    # ****Debug Start****
    if (debug):
        file.write('headers - ' + str(headers) + "\n")
        file.close()
    # ****Debug End****
    
    if payload is not None:
        return requests.get(resource_url, data=payload, headers=headers)
    else:
        return requests.get(resource_url, headers=headers)


def api_post(access_token, resource_url, addParameter, payload):
    # ****Debug Start****
    if (debug):
        file = nt_debug_write_file("api_post")
        file.write("api_post: " + "\n")
        file.write('access_token - ' + repr(access_token) + "\n")
        file.write('resource_url - ' + repr(resource_url) + "\n")
        file.write('addParameter - ' + repr(addParameter) + "\n")
        file.write('payload - ' + repr(payload) + "\n")
    # ****Debug End****
    
    headers = {
        'authorization': 'Bearer ' + access_token,
        'Accept': 'application/vnd.deere.axiom.v3+json'
    }
    if addParameter is not None:
        headers.update(addParameter)

    # ****Debug Start****
    if (debug):
        file.write('headers - ' + repr(headers) + "\n")
        file.close()
    # ****Debug End****
    
    if payload is not None:
        return requests.post(resource_url, json=payload, headers=headers)
    else:
        return requests.post(resource_url, headers=headers)
        
        
def api_put(access_token, resource_url, addParameter, payload):
    # ****Debug Start****
    if (debug):
        file = nt_debug_write_file("api_put")
        file.write("api_put: " + "\n")
        file.write('access_token - ' + repr(access_token) + "\n")
        file.write('resource_url - ' + repr(resource_url) + "\n")
        file.write('addParameter - ' + repr(addParameter) + "\n")
        file.write('payload - ' + repr(payload) + "\n")
    # ****Debug End****
    
    headers = {
        'authorization': 'Bearer ' + access_token,
        'Accept': 'application/vnd.deere.axiom.v3+json'
    }
    if addParameter is not None:
        headers.update(addParameter)
    
    # ****Debug Start****
    if (debug):
        file.write('headers - ' + repr(headers) + "\n")
        file.close()
    # ****Debug End****
    
    if payload is not None:
        return requests.put(resource_url, json=payload, headers=headers)
    else:
        return requests.put(resource_url, headers=headers)


def call_the_api(url, addParameter, payload, method):
    
    # moved from flask call to function call only
    # ****Debug Start****
    if (debug):
        file = nt_debug_write_file("call-api")
        file.write("call-api: " + "\n")  
        file.write("url - " + repr(url) + "\n")
        file.write("settings - " + repr(settings) + "\n")
    # ****Debug End****
    
    try:
        if method=='GET':
            res = api_get(settings['accessToken'], url, addParameter, payload)
        elif method=='POST':
            res = api_post(settings['accessToken'], url, addParameter, payload)
        elif method=='PUT':
            res = api_put(settings['accessToken'], url, addParameter, payload)
        
        #UPDATED, this threw an error previously
        contentType = res.headers.get("Content-Type")
        #contentType = res.headers.get('Content-Type')
        
        # ****Debug Start****
        if (debug):    
            file.write("res - " + str(res) + "\n")
            file.write("res status - " + str(res.status_code) + "\n")
            file.write("res headers - " + str(res.headers) + "\n")
            file.write("res contentType - " + str(contentType) + "\n")
        # ****Debug End****
        
        contentCheck = 'application/vnd.deere.axiom.v3+json'
        
        # ****Debug Start****
        if (debug):    
            file.write("contentCheck - " + str(contentCheck) + "\n")
        # ****Debug End****
        
        if str(contentCheck) in str(contentType):
            jsonBool = True
        elif str(contentCheck) == str(contentType):
            jsonBool = True
        else:
            jsonBool = False
        
        # ****Debug Start****
        if (debug):    
            file.write("jsonBool - " + str(jsonBool) + "\n")
        # ****Debug End****
        
        if  jsonBool == True:
            if res.status_code == 200:
                #set settings apiResponse to respone json
                settings['apiResponse'] = res.json()
                #settings['apiResponse'] = json.dumps(res.json(), indent=4)
                
                # ****Debug Start****
                if (debug):
                    file.write("apiResponse - " + repr(settings['apiResponse']) + "\n")
                    file.write("res - " + repr(res.json()) + "\n")
                # ****Debug End****
        else:
            # ****Debug Start****
            if (debug):
                file.write("no json content to parse " + "\n")
            # ****Debug End****
        
        # ****Debug Start****
        if(debug):
            file.write("closing file" + "\n")
            file.close()
        # ****Debug End****
        
        return res
    except Exception as e:
        logging.exception(e)
        return render_error('Error calling API!')
        

def get_org_res():
    url = 'https://sandboxapi.deere.com/platform/organizations'
    payload = None        #no payload necessary
    addParameter = None     #no additional header parameters necessary
    method='GET'
    res = call_the_api(url, addParameter, payload, method)
    response = res.json()
    # ****Debug Start****
    if (debug):
        file = nt_debug_write_file("get-org")
        file.write("get-org: " + "\n")  
        file.write("res - " + repr(res) + "\n")
        file.write("response - " + repr(response) + "\n")
        file.write("apiResponse - " + repr(settings['apiResponse']) + "\n")
        file.close()
    # ****Debug End****
    return res      #response?
    
    
def get_farms_res(jdOrgID):
    url = 'https://sandboxapi.deere.com/platform/organizations/'+jdOrgID+'/farms'
    payload = None        #no payload necessary
    addParameter = None     #no additional header parameters necessary
    method='GET'
    res = call_the_api(url, addParameter, payload, method)
    response = res.json()
    # ****Debug Start****
    if (debug):
        file = nt_debug_write_file("get-farms")
        file.write("get-farms: " + "\n")  
        file.write("res - " + repr(res) + "\n")
        file.write("response - " + repr(response) + "\n")
        file.write("apiResponse - " + repr(settings['apiResponse']) + "\n")
        file.close()
    # ****Debug End****
    return response
    
    
def get_fields_res(jdOrgID,jdFarmID,url=None,farmID=None,page=None):
    if url==None:
        url = 'https://sandboxapi.deere.com/platform/organizations/'+jdOrgID+'/farms/'+jdFarmID+'/fields' #;count=100'
        
    payload = None        #no payload necessary
    addParameter = None     #no additional header parameters necessary
    method='GET'
    res = call_the_api(url, addParameter, payload, method)
    response = res.json()
    # ****Debug Start****
    if (debug):
        if farmID != None and page != None:
            file = nt_debug_write_file("get-fields"+str(farmID)+"-"+str(page))
        elif farmID != None:
            file = nt_debug_write_file("get-fields"+str(farmID))
        else:
            file = nt_debug_write_file("get-fields"+str(jdFarmID))
        
        file.write("get-fields: " + "\n")
        file.write("url - " + repr(url) + "\n")
        file.write("res - " + repr(res) + "\n")
        file.write("response - " + repr(response) + "\n")
        file.write("apiResponse - " + repr(settings['apiResponse']) + "\n")
        file.close()
    # ****Debug End****
    return response
    
    
def get_EventSubscription(orgID,jdOrgID):
    connection = userTask.create_db_connection()
    #query database for subscription id
    #UPDATED
    #REPLACE WITH select_JD_subscription_ID_by_JD_org_ID_query()?
    #was .select_JDSubID(str(orgID), str(jdOrgID))
    sqlQuery = userTask.select_JD_subscription_ID_by_Org_ID_and_JD_API_org_ID_query()
    #UPDATED
    jdSubID = userTask.execute_select_query_vals(connection,sqlQuery,[str(orgID), str(jdOrgID)])
    # retrieve all jd operations event subscriptions for jdOrgID
    url = 'https://sandboxapi.deere.com/platform/eventSubscriptions/'+jdSubID[0][0]
    payload = None
    addParameter = {'Content-Type':'application/vnd.deere.axiom.v3+json'}
    method='GET'
    
    # ****Debug Start****
    if (debug):
        file = nt_debug_write_file("get-EventSubscript")
        file.write("get-Subscript: " + "\n")
        file.write("sqlQuery - " + str(sqlQuery) + "\n")
        file.write("jdSubID - " + repr(jdSubID) + "\n")
        file.write("jdSubID Parsed - " + repr(jdSubID[0][0]) + "\n")
        file.write("url - " + repr(url) + "\n")
    # ****Debug End****
    
    #CURRENT ERROR
    res = call_the_api(url, addParameter, payload, method)
    response = res.json()

    # ****Debug Start****
    if (debug):
        file.write("res - " + repr(res) + "\n")
        file.write("response - " + repr(response) + "\n")
        file.write("apiResponse - " + repr(settings['apiResponse']) + "\n")
        file.close()
    # ****Debug End****
    return response
    
    
def create_DataSubscription(jdOrgID,cropSeason,reqFields,displayName, token):
    url = 'https://sandboxapi.deere.com/platform/eventSubscriptions'
    payload = {
        'eventTypeId': 'fieldOperation',
        'filters':[
         {
            'key': 'orgId',
            'values': [str(jdOrgID)]
         },
         {
            'key': 'fieldOperationType',
            'values': ['application']
         },
         {
            'key': 'cropSeason',
            'values': [str(cropSeason)]
         },
         {
            'key': 'fieldId',
            'values': reqFields
         }
        ],
        'targetEndpoint':{
            'targetType': 'https',
            'uri': 'https://jd-test.spray-safely.test:5000/receiveEvents'
        },
        'displayName': displayName,
        'token': token
    }
    addParameter = {'Content-Type':'application/vnd.deere.axiom.v3+json'}
    method='POST'
    res = call_the_api(url,addParameter,payload, method)
    
    # ****Debug Start****
    if (debug):
        file = nt_debug_write_file("create_Subscription")
        file.write("create_Subscription: " + "\n")  
        file.write("res - " + repr(res) + "\n")
    # ****Debug End****
    
    response = res.json()
    
    # ****Debug Start****
    if (debug):
        file.write("response - " + repr(response) + "\n")
        file.write("apiResponse - " + repr(settings['apiResponse']) + "\n")
        file.close()
    # ****Debug End****
    return response
    
    
def update_DataSubscription(subscriptionID,status,displayName,token):
    # ****Debug Start****
    if (debug):
        file = nt_debug_write_file("updateDataSub")
        file.write("update-DataSub: " + "\n")
    # ****Debug End****
    
    # update current john deere operations center api data subscription
    url = 'https://sandboxapi.deere.com/platform/eventSubscriptions/'+subscriptionID
    payload = {
        'targetEndpoint':{
            'targetType': 'https',
            'uri': 'https://jd-test.spray-safely.test:5000/receiveEvents'
        },
        'status': str(status),
        'displayName': str(displayName),
        'token': str(token)
    }
    addParameter = {'Content-Type':'application/vnd.deere.axiom.v3+json'}
    method='PUT'
    res = call_the_api(url,addParameter,payload, method)
    response = res.json()
    # ****Debug Start****
    if (debug):
        file.write("res - " + repr(res) + "\n")
        file.write("response - " + repr(response) + "\n")
        file.close()
    # ****Debug End****
    return response
    
    
def get_fieldOps_res(jdOpID,targetEndpoint):
    # ****Debug Start****
    if (debug):
        file = nt_debug_write_file("get-fieldOpsRes")
        file.write("get-fieldOps: " + "\n")
        file.write("time - " + str(datetime.datetime.now()) + "\n")
        file.write("targetEndpoint - " + repr(targetEndpoint) + "\n")
    # ****Debug End****
    
    #url = 'https://sandboxapi.deere.com/platform/fieldOps/'+jdOpID
    url = targetEndpoint
    payload = {
        'splitShapeFile': 'false',
        'shapeType': 'Point',
        'resolution': 'EachSensor',
        'Accept-UOM-System': 'ENGLISH'
    }
    addParameter = None     #no additional header parameters necessary
    method='GET'
    
    # ****Debug Start****
    if (debug):
        file.write("url - " + repr(url) + "\n")
        file.write("payload - " + repr(payload) + "\n")
        file.write("addParameter - " + repr(addParameter) + "\n")
    # ****Debug End****
    
    res = call_the_api(url, addParameter, payload, method)
    
    # ****Debug Start****
    if (debug):
        file.write("res - " + repr(res) + "\n")
        file.write("apiResponse - " + str(res) + "\n")
        file.close()
    # ****Debug End****
    
    return res

def get_fieldOps(targetEndpoint):       #Passed on 403 response
    # john deere is experiencing issues which requires no body be sent 
    # when attempting to retrieve a 307 response. In the event that a
    # body is sent, the response will return a 403 instead of the 
    # desired 307.  Date: August 11, 2022
    
    # ****Debug Start****
    if (debug):
        file = nt_debug_write_file("get-fieldOps")
        file.write("get-fieldOps: " + "\n")
        file.write("time - " + str(datetime.datetime.now()) + "\n")
        file.write("targetEndpoint - " + repr(targetEndpoint) + "\n")
    # ****Debug End****
    
    #url = 'https://sandboxapi.deere.com/platform/fieldOps/'+jdOpID
    url = targetEndpoint
    payload = None
    addParameter = None     #no additional header parameters necessary
    method='GET'
    
    # ****Debug Start****
    if (debug):
        file.write("url - " + repr(url) + "\n")
        file.write("payload - " + repr(payload) + "\n")
        file.write("addParameter - " + repr(addParameter) + "\n")
    # ****Debug End****
    
    res = call_the_api(url, addParameter, payload, method)
    
    # ****Debug Start****
    if (debug):
        file.write("res - " + repr(res) + "\n")
        file.write("apiResponse - " + str(res) + "\n")
        file.close()
    # ****Debug End****
    
    return res
    
    
def get_fieldOperations_res(jdOpID):
    url = 'https://sandboxapi.deere.com/platform/fieldOperations/'+jdOpID
    payload = None
    addParameter = None     #no additional header parameters necessary
    method='GET'
   
    # ****Debug Start****
    if (debug):
        file = nt_debug_write_file("get-fieldOperations")
        file.write("get-fieldOperations: " + "\n") 
        file.write("url - " + repr(url) + "\n")
        file.write("payload - " + repr(payload) + "\n")
        file.write("addParameter - " + repr(addParameter) + "\n")
    # ****Debug End****
    
    res = call_the_api(url, addParameter, payload, method)
    
    # ****Debug Start****
    if (debug):
        file.write("res - " + repr(res) + "\n")
        file.write("apiResponse - " + repr(settings['apiResponse']) + "\n")
        file.close()
    # ****Debug End****
    
    return res


def get_AppDataset_shp(url):
    headers = {
        'Accept': 'application/vnd.deere.axiom.v3+json'
    }
    
    resShp = requests.get(url, headers=headers)
    
    return resShp


#   *   *   *   *   *   *   *   *   *   *   Debug Procedures   *   *   *   *   *   *   *   *   *   *
def render_error(message):
    return render_template('error.html', title='John Deere API with Python', error=message)

def nt_debug_write_file(funct_Str):
    """ 
    debug function that creates text file
    and returns file to be written to for
    debugging functions and procedures.
    """
    
    from datetime import datetime
    
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    cTime = current_time.replace(':','')
    
    save_Path = 'debug_Log'
    file_name = 'debugJDAuth_' + funct_Str + "_" + str(cTime) + ".txt"
    
    file = os.path.join(save_Path,file_name)
    
    debugFile = open(file,"w")
    debugFile.write("Created - " + str(now) + "\n")
    
    return debugFile


#   *   *   *   *   *   *   *   *   *   *   Flask Calls   *   *   *   *   *   *   *   *   *   *
@jd_app.route("/jdaccess/")
def jdAccess():
    username = request.args['username']
    session['username'] = username
    redirect_url = '/'
    return redirect(redirect_url,code=302)


@jd_app.route("/")
def start_oidc():
    try:
        username = session['username']
    except Exception as e:
        logging.exception(e)
        return render_error('Missing Username!')
    
#    return render_template('main.html', title='John Deere API with Python', settings=settings)
    

    # Create database connection
    connection = userTask.create_db_connection()
    sql = userTask.select_userID_by_username_query()
    userid = userTask.execute_select_query_vals(connection,sql, [username])

    
    try: 
        # ****Debug Start****
        if (debug):
            file = nt_debug_write_file("start_oidc")
            file.write("start_oidc: " + "\n")
            file.write("username: " + repr(username) + "\n") #nt
            file.write("userId: " + repr(userid[0][0]) + "\n")
            file.write("settings length - " + repr(len(settings)) + "\n" )
            file.write("settings - callbackUrl: " + repr(settings['callbackUrl']) + "\n")
            file.write("settings - wellKnown: " + repr(settings['wellKnown']) + "\n")
        # ****Debug End****
        
        redirect_url = f"{get_location_from_metadata('authorization_endpoint')}?{get_oidc_query_string()}"
        
        # ****Debug Start****
        if(debug):
            file.write("redirect url -  " + repr(redirect_url) + "\n")
            file.close()
        # ****Debug End****

        return redirect(redirect_url, code=302)
    except Exception as e:
        logging.exception(e)
        return render_error('Error Auth!')

#John deere couldn't get access
def needs_organization_access():
    """Check if another redirect is needed to finish the connection.

    Check to see if the 'connections' rel is present for any organization.
    If the rel is present it means the oauth application has not completed its
    access to an organization and must redirect the user to the uri provided
    in the link.
    """
    addParameter = None
    payload = None
    api_response = api_get(settings['accessToken'], settings['apiUrl']+'/organizations',addParameter,payload).json()
    
    # ****Debug Start****
    if (debug):
        file = nt_debug_write_file("needs_orgAccess")
        file.write("needs_orgAccess: " + "\n")
        file.write("apiResponse - "+repr(api_response)+"\n")
    # ****Debug End****
    
    for org in api_response['values']:
        for link in org['links']:
            if link['rel'] == 'connections':
                connectionsUri = link['uri']
                query = urllib.parse.urlencode({'redirect_uri': settings['orgConnectionCompletedUrl']})
                
                # ****Debug Start****
                if (debug):
                    file.write("query -  " + repr(query) + "\n")
                    file.close()
                # ****Debug End****
                
                return f"{connectionsUri}?{query}"
    return None


@jd_app.route("/callback")
def callback():
    
    # ****Debug Start****
    if(debug):
        file = nt_debug_write_file("callback")
        file.write("callback:" + "\n")
        location = 'username'
        file.write('location - ' + repr(location) + "\n")
    # ****Debug End****
    
    exceptFile = nt_debug_write_file("callback_exception")
    
    if 'username' in session:
        username = session['username']
        
        # ****Debug Start****
        if(debug):
            file.write("username: " + repr(str(username)) + "\n")
        # ****Debug End****
    
        #THESE VARIABLES ARE IMPORTANT AND ARE USED THROUGHOUT THE REST OF THIS FUNCTION
        #UPDATED
        #THIS QUERY GETS THE USERID
        sqlQuery = userTask.select_userID_by_username_query()
        connection = userTask.create_db_connection()
        queryReturn = userTask.execute_select_query_vals(connection,sqlQuery,[username])
        ssUserID = str(queryReturn[0][0])
        
        sqlQuery = ''
        
        #UPDATED
        #IT THEN TRIES TO GET THE ORGID USING THE USERID
        #BUT USERID NO LONGER EXISTS IN ORG_INFO
        
        #WOULD USER_ORG_INFO TABLE WORK IT HAS BOTH USER_ID AND ORG_ID?
        sqlQuery = userTask.select_orgIDs_by_userID_query()
        connection = userTask.create_db_connection()
        queryReturn = userTask.execute_select_query_vals(connection,sqlQuery,[str(ssUserID)])
        ssOrgID = str(queryReturn)
        #ssOrgID = str(queryReturn[0][0])
        
        sqlQuery = ''
        
        # ****Debug Start****
        if(debug):
            file.write("ssUserID: " + repr(ssUserID) + "\n")
            file.write("ssOrgID: " + repr(ssOrgID) + "\n")
            file.write("settings - " + "\n")
            for i in settings:
                file.write("\t" + repr(i) + " - " + repr(settings[i]) + "\n")
                if any(isinstance(i, list) for i in settings):
                    file.write("\t" + "length - " + repr(len(settings[i])) + "\n")
        
            file.write("url - " + repr(request.url) + "\n")
        # ****Debug End****
        
        try:
            # ****Debug Start****
            if(debug):
                location = 'code'
                file.write('location - '+location+"\n")
            # ****Debug End****
            
            code = request.args['code']
            
            # ****Debug Start****
            if(debug):
                file.write('code - ' + repr(code) + "\n")
                location = 'header'
                file.write('location - '+location+"\n")
            # ****Debug End****
            
            res = get_OAuth(code)
            
            # ****Debug Start****
            if(debug): 
                file.write("url state - " + repr(request.args.get('state')) + "\n")
                file.write("code - " + repr(code) + "\n")
                file.write("reqArgs - " + repr(request.args) + "\n")
                file.write("res - " + repr(res) + "\n")
                location = 'update token info'
                file.write('location - '+location+"\n")
            # ****Debug End****
            
            update_token_info(res)
            
            # ****Debug Start****
            if(debug):
                location = 'org access gen'
                file.write('location - '+location+"\n")
            # ****Debug End****
            
            organization_access_url = needs_organization_access()
            
            # ****Debug Start****
            if(debug):
                file.write("org access url - " + repr(organization_access_url) + "\n")
                location = 'org access url'
                file.write('location - '+location+"\n")
            # ****Debug End****
            
            if organization_access_url is not None:
                return redirect(organization_access_url, code=302)
            
            # ****Debug Start****
            if(debug):
                file.write("settings after call - " + "\n")
                #file.write(repr(isinstance(settings,dict)) + "\n")
                location = 'settings loop'
                file.write('location - '+location+"\n")
                for i in settings:
                    file.write("\t" + repr(i) + " - " + repr(settings[i]) + "\n")
                    #file.write("\t\t" + repr(isinstance(settings[i],dict)) + "\n")
                    #if isinstance(settings[i],list):
                    #    file.write("\t" + "length - " + repr(len(settings[i])) + "\n")
            # ****Debug End****
            
        #Request remaining john deere account information    
          #CALL API - get oganizations response
            orgRes = get_org_res()
            # ****Debug Start****
            if (debug):
                location = "get jd org response"
                file.write("org res - " + repr(orgRes) + "\n")
            # ****Debug End****
            
            #update organization info in ssUser_Info DB
            orgs = update_jdOrgInfo(orgRes,ssOrgID)     #sets self org name and id and returns list of all available orgs
            
            # ****Debug Start****
            if (debug):
                file.write("orgs - " + repr(orgs) + "\n")
            # ****Debug End****
            
          #CALL API - get farms response             
            # ****Debug Start****
            if(debug):
                location = 'get org farms'
                file.write("location - "+location+"\n")
            # ****Debug End****
            
            for org in orgs:
                # ****Debug Start****
                if(debug):
                    file.write("org - "+repr(org)+"\n")
                # ****Debug End****
                
              #call api - organizations/{orgID}/farms
                jdOrgID = org['jdOrgID']
                jdOrgName = org['jdOrgName']
                jdOrgType =  org['jdOrgType']
                
                # ****Debug Start****
                if(debug):
                    file.write("jdOrgID: "+repr(jdOrgID)+"\n")
                    file.write("jdOrgName: "+repr(jdOrgName)+"\n")
                    file.write("jdOrgType: "+repr(jdOrgType)+"\n")
                # ****Debug End****
               
                location = 'get farm reponse'
                farms = get_farms_res(org['jdOrgID'])
                
                 # ****Debug Start****
                if(debug):
                    location = 'update farm info'
                    file.write("farms - "+repr(farms)+"\n")
                # ****Debug End****
                
                farmList = update_farm_info(farms, jdOrgID, ssOrgID)
                # ****Debug Start****
                
                if(debug):
                    file.write("farmList - " + repr(farmList) + "\n")
                # ****Debug End****
                
          #CALL API - get fields response
                for farm in farmList:
                    farmID = farm['farmID']
                    jdFarmID = farm['jdFarmID']
                  #call api - organizations/{orgID}/farms/{id}/fields
                    fields = get_fields_res(jdOrgID,jdFarmID,farmID=farmID,page=0)
                    # ****Debug Start****
                    if(debug):
                        location = 'get fields response'
                        file.write("\n"+"farmID - "+repr(farmID)+"\n")
                        file.write("fields - "+repr(fields)+"\n")
                    # ****Debug End****  
                    
                    #update fields info for farm
                    update_field_info(fields, farmID,0)

                    #set variables necessary for handling pagination
                    fieldsTotal = fields ['total']
                    pages = math.ceil(fieldsTotal / 10)
                    
                    # ****Debug Start****
                    if(debug):
                        file.write('fieldsTotal - '+repr(fieldsTotal)+"\n")
                        file.write('pages - '+repr(pages)+"\n")
                        file.write('pagesRange - '+repr(range(pages - 1))+"\n")
                    # ****Debug End****     
                    
                    #if pages > 1:
                    #    #iterate through pagination to acquire all available values
                    #    for i in range(pages - 1):
                    #        location = 'fields res pagination'+str(farmID)+"-"+str(i+1)
                    #
                    #        resLinks = fields['links']
                    #        # ****Debug Start****
                    #        if(debug):
                    #            file.write("\n"+"location - " + repr(location) + "\n")
                    #            file.write("resLinks - "+repr(resLinks)+"\n")                                
                    #        # ****Debug End**** 
                    #
                    #        for link in resLinks:
                    #            if link['rel']=='nextPage':
                    #                uri = link['uri']
                    #                fields = get_fields_res(jdOrgID, jdFarmID, uri, farmID, i+1)
                    #                
                    #                # ****Debug Start****
                    #                if(debug):
                    #                    location = 'get fields response page '+str(i+1)+' farm '+str(farmID)
                    #                    file.write("\n"+"location: "+repr(location)+"\n")
                    #                    file.write("i - "+repr(i)+"\n")
                    #                    file.write("farmID - "+repr(farmID)+"\n")
                    #                    file.write("fields - "+repr(fields)+"\n")
                    #                    file.write("url - "+repr(uri)+"\n")
                    #                    file.write('link called -'+repr(link)+"\n")
                    #                # ****Debug End****    
                    #    
                    #              #update fields info for farm
                    #                update_field_info(fields, farmID, i+1)
                    #              #break for loop and acquire next page
                    #                break
   
          #CALL API - data subscription service
            # ****Debug Start****
            if(debug):
                location = 'data subscription service'
            # ****Debug End****    
            
            dt = datetime.datetime.today()
            if dt.month>11:
                cropSeason = dt.year + 1
            else:
                cropSeason = dt.year
            
            connection = userTask.create_db_connection()
            #UPDATED
            #WOULD WE USE THE USER_JD_ORG_INFO TABLE?
            #WAS select_JDOrgIDs(str(ssOrgID))
            #query database for main and all connected organization id's  
            sqlQuery = userTask.select_jd_api_orgIDs_by_ssorgID_query()
            #UPDATED
            datasubOrgs = userTask.execute_select_query_vals(connection, sqlQuery,[str(ssOrgID)])
            
            sqlQuery = ''
            
            # ****Debug Start****
            if(debug):
                location = 'data subscript orgs info'
                file.write("\n"+"datasub orgs - "+repr(datasubOrgs)+"\n")
            # ****Debug End****
            
            for org in datasubOrgs:
                fieldsArr = []
                # ****Debug Start****
                if(debug):
                    file.write("datasub org - "+repr(org[0])+"\n")
                # ****Debug End****
                #UPDATED
                #query database for jd field id's for selected org
                sqlQuery = userTask.select_OrgFarmIDs_JDOrg()
                orgFarmIDs = userTask.execute_select_query_vals(connection, sqlQuery,[str(ssOrgID),str(org[0])])
                
                sqlQuery = ''
                
                # ****Debug Start****
                if(debug):
                    location = 'data subscript farms info'
                    file.write("datasub farms - "+repr(orgFarmIDs)+"\n")
                # ****Debug End****
                
                fieldCnt = 0
                reqFields = []
#                reqFields = ''
                
                for farm in orgFarmIDs:
                    # ****Debug Start****
                    if(debug):
                        file.write("datasub farm - "+repr(farm[0])+"\n")
                    # ****Debug End****
                    
                    #UPDATED
                    sqlQuery = userTask.select_OrgFieldIDs()
                    orgFields = userTask.execute_select_query_vals(connection, sqlQuery,[str(farm[0])])
                    
                    sqlQuery = ''
                    
                    for i in range(len(orgFields)):
                        reqFields.insert(fieldCnt, str(orgFields[i][0]))
                        fieldCnt = fieldCnt + 1

                    # ****Debug Start****
                    if(debug):
                        location = 'data subscript fields info'
                        file.write("datasub fields - "+repr(orgFields)+"\n")
                        file.write("datasub fieldCnt - "+repr(fieldCnt)+"\n")
                    # ****Debug End****
                    for field in orgFields:
                        fieldsArr.append(field[0])
                # ****Debug Start****
                if(debug):
                    location = 'get data subscript response'
                    file.write('ssOrgID - ' + repr(ssOrgID) + "\n")
                    file.write('jdOrgID - ' + repr(jdOrgID) + "\n") 
                # ****Debug End****
                #UPDATED
                #DO WE USE USER_JD_ORG_INFO TABLE?
                #query subscription name from jd_org_info table
                sqlQuery = userTask.select_JD_subscription_name_by_JD_API_org_ID_query()
                #UPDATED
                subName = userTask.execute_select_query_vals(connection,sqlQuery,[str(ssOrgID),str(jdOrgID)])
                    
                sqlQuery = ''
                
                token = 'ss' + str(ssOrgID) + '-' + str(jdOrgID)
                displayName = 'spraysafely Data Subscription ' + str(token)
                
                # ****Debug Start****
                if(debug):
                    file.write('token - ' + repr(token) + "\n")
                    file.write('reqFields - ' +str(reqFields) + "\n")
                # ****Debug End****
                
                subPostRes = None
                
                #check query
                if subName[0][0] != '':
                    location = 'subscription already exists'
                    
                    # ****Debug Start****
                    if(debug):
                        file.write('subName true - ' + repr(subName) + "\n")
                    # ****Debug End****
                    
                    #get subscription response call
                    subRes = get_EventSubscription(ssOrgID,jdOrgID)
                    # ****Debug Start****
                    if(debug):
                        location = 'data subscript response'
                        file.write("subRes - "+repr(subRes)+"\n")
                    # ****Debug End**** 
                    #break out subscription response variables
                    subID = subRes['id']
                    subFilters = subRes['filters']
                    subStatus = subRes['status']
                    subDisplayName = subRes['displayName']
                    subClientKey = subRes['clientKey']
                    subToken = subRes['token']
                    #UPDATED
                    #query database for subscription filters
                    #was .select_JDSubFilters(str(ssOrgID),str(jdOrgID))
                    sqlQuery = userTask.select_JD_subscription_filters_by_Org_ID_and_JD_API_org_ID_query()
                    #UPDATED
                    filters = userTask.execute_select_query_vals(connection,sqlQuery,[str(ssOrgID),str(jdOrgID)])
                    
                    # ****Debug Start****
                    if(debug):
                        file.write("subFilters - "+str(subFilters)+"\n")
                        file.write("filters - "+str(filters[0][0])+"\n")
                    # ****Debug End**** 
                    
                    sqlQuery = ''
                    
                    location = 'compare subscription filters'
                    updateSub_bool = compare_SubFilters(subRes,jdOrgID,reqFields,cropSeason)
                    #updateSub_bool = True
                    
                    # ****Debug Start****
                    if(debug):
                        file.write('updateSub_bool - ' + repr(updateSub_bool) + "\n")
                        file.write('subStatus - ' + repr(subStatus) + "\n")
                    # ****Debug End****
                    
                    if updateSub_bool == True:
                        #remove old subscription
                        status = 'Terminated'
                        subPutRes = update_DataSubscription(subID,status,subDisplayName,subToken)
                        #create new subscription
                        subPostRes = create_DataSubscription(jdOrgID, cropSeason, reqFields, displayName, token)
                        
                        # ****Debug Start****
                        if(debug):
                            location = 'data subscript update'
                            file.write("subPutRes - "+repr(subPutRes)+"\n")
                            file.write("subPostRes - "+repr(subPostRes)+"\n")
                        # ****Debug End**** 
                    else:
                        if (subStatus == 'Terminated'):
                            subPostRes = create_DataSubscription(jdOrgID, cropSeason, reqFields, displayName, token)
                            # ****Debug Start****
                            if(debug):
                                location = 'terminated data subscript updated'
                                file.write("newsubPutRes - "+repr(subPostRes)+"\n")
                        
                else:
                    location = 'create new subscription'
                    
                    # ****Debug Start****
                    if(debug):
                        file.write('subname false - ' + repr(subName) + "\n")
                    # ****Debug End****
                    
                    #UPDATED
                    #add token to database
                    sqlPost = userTask.update_JDSubToken()
                    
                    # ****Debug Start****
                    if(debug):
                        file.write('sqlPost - ' + repr(sqlPost) + "\n")
                    # ****Debug End****
                    
                    #UPDATED
                    userTask.execute_create_query_vals(connection,sqlPost,[token,str(ssOrgID),jdOrgID])
                    subPostRes = create_DataSubscription(jdOrgID, cropSeason, reqFields, displayName, token)
                    
                    # ****Debug Start****
                    if(debug):
                        file.write('subPostRes - ' + repr(subPostRes) + "\n")
                    # ****Debug End****
                
                if subPostRes:
                    location = 'update subscription info'
                    update_jdSubInfo(subPostRes,ssOrgID,jdOrgID)
   
            # ****Debug Start****
            if(debug):
                location = 'data subscript Fields array'
                file.write("fieldsArr - "+repr(fieldsArr)+"\n")
            # ****Debug End****          
            
            #redirectURL = 'https://www.spray-safely.com/userMain?username='+str(username)
            redirectURL = 'http://test.spray-safely.test:5000/login'
            
            # ****Debug Start****
            if(debug):
                location = 'function return'
                file.write("\n"+'location - '+location+"\n")
                file.write("time - "+str(datetime.datetime.now())+"\n")
                file.write("redirectURL: "+repr(redirectURL)+"\n")
                file.close()
            # ****Debug End****
            
            return redirect(redirectURL, code=302)
            
            #return index()
        except Exception as e:
            logging.exception(e)
            exceptFile.write("Exception - " + repr(e) + "\n")
            exceptFile.write("location - " + repr(location) + "\n")
            exceptFile.close()
            return render_error('Callback Procedure Error! '+"\n"+"\n"+"Location:"+"\n"+location+"\n"+"\n"+"Error:"+"\n"+str(e)) # + "\n" + "\n" + repr(request.query_string))
    else:
        return render_error('No Spray-Safely User Account')
        
        
@jd_app.route("/refresh-access-token")
def refresh_access_token():
    #debug = nt_debug_write_file("receiveEvent_Process_Exception")
    exceptFile = nt_debug_write_file("refreshAccessToken_exception")
    try:
        # **write a call to a procedure with username parameter that populates settings from userInfo database
        #rarely if ever will this be called from anywhere but the backend server while in the middle of a process
        #therefore it most likely doesn't not require an external flask sub address and can call the 
        #'refreshAccessToken' procedure from the currently running module process 
        
        # ****Debug Start****
        if(debug):
            file = nt_debug_write_file("flaskRefreshAccessToken")
            file.write("refreshAccess:" + "\n")
        # ****Debug End****
        
        #THIS WAS COMMENTED OUT
        userName = session['username']
        #THIS WASNT
        #userName = 'thorsonnw'
        
        #create connection to userInfo database
        connectionUser = userTask.create_db_connection() 
        #query user_id by username
        #UPDATED
        sqlUserID_query = userTask.select_userID_by_username_query()
            # ****Debug Start****
        if(debug):
            file.write("sqlUserID - " + repr(sqlUserID_query) + "\n")
            # ****Debug End****
    
        #UPDATED
        userID = userTask.execute_select_query_vals(connectionUser, sqlUserID_query, [str(userName)])
        userID = userID[0][0]
            # ****Debug Start****
        if(debug):
            file.write("userID - " + repr(userID) + "\n")
            # ****Debug End****
            
        #query org_id by user_id
        #UPDATED
        sqlOrgID_query = userTask.select_orgIDs_by_userID_query()
            # ****Debug Start****
        if(debug):
            file.write("sqlOrgID - " + repr(sqlOrgID_query) + "\n")
            # ****Debug End****
            
        #UPDATED
        orgID = userTask.execute_select_query_vals(connectionUser,sqlOrgID_query,[str(userID)])
        orgID = orgID[0][0]
            # ****Debug Start****
        if(debug):
            file.write("orgID - " + repr(orgID) + "\n")
            # ****Debug End****
        
        #UPDATED
        #ALSO THIS SAYS QUERY JDORGINFO BUT HAS ALWAYS BEEN AN ORGINFO QUERY
        #WAS .select_OrgInfo_byOrgID(str(orgID))
        #query jdorginfo by org_id
        sqlOrgInfo_query = userTask.select_JD_Org_Info_byOrgID()
            # ****Debug Start****
        if(debug):
            file.write("sqlOrgInfo - " + repr(sqlOrgInfo_query) + "\n")
            # ****Debug End****
            
        #UPDATED
        orgInfo = userTask.execute_select_query_vals(connectionUser, sqlOrgInfo_query,[str(orgID)])
        orgInfo = orgInfo[0]
            # ****Debug Start****
        if(debug):
            file.write("orgInfo - " + repr(orgInfo) + "\n")
            # ****Debug End****
        #populate settings with accessToken, refreshToken, expiration
        settings['accessToken'] = orgInfo[12]
        settings['refreshToken'] = orgInfo[13]
        settings['exp'] = orgInfo[14]
        
        # ****Debug Start****
        if(debug):
            file.write("settings - " + repr(settings) + "\n")
        # ****Debug End****
        
        refreshAccessToken(userName)
        
        #pass response to populate token info
        
        return '',http.HTTPStatus.OK
        
    except Exception as e:
        logging.exception(e)
        exceptFile.write("Exception - " + repr(e) + "\n")
        exceptFile.write("location - " + repr(location) + "\n")
        exceptFile.close()
        return render_error('Error getting refresh token!')
        
        
@jd_app.route("/time")       
def time():
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")
    cTime = current_time.replace(':','')
    
    save_Path = 'public_html/johndeere/cgi-bin/debug_Log/time'
    file_name = 'debugJDTime_' + cTime + ".txt"
    
    file = os.path.join(save_Path,file_name)
    
    debugFile = open(file,"w")
    
    debugFile.write("currentTimeStr - " + str(now) + "\n")
    debugFile.write("currentTimeRepr - " + repr(now) + "\n")    
    debugFile.close()
    
    return '', http.HTTPStatus.NO_CONTENT  
    
    
@jd_app.route("/receiveEvents",methods=['POST'])        #data subscription service endpoint response procedure
def receiveEvents():
    import threading
    
    cTime = datetime.datetime.now()

    # ****Debug Start****
    if(debug):
        file = nt_debug_write_file("receiveEvents")
        file.write("receiveEvents:" + "\n")
        file.write("time Received - " + str(cTime) + "\n")
    # ****Debug End****
    
    exceptFile = nt_debug_write_file("receiveEvents_exception")
    try:
        #get response
        response = request.json
        
        if response:
            # ****Debug Start****
            if(debug):
                file.write("response - " + repr(response) + "\n")
            # ****Debug End****
            
            thread = threading.Thread(target=receiveEvent_Process, kwargs={'response': response})
            thread.start()
        else:
            # ****Debug Start****
            if(debug):
                file.write("response - No Response" + "\n")
            # ****Debug End****
    
    except Exception as e:
        logging.exception(e)
        exceptFile.write('Exception - ' + repr(e) + "\n")
        exceptFile.close()
    
    exceptFile.close()
    
    # ****Debug Start****
    if(debug):
        file.close()
    # ****Debug End****
    
    return '', http.HTTPStatus.NO_CONTENT # returns 204 no content status to jd api server
    
    
def receiveEvent_Process(response):
    exceptFile = nt_debug_write_file("receiveEvents_Process_exception")
    
    try:
      #Parse Reponse for EventType, OperationType, FieldID, and OrganizationID (jd generated)
        cnt = 0
        for event in response:
            cnt += 1
            
            res_EventType = event['eventTypeId']
            res_Token = event['token']
            res_ClientKey = event['clientKey']
            
            # ****Debug Start****
            if(debug):
                fileStrt = nt_debug_write_file("receiveEvent_Process_"+str(res_Token))
                fileStrt.write("receiveEvent_Process:" + "\n")
                fileStrt.write("response - " + repr(response) + "\n")
                fileStrt.write("\n"+"event Instance - "+repr(cnt)+"\n")
                fileStrt.write("event - " + repr(event) + "\n")
                fileStrt.write("eventTypeID - " + repr(res_EventType) + "\n")
                fileStrt.write("eventToken - " + repr(res_Token)+ "\n")
                fileStrt.write("eventClientKey - " + repr(res_ClientKey) + "\n")
                fileStrt.close()
            # ****Debug End****
            
            #check for subscription verification
            if res_EventType != 'subscriptionVerification':
                for inst in event['metadata']:
                    if inst['key'] == 'fieldOperationType':
                        operType = inst['value']
                    elif inst['key'] == 'fieldId':
                        appFieldID = inst['value']
                    elif inst['key'] == 'orgId':
                        appOrgID = inst['value']
                
                # ****Debug Start****
                if(debug):
                    file = nt_debug_write_file("receiveEvent_Process"+str(appFieldID))
                    file.write("event operType - " + repr(operType) + "\n")
                    file.write("event fieldID - " + repr(appFieldID) + "\n")
                    file.write("event orgID - " + repr(appOrgID) + "\n")
                # ****Debug End****
        
                if res_EventType == 'fieldOperation' and operType == 'application':
                    #parse targetResource (jd generated)
                    res_TargetResource = event['targetResource'] # dataset url when calling back to acquire dataset
                    #parse application id from end of target resource string
                    for i in range(len(res_TargetResource)):
                        index = (len(res_TargetResource)-1)-i
                        if res_TargetResource[index] == '/':
                            idStart = index + 1
                            idEnd = len(res_TargetResource)
                            jdAppID = res_TargetResource[idStart:idEnd] #parse value based on index values and set to variable
                            break
                    
                    # ****Debug Start****
                    if(debug):
                        file.write("res_TargetResource: " + repr(res_TargetResource) + "\n")
                        file.write("jdAppID: " + repr(jdAppID) + "\n")
                        file.write("settings - " + repr(settings) + "\n")
                    # ****Debug End****
                    
                  #connect to application database
                    connectionApp = appTask.create_AppDB_Connection()
                    connectionUser = userTask.create_db_connection() 
                  #check id against 'JD_ReceivedEvents' table in the ssAppData database
                    #   NEED TO RETHINK THIS FOLLOWING QUERY - response is not providing an event id therefore the query will need to be 
                    #                                           based off of one of multiple of the following: jdorgID, clientkey, token,
                    #                                           fieldID, applicationID
                    
                    #UPDATED
                    #query OrgID by jdToken
                    #WAS .select_OrgID_byJDToken(res_Token)
                    #DON'T KNOW WHICH JD TOKEN THIS REFERS TO
                    sqlOrg_query = userTask.select_OrgID_by_JD_Sub_Token_query()
                    # ****Debug Start****
                    if(debug):
                        file.write("\n" + "Query Local Databases:" + "\n")
                        file.write("sqlOrg_query - " + repr(sqlOrg_query) + "\n")
                    # ****Debug End****
                    
                    #UPDATED
                    ssOrgID = userTask.execute_select_query_vals(connectionUser,sqlOrg_query,[res_Token])
                    ssOrgID = ssOrgID[0][0]
                    
                    #UPDATED
                    #WAS .select_App_byOrgJDAppID(jdAppID,str(ssOrgID))
                    #query Application by orgID and JDAppID
                    sqlApp_query = appTask.select_App_byOrgJDAppID_query()
                    # ****Debug Start****
                    if(debug):
                        file.write("ssOrgID - " + repr(ssOrgID) + "\n")
                        file.write("sqlApp_query - " + repr(sqlApp_query) + "\n")
                    # ****Debug End****
                    
                    #UPDATED
                    eventStatus = appTask.execute_select_query_vals(connectionApp,sqlApp_query,[jdAppID,str(ssOrgID)])
                    
                    #UPDATED
                    #query orgInfo by orgID
                    sqlOrgInfo_query = userTask.select_OrgInfo_byOrgID()
                    # ****Debug Start****
                    if(debug):
                        file.write("eventStatus - " + repr(eventStatus) + "\n")
                        file.write("sqlOrgInfo_query - " + repr(sqlOrgInfo_query) + "\n")
                    # ****Debug End****
                    #UPDATED
                    ssOrgInfo = userTask.execute_select_query_vals(connectionUser,sqlOrgInfo_query,[str(ssOrgID)])
                    
                    #UPDATED
                    #Org_Info doesn't have user ID anymore
                    #was userTask.select_UserID_byOrgID(str(ssOrgID))
                    #query userID by orgID
                    sqlUserID_query = userTask.select_userID_by_orgID_query()
                    # ****Debug Start****
                    if(debug):
                        file.write("sqlUserID - " + repr(sqlUserID_query) + "\n")
                    # ****Debug End****
            
                    #UPDATED
                    ssUserID = userTask.execute_select_query_vals(connectionUser, sqlUserID_query,[str(ssOrgID)])
                    ssUserID = ssUserID[0][0]
                    # ****Debug Start****
                    if(debug):
                        file.write("userID - " + repr(ssUserID) + "\n")
                    # ****Debug End****
                    
                    #query username by userID
                    #UPDATED FROM userTask.select_Username
                    sqlUserName_query = userTask.select_username_by_userID_query()
                    # ****Debug Start****
                    if(debug):
                        file.write("sqlUserName - " + repr(sqlUserName_query) + "\n")
                    # ****Debug End****

                    #UPDATED
                    ssUserName = userTask.execute_select_query_vals(connectionUser, sqlUserName_query,[str(ssUserID)])
                    ssUserName = str(ssUserName[0][0])
                    # ****Debug Start****
                    if(debug):
                        file.write("userName - " + repr(ssUserName) + "\n")
                    # ****Debug End****
                    
                    sqlOrg_query = ''
                    sqlApp_query = ''
                    sqlOrgInfo_query = ''
                    sqlUserID_query = ''
                    sqlUserName_query = ''
                        
                    # ****Debug Start****
                    if(debug):
                        file.write("\n" + "ssOrgInfo: " + "\n")
                        file.write("ssOrgInfo - " + repr(ssOrgInfo) + "\n")
                        file.write("accessToken - " + repr(ssOrgInfo[0][6]) + "\n")
                        file.write("refreshToken - " + repr(ssOrgInfo[0][7]) + "\n")
                        file.write("expiration - " + repr(ssOrgInfo[0][8]) + "\n")
                    # ****Debug End****
                        
                    #populate settings from User Database Query
                    settings['accessToken'] = ssOrgInfo[0][6]
                    settings['refreshToken'] = ssOrgInfo[0][7]
                    settings['exp'] = ssOrgInfo[0][8]
                    
                    # ****Debug Start****
                    if(debug):
                        file.write("ssOrgID - " + repr(ssOrgID) + "\n")
                        if (eventStatus):
                            file.write("eventStatus " + repr(eventStatus) + "\n")
                    # ****Debug End****
                    
                  #query jd org info from database using parsed response token
                    if not eventStatus:
                        # ****Debug Start****
                        if(debug):
                            location = 'Check Access Status'
                            file.write("Location - " + repr(location) + "\n")
                        # ****Debug End****
                        
                        if str(datetime.datetime.now()) > settings['exp']:
                            refreshAccessToken(ssUserName)
                            # ****Debug Start****
                            if(debug):
                                file.write('refreshedAccessToken' + "\n")
                            # ****Debug End****
                        
                        # ****Debug Start****
                        if(debug):
                            location = 'Create Application'
                            file.write("Location - " + repr(location) + "\n")
                        # ****Debug End****                        
                        
                      #create new application for all orgs associated with parsed jdToken]
                        # ****Debug Start****
                        if(debug):
                            file.write("settings - " + repr(settings) + "\n")
                        # ****Debug End****
                        
                        #obtain field operations request and store info to database
                        appRes = get_fieldOperations_res(str(jdAppID))
                        appResContent = appRes.json()
                        
                        # ****Debug Start****
                        if(debug):
                            file.write("appRes - " + repr(appRes) + "\n")
                            location = "request FieldOps"
                            file.write("location - " + repr(location) + "\n")
                            file.write("appRes Content - " + str(appResContent) + "\n")
                        # ****Debug End****
                       
                        statusCode = ''
                        for link in appResContent['links']:
                            # ****Debug Start****
                            if(debug):
                                file.write("link - " + str(link) + "\n")
                            # ****Debug End****
                            if link['rel'] == 'shapeFileAsync':
                                # ****Debug Start****
                                if(debug):
                                    file.write("linkURI - " + str(link['uri']) + "\n")
                                # ****Debug End****
                                
                                fieldOpsURL = link['uri']
                                break
                        
                        #check for fieldOps URL    
                        if (fieldOpsURL):
                            # ****Debug Start****
                            if(debug):
                                file.write("fieldOpsURL - " + repr(fieldOpsURL) + "\n")
                            # ****Debug End****
                            #call fieldOps Request
                            dataRes = get_fieldOps_res(str(jdAppID),fieldOpsURL)
                            statusCode = dataRes.status_code
                        else:
                            # ****Debug Start****
                            if(debug):
                                file.write("No fieldOps URL Stored to Variable" + "\n")
                            # ****Debug End****
                        
                        # ****Debug Start****
                        if(debug):
                        #    file.write("dataRes - " + repr(dataRes) + "\n")
                        #    file.write("dataRes content - " + repr(dataRes.content) + "\n" )
                            file.write("dataRes statuscode - " + repr(statusCode) + "\n")
                        # ****Debug End****
                        
                        
                        if statusCode == 200 or statusCode == 202 or statusCode == 307 or statusCode == 403:
                            #call data package status reponse
                            numberOfAttempts = 0
                            
                            # ****Debug Start****
                            if(debug):
                                file.write("\n" + "fieldOps statusCode - " + repr(statusCode) + "\n")
                                location = "start loop"
                                file.write("location - " + repr(location) + "\n")
                            # ****Debug End****
                            
                            datasetLoopBool = True
                            #loop until fieldops dataset is available for download and processed
                            loopStart = datetime.datetime.now()
                            loopMax = loopStart + datetime.timedelta(hours=3)
                            
                            # ****Debug Start****
                            if(debug):
                                file.write("loopStart - " + str(loopStart) + "\n")
                                file.write("loopMax - " + str(loopMax) + "\n")
                            # ****Debug End****
                            
                            while datasetLoopBool == True:
                                #limit loop to a 3 hour run time (after 3 hours, if file is not downloaded then exit loop after current iteration)
                                if loopMax <= datetime.datetime.now():
                                    datasetLoopBool = False
                                    
                                # ****Debug Start****
                                if(debug):
                                    file.write("\n" + "settings - " + repr(settings) + "\n")
                                    file.write("datasetLoopBool - " + repr(datasetLoopBool) + "\n")
                                    location = "loop request FieldOps"
                                    file.write("location - " + repr(location) + "\n")
                                # ****Debug End****
                                
                                if statusCode != 200:
                                    #check for fieldOps URL
                                    if (fieldOpsURL):
                                        # ****Debug Start****
                                        if(debug):
                                            file.write("loop fieldOpsURL - " + str(fieldOpsURL) + "\n")
                                        # ****Debug End****
                                        
                                        #call fieldOps Request
                                        dataRes = get_fieldOps(fieldOpsURL)
                                        statusCode = dataRes.status_code
                                        
                                        # ****Debug Start****
                                        if(debug):
                                            file.write('loop statusCode - ' + repr(statusCode) + "\n")
                                            file.write("loop dataRes - " + str(fieldOpsURL) + "\n")
                                        # ****Debug End****
                                        
                                
                                # ****Debug Start****
                                if(debug):
                                    file.write("fieldOps loop statusCode - " + repr(statusCode) + "\n")
                                    file.write("numberOfAttempts - " + repr(numberOfAttempts) + "\n")
                                # ****Debug End****
                                if statusCode == 307 or statusCode == 200:
                                    # ****Debug Start****
                                    if(debug):
                                        location = "loop dataset download"
                                        file.write("statusCode 307 - True"+"\n")
                                        file.write("location - " + repr(location) + "\n")
                                    # ****Debug End****
                                    if statusCode == 307:
                                        #parse reponse for targetEndpoint
                                        response = dataRes.json()
                                        url = dataRes['Location']
                                        # ****Debug Start****
                                        if(debug):
                                            location = 'loop 307 parse dataset download link'
                                            file.write("response fieldOps - " + repr(response) + "\n")
                                            file.write("download url - " + repr(url) + "\n")
                                            file.write("location - " + repr(location) + "\n")
                                        # ****Debug End****
                                        #call download targetEndpoint
                                        appDataZip = get_AppDataset_shp(url)
                                        # ****Debug Start****
                                        if(debug):
                                            location = "loop 307 parse zipfile"
                                            file.write("location - " + repr(location) + "\n")
                                            file.write("appDataZip - " + str(appDataZip) + "\n")
                                        # ****Debug End****
                                        appZipList = parseZip(appDataZip)
                                        filetype = 'zip'
                                        # ****Debug Start****
                                        if(debug):
                                            file.write("downloadFile status - " + repr(appDataZip.status_code) + "\n")
                                        # ****Debug End****
                                    elif statusCode == 200:
                                        # ****Debug Start****
                                        if (debug):
                                            location = "loop 200 parse zipfile"
                                            file.write("location - " + repr(location) + "\n")
                                        # ****Debug End****
                                        
                                        #appZipList = parseZip(dataRes)
                                        #filetype = 'zip'
                                        extractDir = 'public_html/johndeere/cgi-bin/shpDownload/'+str(jdAppID)
                                        appZipList,jsonDir = parseZip(dataRes,True,extractDir)
                                        filetype = 'shp'
                                    
                                    # ****Debug Start****
                                    if (debug):
                                        file.write('appZipList - ' + repr(appZipList) + "\n")
                                        location = "loop end loop/generate boundary"
                                        file.write("location - " + repr(location) + "\n")
                                    # ****Debug End****
                                    
                                #generate boundary from shapefile point data (downloaded from jdOpCenter API)
                                    buffPoly,hull_array,dataset = boundary.concave_hull(appZipList,filetype,0)
                                    if buffPoly:
                                        geometry = shapely.geometry.mapping(buffPoly)
                                        # ****Debug Start****
                                        if(debug):
                                            file.write("Geometry Conclusion Time - " + str(datetime.datetime.now())+ "\n")
                                            file.write("geometry - " + repr(geometry) + "\n")
                                            file.write("buffPoly - " + repr(buffPoly) + "\n")
                                        # ****Debug End****
                                    
                                    # ****Debug Start****
                                    if(debug):
                                        location = "Loop Load JSON"
                                        file.write("location - " + repr(location) + "\n")
                                    # ****Debug End****
                                    jsonFile = open(jsonDir)
                                    appJSON = json.load(jsonFile)
                                    
                                    # ****Debug Start****
                                    if(debug):
                                        file.write("appJSON - " + repr(appJSON) + "\n")
                                    # ****Debug End****
                                    
                                    datasetLoopBool = False
                                elif statusCode == 406:
                                    # ****Debug Start****
                                    if(debug):
                                        file.write("statusCode 406 - True" + "\n")
                                        file.write("non-downloadable dataset" + "\n")
                                        location = "loop 406 status"
                                        file.write("location - " + repr(location) + "\n")
                                    # ****Debug End****
                                    
                                    datasetLoopBool = False
                                else:
                                    numberOfAttempts = numberOfAttempts + 1
                                    # ****Debug Start****
                                    if(debug):
                                        location = "loop calculate sleep time"
                                        file.write("location - " + repr(location) + "\n")
                                        file.write("numberOfAttempts - " + repr(numberOfAttempts) + "\n")
                                    # ****Debug End****
                                    
                                    power = numberOfAttempts - 1
                                    # ****Debug Start****
                                    if(debug):
                                        file.write("power - " + repr(power) + "\n")
                                    # ****Debug End****
                                    
                                    noaPower = math.pow(2,power)
                                    # ****Debug Start****
                                    if(debug):
                                        file.write("noaPower - " + repr(noaPower) + "\n")
                                    # ****Debug End****
                                    
                                    secWait = 5*noaPower
                                    # ****Debug Start****
                                    if(debug):
                                        file.write("secWait - " + repr(secWait) + "\n")
                                        file.write("time before - " + str(datetime.datetime.now()) + "\n")
                                    # ****Debug End****
                                    
                                    #secWait = 5 * 2^(numberOfAttempts - 1)
                                    #datasetLoopBool = False
                                    
                                    sleep(secWait)
                                   
                                    # ****Debug Start****
                                    if(debug):
                                        file.write("time after - " + str(datetime.datetime.now()) + "\n")
                                    # ****Debug End****
                            
                            #insert application data in appData db
                            # ****Debug Start****
                            if(debug):
                                location = "Insert Application Instance"
                                file.write("location - " + repr(location) + "\n")
                            # ****Debug End****
                            
                            post_AppData(appRes,appJSON,ssOrgID,jdAppID,appOrgID,geometry)
                            
                            jsonFile.close()
                            
                            # ****Debug Start****
                            if(debug):
                                location = "End of Data Acquistion Operation"
                                file.write("location - " + repr(location) + "\n")
                            # ****Debug End****
                            
                            #ie the targetResource value obtained from the response
                        #this url returns a shapefile
                      #loop through all orgs and store information to application database
                        
                        #NOTE: need to determine if a check is necessary here. For instance, if you store the application for every 
                        #       organization associated with the jd org and field application and then receive a new subscription 
                        #       event for each of these spray safely organizations, you will end up with duplicates if you do not
                        #       contain some sort of check.
                        #       This check could consist of a simple comparison between event subscription org ID and the spray-safely 
                        #       orgId associated with the eventStatus query Return
                        #   The other option is to just call the application for each event subscription received and store the information
                        #       for that spray-safely organization only.    
                        #       (Downside to this is multiple calls to the jd api for the exact dataset information ; twice as much traffic and processing)
                    
                        #for org in eventOrgs:
                          #Pass field operations reponse to application database insert query
                            #connectionAppData = application database connection
                            #sqlQuery = application database query
                            #execute insert data query
                    
                    # ****Debug Start****
                    if(debug):   
                        file.close()
                    # ****Debug End****
                else:
                    # ****Debug Start****
                    if(debug):
                        file.write("non Field Operation" + "\n")
                        file.write("eventTypeID - " + repr(eventTypeID) + "\n")
                    # ****Debug End****
                
    except Exception as e:
        logging.exception(e)
        exceptFile.write("Exception - " + repr(e) + "\n")
        exceptFile.write("location - " + repr(location) + "\n")
        exceptFile.close()
            
        #return render_error('ReceiveEvents Procedure Error! '+"\n"+"\n"+"Location:"+"\n"+location+"\n"+"\n"+"Error:"+"\n"+str(e))
    
    exceptFile.close()



