import base64
import datetime
import uuid
import logging
import ssdebug
import requests
import json
import dbProc
from urllib import parse
from flask import request,make_response,redirect

debug = True

SERVER_URL='http://127.0.0.1:5000'
#SERVER_URL='http://spray-safely.co
#SERVER_URL='http://jd-test.spray-safely.test:5000'
#SERVER_URL='https://myjohndeere.deere.com/mjd/my/login'

settings = {
    'apiUrl': 'https://sandboxapi.deere.com/platform',
    'clientId': '0oavn0rxbVDnQyEYd5d6',
    'clientSecret': 'frhDA8LW5fpBirdhLkh1sMNr2pUzqd7PL5TS2Buwdf_8WV9VYM-7CY1k1L8XJd7s',
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


#   *   *   *   *   *   *   *   *   *   *   API Procedures   *   *   *   *   *   *   *   *   *   *

def get_api_settings():
    api_settings = settings
    return api_settings

def post_oauth_settings(res):
    #Store Information to system Memory
    json_response = res.json()
    token = json_response['access_token']
    settings['accessToken'] = token
    settings['refreshToken'] = json_response['refresh_token']
    settings['exp'] = str(datetime.datetime.now() + datetime.timedelta(seconds=json_response['expires_in']))
    (header, payload, sig) = token.split('.')
    payload += '=' * (-len(payload) % 4)
    settings['accessTokenDetails'] = json.dumps(json.loads(base64.urlsafe_b64decode(payload).decode()), indent=4)

def populate(data):
    settings['clientId'] = data['clientId']
    settings['clientSecret'] = data['clientSecret']
    settings['wellKnown'] = data['wellKnown']
    settings['callbackUrl'] = data['callbackUrl']
    settings['scopes'] = data['scopes']
    settings['state'] = data['state']


def needs_organization_access():
    """Check if another redirect is needed to finish the connection.

    Check to see if the 'connections' rel is present for any organization.
    If the rel is present it means the oauth application has not completed its
    access to an organization and must redirect the user to the uri provided
    in the link.
    """
    # ****Debug Start****
    if (debug):
        file = ssdebug.write_file("needs_orgAccess - jdAPI",'flask_Procedure')
        file.write("needs_orgAccess: " + "\n")
    # ****Debug End****
    
    try:
        addParameter = None
        payload = None
        location = 'api_res'
        api_res = api_get(settings['accessToken'], settings['apiUrl']+'/organizations',addParameter,payload)

        # ****Debug Start****
        if (debug):
            file.write("api_res: " +repr(api_res)+ "\n")
        # ****Debug End****

        location = 'api_response'
        api_response= api_res.json()
        
        # ****Debug Start****
        if (debug):
            file.write("apiResponse - "+repr(api_response)+"\n")
        # ****Debug End****
        
        location = 'api_response org loop'
        for org in api_response['values']:
            for link in org['links']:
                if link['rel'] == 'connections':
                    connectionsUri = link['uri']
                    query = parse.urlencode({'redirect_uri': settings['orgConnectionCompletedUrl']})
                    
                    # ****Debug Start****
                    if (debug):
                        file.write("query -  " + repr(query) + "\n")
                        file.close()
                    # ****Debug End****
                    
                    return f"{connectionsUri}?{query}"
        return None
    except Exception as e:
        logging.exception(e)
        exceptFile = ssdebug.write_file("needsOrgAceess_exception")
        exceptFile.write("Exception - " + repr(e) + "\n")
        exceptFile.write("location - " + repr(location) + "\n")
        exceptFile.close()
        return ssdebug.render_error('JD Org Access Error','Needs Organization Access Error! '+"\n"+"\n"+"Location:"+"\n"+location+"\n"+"\n"+"Error:"+"\n"+str(e)) # + "\n" + "\n" + repr(request.query_string))


def get_location_from_metadata(endpoint):
    response = requests.get(settings['wellKnown'])
    return response.json()[endpoint]


def get_oidc_query_string():
    query_params = {
        "client_id": settings['clientId'],
        "response_type": "code",
        "scope": parse.quote(settings['scopes']),
        "redirect_uri": settings['callbackUrl'],
        "state": settings['state'],
    }
    params = [f"{key}={value}" for key, value in query_params.items()]
    return "&".join(params)

def get_OAuth(code):
    try:
        # ****Debug Start****
        if(debug):
            file = ssdebug.write_file('get_OAuth','jdAPI_OAuth')
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
        
        post_oauth_settings(res)

        #return res
    except Exception as e:
        logging.exception(e)
        return ssdebug.render_error('Error Getting OAuth!')

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
            file = ssdebug.write_file("refreshAccessToken",'jdAPI_OAuth')
            file.write("refresh access token:" + "\n")
            file.write("headers - " + repr(headers) + "\n")
            file.write("payload - " + repr(payload) + "\n")
        # ****Debug End****
        
        res = requests.post(get_location_from_metadata('token_endpoint'), data=payload, headers=headers)
        
        # ****Debug Start****
        if (debug):
            file.write("response - " + repr(res) + "\n")
            file.write("res json - " + repr(res.json()) + "\n")

        post_oauth_settings(res)
        
        # ****Debug End****
        if username==None:
            dbProc.update_token_info(res,settings)
        else:
            dbProc.update_token_info(res,settings,username)
        
        #return index()
    except Exception as e:
        logging.exception(e)
        return ssdebug.render_error('Error getting refresh token!')


def get_basic_auth_header():
    return base64.b64encode(bytes(settings['clientId'] + ':' + settings['clientSecret'], 'utf-8'))



def api_get(access_token, resource_url, addParameter, payload):
    # ****Debug Start****
    if (debug):
        file = ssdebug.write_file("api_get",'jdAPI')
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
        file = ssdebug.write_file("api_post",'jdAPI')
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
        file = ssdebug.write_file("api_put",'jdAPI')
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
        file = ssdebug.write_file("call-api",'jdAPI')
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
        return ssdebug.render_error('Error calling API!')
        

def get_org_res():
    url = 'https://sandboxapi.deere.com/platform/organizations'
    payload = None        #no payload necessary
    addParameter = None     #no additional header parameters necessary
    method='GET'
    res = call_the_api(url, addParameter, payload, method)
    response = res.json()
    # ****Debug Start****
    if (debug):
        file = ssdebug.write_file("get-org",'jdAPI')
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
        file = ssdebug.write_file("get-farms",'jdAPI')
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
            file = ssdebug.write_file("get-fields"+str(farmID)+"-"+str(page),'jdAPI')
        elif farmID != None:
            file = ssdebug.write_file("get-fields"+str(farmID),'jdAPI')
        else:
            file = ssdebug.write_file("get-fields"+str(jdFarmID),'jdAPI')
        
        file.write("get-fields: " + "\n")
        file.write("url - " + repr(url) + "\n")
        file.write("res - " + repr(res) + "\n")
        file.write("response - " + repr(response) + "\n")
        file.write("apiResponse - " + repr(settings['apiResponse']) + "\n")
        file.close()
    # ****Debug End****
    return response
    

def get_fieldOps_res(jdOpID,targetEndpoint):
    # ****Debug Start****
    if (debug):
        file = ssdebug.write_file("get-fieldOpsRes",'jdAPI')
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
        file = ssdebug.write_file("get-fieldOps",'jdAPI')
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
        file = ssdebug.write_file("get-fieldOperations",'jdAPI')
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