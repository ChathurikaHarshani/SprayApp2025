import base64
import datetime
import json
import uuid
import logging
import http
import sys
import os
import math
from ntsqltasks import userdbTasks as userTask
from ntsqltasks import appdbTasks as appTask
#import pntbound.boundGen as boundary
from pntbound import boundGen as boundary
import zipfile
import shapefile
import shapely.geometry
import requests
import mysql.connector
import ssdebug
import dbProc
import jdAPI
import jdSub

from time import sleep
from io import BytesIO
from flask import Flask, render_template, request, redirect, session, make_response
#from flask import Flask, render_template, request, redirect, session, make_response,Blueprint

#app = Blueprint('johndeere',__name__, subdomain="jd-test")
app = Flask(__name__)
app.secret_key = "jdss88"

#DEBUG MODE - true = enabled ; false = disabled
debug = True



#   *   *   *   *   *   *   *   *   *   *   Local DB Procedures   *   *   *   *   *   *   *   *   *   *





    



#   *   *   *   *   *   *   *   *   *   *   Local API helper Procedures   *   *   *   *   *   *   *   *   *   *
    
def parseZip(resShp,extract=None,directory=None):
    # ****Debug Start****
    if(debug):
        file = ssdebug.write_file('get_parseZip')
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





#   *   *   *   *   *   *   *   *   *   *   Debug Procedures   *   *   *   *   *   *   *   *   *   *
#See ssdebug Library'




#   *   *   *   *   *   *   *   *   *   *   Flask Calls   *   *   *   *   *   *   *   *   *   *
@app.route("/jdaccess/")
def jdAccess():
    username = request.args['username']
    session['username'] = username
    redirect_url = '/'
    return redirect(redirect_url,code=302)


@app.route("/")
def start_oidc():
    try:
        username = session['username']
    except Exception as e:
        logging.exception(e)
        return ssdebug.render_error('Missing Username!')
    
#    return render_template('main.html', title='John Deere API with Python', settings=settings)
    
    location = 'database connection'
    # Create database connection
    connection = userTask.create_db_connection()
    sql = userTask.select_userID_by_username_query()
    userid = userTask.execute_select_query_vals(connection,sql, [username])

    
    try: 
        api_settings = jdAPI.get_api_settings()
        # ****Debug Start****
        if (debug):
            file = ssdebug.write_file("start_oidc",'flask_Procedure')
            file.write("start_oidc: " + "\n")
            file.write("username: " + repr(username) + "\n") #nt
            file.write("userId: " + repr(userid[0][0]) + "\n")
            file.write("settings:" + repr(api_settings) + "\n")
            file.write("settings length - " + repr(len(api_settings)) + "\n" )
            file.write("settings - callbackUrl: " + repr(api_settings['callbackUrl']) + "\n")
            file.write("settings - wellKnown: " + repr(api_settings['wellKnown']) + "\n")
        # ****Debug End****
        location = 'redirect url' 
        redirect_url = f"{jdAPI.get_location_from_metadata('authorization_endpoint')}?{jdAPI.get_oidc_query_string()}"
        
        # ****Debug Start****
        if(debug):
            file.write("redirect url -  " + repr(redirect_url) + "\n")
            file.close()
        # ****Debug End****

        return redirect(redirect_url, code=302)
    except Exception as e:
        logging.exception(e)
        exceptFile = ssdebug.write_file("start_oidc_exception")
        exceptFile.write("Exception - " + repr(e) + "\n")
        exceptFile.write("location - " + repr(location) + "\n")
        exceptFile.close()
        return ssdebug.render_error('JD OAuth2 Error - Start oidc','Error Auth!')


