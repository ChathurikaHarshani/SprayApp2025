from ntsqltasks import userdbTasks as userTask
import ssdebug
import jdAPI

debug = True

def get_EventSubscription(orgID,jdOrgID,settings):
    connection = userTask.create_db_connection()
    #query database for subscription id
    #UPDATED
    #REPLACE WITH select_JD_subscription_ID_by_JD_org_ID_query()?
    #was .select_JDSubID(str(orgID), str(jdOrgID))
    sqlQuery = userTask.select_JD_subscription_ID_by_Org_ID_and_JD_API_org_ID_query()
    #UPDATED
    #jdSubID = userTask.execute_select_query_vals(connection,sqlQuery,[str(orgID), str(jdOrgID)])
    # retrieve all jd operations event subscriptions for jdOrgID
    url = 'https://sandboxapi.deere.com/platform/eventSubscriptions/'#+jdSubID[0][0]
    payload = None
    addParameter = {'Content-Type':'application/vnd.deere.axiom.v3+json'}
    method='GET'
    
    # ****Debug Start****
    if (debug):
        file = ssdebug.write_file("get-EventSubscript",'jdAPI')
        file.write("get-Subscript: " + "\n")
        file.write("sqlQuery - " + str(sqlQuery) + "\n")
        #file.write("jdSubID - " + repr(jdSubID) + "\n")
        #file.write("jdSubID Parsed - " + repr(jdSubID[0][0]) + "\n")
        file.write("url - " + repr(url) + "\n")
    # ****Debug End****
    
    #CURRENT ERROR
    res = jdAPI.call_the_api(url, addParameter, payload, method)
    
    # ****Debug Start****
    if (debug):
        file.write("res - " + repr(res) + "\n")
    # ****Debug End****
    
    response = res.json()

    # ****Debug Start****
    if (debug):
        #file.write("res - " + repr(res) + "\n")
        file.write("response - " + repr(response) + "\n")
        file.write("apiResponse - " + repr(settings['apiResponse']) + "\n")
        file.close()
    # ****Debug End****
    return response

def create_DataSubscription(jdOrgID,ssOrgID,cropSeason,reqFields,settings):
    #move to create subscription procedure?
    token = 'ss' + str(ssOrgID) + '-' + str(jdOrgID)
    displayName = 'spraysafely Data Subscription ' + str(token)
    
    # ****Debug Start****
    if(debug):
        file = ssdebug.write_file("post-EventSubscript",'jdAPI')
        file.write('token - ' + repr(token) + "\n")
        file.write('reqFields - ' +str(reqFields) + "\n")
    # ****Debug End****
    
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
            'uri': 'http://development.johndeere.spray-safely.com/receiveEvents'
        },
        'displayName': displayName,
        'token': token
    }
    addParameter = {'Content-Type':'application/vnd.deere.axiom.v3+json'}
    method='POST'
    res = jdAPI.call_the_api(url,addParameter,payload, method)
    
    # ****Debug Start****
    if (debug):
        file = ssdebug.write_file("create_Subscription",'jdAPI')
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
        file = ssdebug.write_file("updateDataSub",'jdAPI')
        file.write("update-DataSub: " + "\n")
    # ****Debug End****
    
    # update current john deere operations center api data subscription
    url = 'https://sandboxapi.deere.com/platform/eventSubscriptions/'+subscriptionID
    payload = {
        'targetEndpoint':{
            'targetType': 'https',
            'uri': 'http://development.johndeere.spray-safely.com/receiveEvents'
        },
        'status': str(status),
        'displayName': str(displayName),
        'token': str(token)
    }
    addParameter = {'Content-Type':'application/vnd.deere.axiom.v3+json'}
    method='PUT'
    res = jdAPI.call_the_api(url,addParameter,payload, method)
    response = res.json()
    # ****Debug Start****
    if (debug):
        file.write("res - " + repr(res) + "\n")
        file.write("response - " + repr(response) + "\n")
        file.close()
    # ****Debug End****
    return response

#def compare_SubFilters(res,jdOrgID,fieldIDs,cropSeason):
def compare_SubFilters(resFilters,jdOrgID,fieldIDs,cropSeason):
    # procedure returns true if the subscription needs to be updated
    # and false if no updates are needed
    
    import numpy as np
    
    # ****Debug Start****
    if (debug):
        file = ssdebug.write_file("compareSubFilters",'ssDatabase')
        file.write("compareSubFilters: " + "\n")
        file.write("resFilters - "+repr(resFilters)+"\n")
        file.write("cropSeason - "+repr(cropSeason)+"\n")
        #file.write('res - ' + repr(res) + "\n")
        #file.write('resLen - ' + repr(len(res)) + "\n")
        #file.write('resFilters - ' + repr(res['filters']) + "\n")
    # ****Debug End****
    
    #resFilters = res['filters']
    
    jdOrgID = [str(jdOrgID)]
    cropSeason = [str(cropSeason)]
    
    # ****Debug Start****
    if (debug):
        file.write("resFilters - "+repr(resFilters)+"\n")
        file.write('jdOrgID - ' + repr(jdOrgID) + "\n")
        file.write("cropSeason - "+repr(cropSeason)+"\n")
        #file.write('resLen - ' + repr(len(res)) + "\n")
        #file.write('resFilters - ' + repr(res['filters']) + "\n")
    # ****Debug End****

    #set local variables
    for i in range(len(resFilters)):
        filterKey = resFilters[i]['key']
        filterValues = resFilters[i]['values']
    
        # ****Debug Start****
        if (debug):
            file.write('filterKey - ' + repr(filterKey) + "\n")
            file.write('filterValues - ' + repr(filterValues) + "\n")
        # ****Debug End****
        if filterKey == 'orgId':
            subOrgID = filterValues
        elif filterKey == 'fieldId':
            subFieldIDs = filterValues
        elif filterKey == 'cropSeason':
            subCropSeason = filterValues
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
        file = ssdebug.write_file("update-SubInfo",'ssDatabase')
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