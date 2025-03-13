import ssdebug
import jdAPI
import datetime
import base64
from flask import session
from ntsqltasks import userdbTasks as userTask
from ntsqltasks import appdbTasks as appTask

debug = True

def check_JDOrgInfo_entry(ssOrgID,jdOrgID):
    # ****Debug Start****
    if(debug):
        file = ssdebug.write_file('checkJDOrgInfoEntry','ssDatabase')
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
        

def update_token_info(api_settings,username=None):
  #Store Token Information to User Database
    # ****Debug Start****
    if(debug):
        file = ssdebug.write_file('updateToken','jdAPI_OAuth')
        file.write('username - ' + repr(username) + "\n")
        file.write('api settings: ' + repr(api_settings) + "\n")
    # ****Debug End****
    if username==None:
        username = session['username']
    
    accLvl = api_settings['scopes']
    tokenID = api_settings['idToken']
    accToken = api_settings['accessToken']
    refToken = api_settings['refreshToken']
    tokenExp = api_settings['exp']
    
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
            file.write('orgid: ' + repr(orgid) + "\n")
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
            updated_api_settings = jdAPI.get_api_settings()
            file.write('updated api settings:' + repr(updated_api_settings))
            file.close()
        # ****Debug End****
        
    else:
        return 'no username for available'


def update_jdOrgInfo(res, orgid):
    orgList =[]                             #list of organizations user has access to
    orgID = orgid
    # ****Debug Start****
    if (debug):
        file = ssdebug.write_file("update-orgInfo",'ssDatbase')
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


#
def update_farm_info(farms, jdOrgID, orgid):
    orgID = orgid
    # ****Debug Start****
    if (debug):
        file = ssdebug.write_file("update-farmInfo",'ssDatabase')
        file.write("update-farmInfo: " + "\n")  
        file.write("farms - " + repr(farms) + "\n")
        file.write("jdOrgID - " + repr(jdOrgID) + "\n")
        file.write("orgID - " + repr(orgID) + "\n")
        #file.write("orgID index 2:" + repr(orgID[2]) + "\n")
        #file.write("orgID index 0,0:" + repr(orgID[0][0]) + "\n")
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
            # ****Debug Start****
            if (debug):
                file.write("JDOrgIdQuery - " + repr(JDOrgIdQuery) + "\n")
            # ****Debug End****
            dbTbl_JDOrgID = userTask.execute_select_query_vals(connection,JDOrgIdQuery,[orgID,jdOrgID])
            # ****Debug Start****
            if (debug):
                file.write("dbTbl_JDOrgID - " + repr(dbTbl_JDOrgID) + "\n")
            # ****Debug End****
            dbTbl_JDOrgID = str(dbTbl_JDOrgID[0][0])
            vals = (str(jdFarmName),str(jdFarmID),str(orgID),str(dbTbl_JDOrgID),"")
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
            file = ssdebug.write_file("update-fieldInfo_"+str(farmID)+"_pg"+str(page),'ssDatabase')
        else:
            file = ssdebug.write_file("update-fieldInfo_"+str(farmID),'ssDatabase')
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


def post_AppData(appRes,appJSON,orgID,JDAppID,appOrgID,geometry):
    #obtain application values from field operations and fieldops dataset 
    #and then store them to the application database
    
    # ****Debug Start****
    if (debug):
        file = ssdebug.write_file("post-application",'jdAPI')
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
        

def post_org_res(res,orgID,api_settings):
    response = res.json()
    values = response['values']
    # ****Debug Start****
    if (debug):
        file = ssdebug.write_file("post-org",'jdAPI')
        file.write("post-org: " + "\n")  
        file.write("res - " + repr(res) + "\n")
        file.write("response - " + repr(response) + "\n")
        file.write("values - " + repr(values[0]) + "\n")
        for val in values:
            file.write("jdOrgID - " + repr(str(val['id'])) + "\n")
            file.write("jdOrgName - " + repr(str(val['name'])) + "\n")
        
        file.write("apiResponse - " + repr(api_settings['apiResponse']) + "\n")
        file.close()
    # ****Debug End****
    
    
#
def post_fieldOps_res(res,orgID,api_settings):
    response = res.json()
    # ****Debug Start****
    if (debug):
        file = ssdebug.write_file("post-fieldOps",'jdAPI')
        file.write("post-fieldOps: " + "\n")  
        file.write("res - " + repr(res) + "\n")
        file.write("response - " + repr(response) + "\n")
        file.write("apiResponse - " + repr(api_settings['apiResponse']) + "\n")
        file.close()
    # ****Debug End****



#
def post_farms_res(response,jdOrgID,orgID,api_settings):
    #for farm in response['values']:
        #query if farms already exist
        #if not present insert farm with info
            #call insert procedure
        #if present check info and update accordingly
            #call update procedure    
    
    # ****Debug Start****
    if (debug):
        file = ssdebug.write_file("post-farms",'jdAPI')
        file.write("post-farms: " + "\n")  
        file.write("res - " + repr(response) + "\n")
        file.write("response - " + repr(response) + "\n")
        file.write("apiResponse - " + repr(api_settings['apiResponse']) + "\n")
        file.close()
    # ****Debug End****

    

#
def post_fields_res(response,jdOrgID,jdFarmID,orgID,api_settings):
    
    #for field in response['values']:
        #query if field already present
        #if not present insert new field
            #call insert procedure
        #if present check info and update accordingly
            #call update procedure
    
    # ****Debug Start****
    if (debug):
        file = ssdebug.write_file("post-fields",'jdAPI')
        file.write("post-fields: " + "\n")  
        file.write("res - " + repr(response) + "\n")
        file.write("response - " + repr(response) + "\n")
        file.write("apiResponse - " + repr(api_settings['apiResponse']) + "\n")
        file.close()
    # ****Debug End****