@app.route("/callback")
def callback():
    
    # ****Debug Start****
    if(debug):
        file = ssdebug.write_file("callback",'flask_Procedure')
        file.write("callback:" + "\n")
        location = 'username'
        file.write('location - ' + repr(location) + "\n")
    # ****Debug End****
    
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
        #ssOrgID = str(queryReturn)
        ssOrgID = str(queryReturn[0][0])
        
        sqlQuery = ''
        
        # ****Debug Start****
        if(debug):
            api_settings = jdAPI.get_api_settings()
            file.write("ssUserID: " + repr(ssUserID) + "\n")
            file.write("ssOrgID: " + repr(ssOrgID) + "\n")
            file.write("settings - " + "\n")
            for i in api_settings:
                file.write("\t" + repr(i) + " - " + repr(api_settings[i]) + "\n")
                if any(isinstance(i, list) for i in api_settings):
                    file.write("\t" + "length - " + repr(len(api_settings[i])) + "\n")
        
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
            
            #res = jdAPI.get_OAuth(code)
            jdAPI.get_OAuth(code)

            #re-acquire most recent jd api settings after update from get_OAuth method
            api_settings = jdAPI.get_api_settings()

            # ****Debug Start****
            if(debug): 
                file.write("url state - " + repr(request.args.get('state')) + "\n")
                file.write("code - " + repr(code) + "\n")
                file.write("reqArgs - " + repr(request.args) + "\n")
                #file.write("res - " + repr(res) + "\n")
                file.write("api settings - " + repr(api_settings) + "\n")
                location = 'update token info'
                file.write('location - '+location+"\n")
            # ****Debug End****

            #dbProc.update_token_info(api_settings)
            dbProc.update_token_info(api_settings,username)

            # ****Debug Start****
            if(debug):
                location = 'org access gen'
                file.write('location - '+location+"\n")
            # ****Debug End****
            
            organization_access_url = jdAPI.needs_organization_access()
            
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
                for i in api_settings:
                    file.write("\t" + repr(i) + " - " + repr(api_settings[i]) + "\n")
                    #file.write("\t\t" + repr(isinstance(settings[i],dict)) + "\n")
                    #if isinstance(settings[i],list):
                    #    file.write("\t" + "length - " + repr(len(settings[i])) + "\n")
            # ****Debug End****
            
        #Request remaining john deere account information    
          #CALL API - get oganizations response
            orgRes = jdAPI.get_org_res()
            # ****Debug Start****
            if (debug):
                location = "get jd org response"
                file.write("org res - " + repr(orgRes) + "\n")
            # ****Debug End****
            
            #update organization info in ssUser_Info DB
            orgs = dbProc.update_jdOrgInfo(orgRes,ssOrgID)     #sets self org name and id and returns list of all available orgs
            
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
                farms = jdAPI.get_farms_res(org['jdOrgID'])
                
                 # ****Debug Start****
                if(debug):
                    location = 'update farm info'
                    file.write("farms - "+repr(farms)+"\n")
                # ****Debug End****
                
                farmList = dbProc.update_farm_info(farms, jdOrgID, ssOrgID)
                # ****Debug Start****
                
                if(debug):
                    file.write("farmList - " + repr(farmList) + "\n")
                # ****Debug End****
                
          #CALL API - get fields response
                for farm in farmList:
                    farmID = farm['farmID']
                    jdFarmID = farm['jdFarmID']
                  #call api - organizations/{orgID}/farms/{id}/fields
                    fields = jdAPI.get_fields_res(jdOrgID,jdFarmID,farmID=farmID,page=0)
                    # ****Debug Start****
                    if(debug):
                        location = 'get fields response'
                        file.write("\n"+"farmID - "+repr(farmID)+"\n")
                        file.write("fields - "+repr(fields)+"\n")
                    # ****Debug End****  
                    
                    #update fields info for farm
                    dbProc.update_field_info(fields, farmID,0)

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
            sqlQuery = userTask.select_jd_api_orgID_by_orgID_query()
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
                    file.write('api_settings - ' + repr(api_settings) + "\n")
                # ****Debug End****

                #get subscription response call
                subRes = jdSub.get_EventSubscription(ssOrgID,jdOrgID,api_settings)

                # ****Debug Start****
                if(debug):
                    location = 'data subscript response'
                    file.write("subRes - "+repr(subRes)+"\n")
                # ****Debug End**** 

                if subRes['total']>0:
                    #break out subscription response variables per org subscription
                    for i in range(len(subRes['values'])):
                        subscript = subRes['values'][i]
                        subID = subscript['id']
                        subFilters = subscript['filters']
                        subStatus = subscript['status']
                        subDisplayName = subscript['displayName']
                        subClientKey = subscript['clientKey']
                        subToken = subscript['token']

                        # ****Debug Start****
                        if(debug):
                            file.write("\n")
                            file.write("i - "+repr(i)+"\n")
                            file.write("subscript - "+repr(subscript)+"\n")
                            file.write("subID - "+repr(subID)+"\n")
                            file.write("subFilters - "+repr(subFilters)+"\n")
                            file.write("subStatus - "+repr(subStatus)+"\n")
                            file.write("subDisplayName - "+repr(subDisplayName)+"\n")
                            file.write("subclientKey - "+repr(subClientKey)+"\n")
                            file.write("subToken - "+repr(subToken)+"\n")
                        # ****Debug End**** 
                        
                        # is this needed?
                        
                        if subStatus == 'Active':
                            #UPDATED
                            #query database for subscription filters
                            #was .select_JDSubFilters(str(ssOrgID),str(jdOrgID))
                            sqlQuery = ''
                            sqlQuery = userTask.select_JD_subscription_filters_by_Org_ID_and_JD_API_org_ID_query()
                            #UPDATED
                            filters = userTask.execute_select_query_vals(connection,sqlQuery,[str(ssOrgID),str(jdOrgID)])
                            
                            # ****Debug Start****
                            if(debug):
                                file.write("subFilters_1 - "+str(subFilters)+"\n")
                                file.write("filters - "+str(filters[0][0])+"\n")
                            # ****Debug End**** 
                            
                            sqlQuery = ''
                            
                            location = 'compare subscription filters'
                            updateSub_bool = jdSub.compare_SubFilters(subFilters,jdOrgID,reqFields,cropSeason)

                            # ****Debug Start****
                            if(debug):
                                file.write('updateSub_bool - ' + repr(updateSub_bool) + "\n")
                                file.write('subStatus - ' + repr(subStatus) + "\n")
                            # ****Debug End****

                            if updateSub_bool == True:
                                activeSub_bool = True
                                # ****Debug Start****
                                if(debug):
                                    location = 'subscription already exists'
                                    file.write("location - "+repr(location)+"\n")
                                    file.write("activeSub_bool - "+repr(activeSub_bool)+"\n")
                                # ****Debug End**** 
                                break
                            else:
                                # ****Debug Start****
                                if(debug):
                                    location = 'outdated data subscription'
                                    file.write("location - "+repr(location)+"\n")
                                # ****Debug End**** 

                                #remove old subscription
                                status = 'Terminated'
                                subPutRes = jdSub.update_DataSubscription(subID,status,subDisplayName,subToken)
                                activeSub_bool = False
                                # ****Debug Start****
                                if(debug):
                                    location = 'data subscript update'
                                    file.write("location - "+repr(location)+"\n")
                                    #file.write("subPutRes - "+repr(subPutRes)+"\n")
                                    file.write("activeSub_bool - "+repr(activeSub_bool)+"\n")
                                # ****Debug End**** 
                                break
                            
                        else:
                            activeSub_bool = False

                    if activeSub_bool == False:
                        # ****Debug Start****
                        if(debug):
                            location = 'no active subscriptions'
                            file.write("\n")
                            file.write("location - "+repr(location)+"\n")
                            file.write("activeSub_bool - "+repr(activeSub_bool)+"\n")
                            file.write("api_settings - "+repr(api_settings)+"\n")
                        # ****Debug End**** 
                        #create event subscripton (place where needed)
                        jdSub.create_DataSubscription(jdOrgID,ssOrgID,cropSeason,reqFields,api_settings)

                else:
                    # ****Debug Start****
                    if(debug):
                        location = 'no subscriptions'
                        file.write("location - "+repr(location)+"\n")
                        file.write("api_settings - "+repr(api_settings)+"\n")
                    # ****Debug End**** 
                    #create event subscripton (place where needed)
                    jdSub.create_DataSubscription(jdOrgID,ssOrgID,cropSeason,reqFields,api_settings)
                
                
                #### WRITE NEW EVENT SUBCRIPTION WORKFLOW #######
                '''
                #get subscription response call
                subRes = jdSub.get_EventSubscription(ssOrgID,jdOrgID,api_settings)

                # ****Debug Start****
                if(debug):
                    location = 'data subscript response'
                    file.write("subRes - "+repr(subRes)+"\n")
                # ****Debug End**** 

                #move to create subscription procedure?
                token = 'ss' + str(ssOrgID) + '-' + str(jdOrgID)
                displayName = 'spraysafely Data Subscription ' + str(token)
                
                # ****Debug Start****
                if(debug):
                    file.write('token - ' + repr(token) + "\n")
                    file.write('reqFields - ' +str(reqFields) + "\n")
                # ****Debug End****
                
                if subRes['total']>0:
                    #break out subscription response variables per org subscription
                    for subscript in subRes['values']:
                        subID = subscript['id']
                        subFilters = subscript['filters']
                        subStatus = subscript['status']
                        subDisplayName = subscript['displayName']
                        subClientKey = subscript['clientKey']
                        subToken = subscript['token']
                        
                        # is this needed?
                        
                        

                        if subStatus == 'Active':
                            #UPDATED
                            #query database for subscription filters
                            #was .select_JDSubFilters(str(ssOrgID),str(jdOrgID))
                            sqlQuery = ''
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
                            updateSub_bool = jdSub.compare_SubFilters(subRes,jdOrgID,reqFields,cropSeason)
                            #updateSub_bool = True

                            # ****Debug Start****
                            if(debug):
                                file.write('updateSub_bool - ' + repr(updateSub_bool) + "\n")
                                file.write('subStatus - ' + repr(subStatus) + "\n")
                            # ****Debug End****

                            if updateSub_bool == True:
                                break
                                #remove old subscription
                                status = 'Terminated'
                                subPutRes = jdSub.update_DataSubscription(subID,status,subDisplayName,subToken)
                                #create new subscription
                                subPostRes = jdSub.create_DataSubscription(jdOrgID, cropSeason, reqFields, displayName, token)
                                
                                # ****Debug Start****
                                if(debug):
                                    location = 'data subscript update'
                                    file.write("subPutRes - "+repr(subPutRes)+"\n")
                                    file.write("subPostRes - "+repr(subPostRes)+"\n")
                                # ****Debug End**** 
                        else:
                            file.write('place holder for create new subscription')

                                           
                
                else:
                    #create new subscription
                    file.write('place holder create subscription')

                #file.write("test")    
                '''
                '''
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
                    subRes = jdSub.get_EventSubscription(ssOrgID,jdOrgID,api_settings)
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
                    updateSub_bool = jdSub.compare_SubFilters(subRes,jdOrgID,reqFields,cropSeason)
                    #updateSub_bool = True
                    
                    # ****Debug Start****
                    if(debug):
                        file.write('updateSub_bool - ' + repr(updateSub_bool) + "\n")
                        file.write('subStatus - ' + repr(subStatus) + "\n")
                    # ****Debug End****
                    
                    if updateSub_bool == True:
                        #remove old subscription
                        status = 'Terminated'
                        subPutRes = jdSub.update_DataSubscription(subID,status,subDisplayName,subToken)
                        #create new subscription
                        subPostRes = jdSub.create_DataSubscription(jdOrgID, cropSeason, reqFields, displayName, token)
                        
                        # ****Debug Start****
                        if(debug):
                            location = 'data subscript update'
                            file.write("subPutRes - "+repr(subPutRes)+"\n")
                            file.write("subPostRes - "+repr(subPostRes)+"\n")
                        # ****Debug End**** 
                    else:
                        if (subStatus == 'Terminated'):
                            subPostRes = jdSub.create_DataSubscription(jdOrgID, cropSeason, reqFields, displayName, token)
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
                    subPostRes = jdSub.create_DataSubscription(jdOrgID, cropSeason, reqFields, displayName, token)
                    
                    # ****Debug Start****
                    if(debug):
                        file.write('subPostRes - ' + repr(subPostRes) + "\n")
                    # ****Debug End****
                
                if subPostRes:
                    location = 'update subscription info'
                    jdSub.update_jdSubInfo(subPostRes,ssOrgID,jdOrgID)
   
            # ****Debug Start****
            if(debug):
                location = 'data subscript Fields array'
                file.write("fieldsArr - "+repr(fieldsArr)+"\n")
            # ****Debug End****          
            '''
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
            exceptFile = ssdebug.write_file("callback_exception")
            exceptFile.write("Exception - " + repr(e) + "\n")
            exceptFile.write("location - " + repr(location) + "\n")
            exceptFile.close()
            return ssdebug.render_error('JD Callback Error - Callback','Callback Procedure Error! '+"\n"+"\n"+"Location:"+"\n"+location+"\n"+"\n"+"Error:"+"\n"+str(e)) # + "\n" + "\n" + repr(request.query_string))
    else:
        return ssdebug.render_error('JD Callback Error - Callback','No Spray-Safely User Account')
        
        
@app.route("/refresh-access-token")
def refresh_access_token():
        # **write a call to a procedure with username parameter that populates settings from userInfo database
        #rarely if ever will this be called from anywhere but the backend server while in the middle of a process
        #therefore it most likely doesn't not require an external flask sub address and can call the 
        #'refreshAccessToken' procedure from the currently running module process 
    try:    
        location = 'refreshAccessToken'
        api_settings = jdAPI.get_api_settings()
        # ****Debug Start****
        if(debug):
            file = ssdebug.write_file("flaskRefreshAccessToken-jdAPI",'flask_Procedure')
            file.write("refreshAccess:" + "\n")
        # ****Debug End****
        
        #THIS WAS COMMENTED OUT
        userName = session['username']
        #THIS WASNT
        #userName = 'thorsonnw'
        
        location = 'databaseConnection'
        #create connection to userInfo database
        connectionUser = userTask.create_db_connection() 
        #query user_id by username
        location = 'querybyUserName'
        #UPDATED
        sqlUserID_query = userTask.select_userID_by_username_query()
            # ****Debug Start****
        if(debug):
            file.write("sqlUserID - " + repr(sqlUserID_query) + "\n")
            # ****Debug End****
        location = 'executeQuery'
        #UPDATED
        userID = userTask.execute_select_query_vals(connectionUser, sqlUserID_query, [str(userName)])
        userID = userID[0][0]
            # ****Debug Start****
        if(debug):
            file.write("userID - " + repr(userID) + "\n")
            # ****Debug End****

        location = 'querybyUserID'    
        #query org_id by user_id
        #UPDATED
        sqlOrgID_query = userTask.select_orgIDs_by_userID_query()
            # ****Debug Start****
        if(debug):
            file.write("sqlOrgID - " + repr(sqlOrgID_query) + "\n")
            # ****Debug End****

        location = 'executeQuery'    
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
        #api_settings['accessToken'] = orgInfo[12]
        #api_settings['refreshToken'] = orgInfo[13]
        #api_settings['exp'] = orgInfo[14]
        
        # ****Debug Start****
        if(debug):
            file.write("settings - " + repr(api_settings) + "\n")
        # ****Debug End****
        
        jdAPI.refreshAccessToken(userName)
        
        #pass response to populate token info
        
        return '',http.HTTPStatus.OK
        
    except Exception as e:
        logging.exception(e)
        exceptFile = ssdebug.write_file("refreshAccessToken_exception")
        exceptFile.write("Exception - " + repr(e) + "\n")
        exceptFile.write("location - " + repr(location) + "\n")
        exceptFile.close()
        return ssdebug.render_error('Jd Refresh Token - Get Refresh Token','Error getting refresh token!')
        
        
@app.route("/time")       
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
    
    
@app.route("/receiveEvents",methods=['POST'])        #data subscription service endpoint response procedure
def receiveEvents():
    import threading
    
    cTime = datetime.datetime.now()

    # ****Debug Start****
    if(debug):
        file = ssdebug.write_file("receiveEvents-jdAPI",'flask_Procedure')
        file.write("receiveEvents:" + "\n")
        file.write("time Received - " + str(cTime) + "\n")
    # ****Debug End****
    
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
        exceptFile = ssdebug.write_file("receiveEvents_exception")
        exceptFile.write('Exception - ' + repr(e) + "\n")
        exceptFile.close()
    
    # ****Debug Start****
    if(debug):
        file.close()
    # ****Debug End****
    
    return '', http.HTTPStatus.NO_CONTENT # returns 204 no content status to jd api server
    
    
def receiveEvent_Process(response):
        
    try:
        api_settings = jdAPI.get_api_settings()
      #Parse Reponse for EventType, OperationType, FieldID, and OrganizationID (jd generated)
        cnt = 0
        for event in response:
            cnt += 1
            
            res_EventType = event['eventTypeId']
            res_Token = event['token']
            res_ClientKey = event['clientKey']
            
            # ****Debug Start****
            if(debug):
                fileStrt = ssdebug.write_file("receiveEvent_Process_"+str(res_Token),'flask_Procedure')
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
                    file = ssdebug.write_file("receiveEvent_Process"+str(appFieldID),'flask_Procedure')
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
                        file.write("settings - " + repr(api_settings) + "\n")
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
                    api_settings['accessToken'] = ssOrgInfo[0][6]
                    api_settings['refreshToken'] = ssOrgInfo[0][7]
                    api_settings['exp'] = ssOrgInfo[0][8]
                    
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
                        
                        if str(datetime.datetime.now()) > api_settings['exp']:
                            jdAPI.refreshAccessToken(ssUserName)
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
                            file.write("settings - " + repr(api_settings) + "\n")
                        # ****Debug End****
                        
                        #obtain field operations request and store info to database
                        appRes = jdAPI.get_fieldOperations_res(str(jdAppID))
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
                            dataRes = jdAPI.get_fieldOps_res(str(jdAppID),fieldOpsURL)
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
                                    file.write("\n" + "settings - " + repr(api_settings) + "\n")
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
                                        dataRes = jdAPI.get_fieldOps(fieldOpsURL)
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
                                        appDataZip = jdAPI.get_AppDataset_shp(url)
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
                            
                            dbProc.post_AppData(appRes,appJSON,ssOrgID,jdAppID,appOrgID,geometry)
                            
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
                        file.write("event operation Type - " + repr(operType) + "\n")
                    # ****Debug End****
                
    except Exception as e:
        logging.exception(e)
        exceptFile = ssdebug.write_file("receiveEvents_Process_exception")
        exceptFile.write("Exception - " + repr(e) + "\n")
        exceptFile.write("location - " + repr(location) + "\n")
        exceptFile.close()
            
        #return render_error('ReceiveEvents Procedure Error! '+"\n"+"\n"+"Location:"+"\n"+location+"\n"+"\n"+"Error:"+"\n"+str(e))



