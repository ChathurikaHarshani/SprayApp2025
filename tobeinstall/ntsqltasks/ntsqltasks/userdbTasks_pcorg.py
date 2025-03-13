# -*- coding: utf-8 -*-
#"""
#Created on Sat Jul 11 12:55:40 2020
#
#@author: thors
#"""



#   ************************************************************
#   ** Create 'ssUser_Info' Database Connection **
#   ************************************************************
def create_db_connection():
    import mysql.connector
    from mysql.connector.errors import Error
    
    try:
        connection = mysql.connector.connect(
            host = "208.109.60.84",
            user = "ssUser_Admin",
            password = "UNLSpraySafely1*",
            database = "ntUser_Info_Org",
        )
        if connection.is_connected():    
            print(connection)
            #cursor = connection.cursor()
            #print(cursor)
            return connection
    except Error as e:
        print(e)




#   ************************************************************
#   **** EXECUTE QUERY WITHIN MySQL DATABASE ****
#   * Description -  This procedure applies to any query within 
#                    this task file NOT requiring user information, 
#                    and applies to all spray-safely databases 
#                    designated within the query parameters.       
#   ************************************************************
def execute_Create_query(connection, sql_query):
    import mysql.connector
    from mysql.connector.errors import Error
    
    try:
        with connection.cursor(buffered=True) as cursor:
            cursor.execute(sql_query)
            connection.commit()
    except Error as e:
        print(e)




#   ************************************************************
#   **** EXECUTE QUERY WITHIN MySQL DATABASE ****
#   * Description -  This procedure applies to any query within 
#                    this task file requiring user information, 
#                    and applies to all spray-safely databases 
#                    designated within the query parameters.       
#   ************************************************************
def execute_Insert_query(connection, sql_query, vals):
    import mysql.connector
    from mysql.connector.errors import Error
    
    try:
        if connection:
            if vals:
                with connection.cursor() as cursor:
                    cursor.execute(sql_query,vals)
                    connection.commit()
                    
                return cursor.lastrowid
                cursor.close()
                connection.close()
            else:
                return "no info"
        else:
            return "failed connection"
    except Error as e:
        print (e)
        


#   ************************************************************
#   **** EXECUTE QUERY WITHIN MySQL DATABASE ****
#   * Description -  This procedure applies to any query within 
#                    this task file requiring user information, 
#                    and applies to all spray-safely databases 
#                    designated within the query parameters.       
#   ************************************************************
def execute_query(connection, sql_query):
    import mysql.connector
    from mysql.connector.errors import Error
    
    returnArr = []
    
    try:
        if connection:
            with connection.cursor() as cursor:
                cursor.execute(sql_query)
                records = cursor.fetchall()
                return records
            cursor.close()
            connection.close()
        else:
            return "failed connection"
    except Error as e:
        print (e)
        
        
#   ************************************************************
#   ** Main User_Info EVENT DATABASE STRUCTURE **
#   ************************************************************

#   ************************************************************
#   * Main Table *
#   ************************************************************
def create_UserInfo_tbl():
    create_UserInfo_tbl_query = """CREATE TABLE if not exists 
                                        User_Info(
                                            User_ID INT NOT NULL AUTO_INCREMENT,
                                            UserName text NOT NULL,
                                            Email text NOT NULL,
                                            Password text NOT NULL,
                                            Status text NOT NULL,
                                            PRIMARY KEY (User_ID)
                                         )"""
    return create_UserInfo_tbl_query
    
#   ************************************************************    
#   * Relational Tables *
#   ************************************************************
def create_OrgInfo_tbl():
    create_OrgInfo_table_query = """CREATE TABLE if not exists
                                            Org_Info(
                                                Org_ID INT NOT NULL AUTO_INCREMENT,
                                                Org_Name text NOT NULL,
                                                User_ID INT NOT NULL,
                                                JD_UserName text NOT NULL,
                                                JD_Access_lvl text NOT NULL,
                                                JD_TokenID text NOT NULL,
                                                JD_AccessToken text NOT NULL,
                                                JD_RefreshToken text NOT NULL,
                                                JD_TokenExpiration text NOT NULL,
                                                x_deere_signature text NOT NULL,
                                                Status text NOT NULL,
                                                PRIMARY KEY (Org_ID),
                                                FOREIGN KEY (User_ID)
                                                    REFERENCES User_Info(User_ID)
                                            )"""
    return create_OrgInfo_table_query

def create_JDOrgInfo_tbl():
    create_JDOrgInfo_table_query = """CREATE TABLE if not exists
                                            JD_OrgInfo(
                                                Org_ID INT NOT NULL,
                                                JD_OrgID INT NOT NULL,
                                                JD_OrgName text NOT NULL,
                                                JD_OrgType text NOT NULL,
                                                JD_Subscription_Token text NOT NULL,
                                                JD_Subscription_ClientKey text NOT NULL,
                                                JD_Subscription_Name text NOT NULL,
                                                JD_Subscription_ID text NOT NULL,
                                                JD_Subscription_Filters text NOT NULL,
                                                FOREIGN KEY (Org_ID)
                                                    REFERENCES User_Info(Org_ID)
                                            )"""
    return create_JDOrgInfo_table_query
 
def create_FarmInfo_tbl():
    create_FarmInfo_table_query = """CREATE TABLE if not exists 
                                            Farm_Info(
                                                Farm_ID INT NOT NULL AUTO_INCREMENT,
                                                Farm_Name text NOT NULL,
                                                Org_ID INT NOT NULL,
                                                JD_FarmID text NOT NULL,
                                                JD_OrgID INT NOT NULL,
                                                PRIMARY KEY (Farm_ID),
                                                FOREIGN KEY (Org_ID)
                                                    REFERENCES Org_Info(Org_ID),
                                                FOREIGN KEY (JD_OrgID)
                                                    REFERENCES JD_OrgInfo(JD_OrgID)
                                            )"""
    return create_FarmInfo_table_query

def create_FieldInfo_tbl():
    create_FieldInfo_table_query = """CREATE TABLE if not exists 
                                            Field_Info(
                                                Field_ID INT NOT NULL AUTO_INCREMENT,
                                                Field_Name text NOT NULL,
                                                Farm_ID INT NOT NULL,
                                                JD_FarmID INT NOT NULL,
                                                PRIMARY KEY (Field_ID),
                                                FOREIGN KEY (Farm_ID)
                                                    REFERENCES Farm_Info(Farm_ID)
                                            )"""
    return create_FieldInfo_table_query

#***********************************************************************************************************************************   
# ** <user>_Fields Table  ** 
#   ** This will be a separate table for every
#       user in the database. This will contain
#       every field accessible by the user,
#       regardless of farm or organization name.
    
#def create UserFields_tbl():
#    create_UserFields_table_query = """CREATE TABLE IF NOT EXISTS 
#                                            User_Info(
#                                                User_ID INT NOT NULL,
#                                                Owner_ID INT NOT NULL,
#                                                First_Name text NOT NULL,
#                                                Last_Name text NOT NULL,
#                                                Email text NOT NULL,
#                                                Username text NOT NULL,
#                                                Password text NOT NULL,
#                                                Access_Type text NOT NULL,
#                                                User_Type text NOT NULL,
#                                                Training_Date text NOT NULL,
#                                                Instructor_ID INT NOT NULL,
#                                                Status text NOT NULL,
#                                                PRIMARY KEY (User_ID),
#                                                FOREIGN KEY (Owner_ID) 
#                                                    REFERENCES Owner_Info(Owner_ID),
#                                                FOREIGN KEY (Instructor_ID) 
#                                                    REFERENCES Instructor_Info(Instructor_ID)
#                                            )"""
#    return create_UserFields_table_query
#***********************************************************************************************************************************



#   ************************************************************
#   *** MANIPULATE DATABASE TABLE DATA ***
#   * Description - 
#   ************************************************************

        
#   ************************************************************
#   ** Insert Table Information **
#   ************************************************************
def insert_User():
    insert_User_post = """INSERT INTO 
                                User_Info(
                                    UserName,
                                    Email,
                                    Password,
                                    Status                                        
                                )
                                VALUES (%s,%s,%s,%s);"""
    return insert_User_post
    
def insert_Org():
    insert_Org_post = """INSERT INTO
                                Org_Info(
                                    Org_Name,
                                    User_ID,
                                    JD_UserName,
                                    JD_Access_lvl,
                                    JD_TokenID,
                                    JD_AccessToken,
                                    JD_RefreshToken,
                                    JD_TokenExpiration,
                                    x_deere_signature,
                                    Status
                                )
                                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"""
    return insert_Org_post

def insert_JDOrg():
    insert_JDOrg_post = """INSERT INTO
                                JD_OrgInfo(
                                    Org_ID,
                                    JD_OrgID,
                                    JD_OrgName,
                                    JD_OrgType,
                                    JD_Subscription_Token,
                                    JD_Subscription_ClientKey,
                                    JD_Subscription_Name,
                                    JD_Subscription_ID,
                                    JD_Subscription_Filters
                                )
                                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);"""
    return insert_JDOrg_post

def insert_Farm():
    insert_Farm_post = """INSERT INTO
                                Farm_Info(
                                    Farm_Name,
                                    Org_ID,
                                    JD_FarmID,
                                    JD_OrgID
                                )
                                VALUES (%s,%s,%s,%s);"""
    return insert_Farm_post

def insert_Field():
    insert_Field_post = """INSERT INTO
                                Field_Info(                                                               
                                    Field_Name,
                                    Farm_ID,
                                    JD_FieldID
                                )
                                VALUES (%s,%s,%s);"""
    return insert_Field_post
    
    
#   ************************************************************    
#   ** Update Table Information **
#   ************************************************************
def update_JDAccess(accLvl,tokenID,accToken,refToken,tokenExp,orgID):
    update_JDAccess_post = "UPDATE Org_Info SET `JD_Access_lvl`='" + accLvl + "',`JD_TokenID`='" + tokenID + "',`JD_AccessToken`='" + accToken\
                            + "',`JD_RefreshToken`='" + refToken + "',`JD_TokenExpiration`='" + tokenExp + "' WHERE `Org_ID`='" + orgID + "'"
    # call parameter Structure - query, values = (JD_Access_lvl, JD_TokenID, JD_AccessToken, JD_RefreshToken, JD_TokenExpiration, Org_ID)exit
    return update_JDAccess_post
    
def update_UserPassword_byID(password,userID):
    update_UserPassword_byID_post = "UPDATE User_Info SET `Password`='" + password + "' WHERE `User_ID`='" + userID + "'"
    return update_UserPassword_byID_post

def update_UserPassword_byUserName(password,userName):
    update_UserPassword_byUserName_post = "UPDATE User_Info SET `Password`='" + password + "' WHERE `UserName`='" + userName + "'"
    return update_UserPassword_byUserName_post

def update_UserPassword_byEmail(password,email):
    update_UserPassword_byEmail_post = "UPDATE User_Info SET `Password`='" + password + "' WHERE `Email`='" + email + "'"
    return update_UserPassword_byEmail_post

def update_UserStatus(status,userID):
    update_UserStatus_post = "UPDATE User_Info SET `Status`='" + status + "' WHERE `User_ID`='" + userID + "'"
    return update_UserStatus_post

def update_OrgName(orgName,orgID):
    update_OrgName_post = "UPDATE Org_Info SET `Org_Name`='" + orgName + "' WHERE `Org_ID`='" + orgID + "'"
    return update_OrgName_post

def update_JDOrgID(jdOrgID,orgID):
    update_JDOrgID_post = "UPDATE JD_OrgInfo SET `JD_OrgID`='" + jdOrgID + "' WHERE `Org_ID`='" + orgID + "'"
    return update_JDOrgID_post

def update_JDOrgName(jdOrgName,orgID):
    update_JDOrgName_post = "UPDATE JD_OrgInfo SET `JD_OrgName`='" + jdOrgName + "' WHERE `Org_ID`='" + orgID + "'"
    return update_JDOrgName_post
    
def update_JDOrgType(jdOrgType,orgID,jdOrgID):
    update_JDOrgType_post = "UPDATE JD_OrgInfo SET `JD_OrgType`='" + jdOrgType + "' WHERE `Org_ID`='" + orgID + "' AND `JD_OrgID`='" + jdOrgID + "'"
    return update_JDOrgType_post
    
    #write jd subscription info update
def update_JDSubToken(orgID, jdOrgID, token):
    update_JDSubToken_post = "UPDATE JD_OrgInfo SET `JD_Subscription_Token`='" + token + "' WHERE `Org_ID`='" + orgID + "' AND `JD_OrgID`='" + jdOrgID + "'"
    return update_JDSubToken_post
    
def update_JDSubClientKey(orgID, jdOrgID, clientKey):
    update_JDSubClientKey_post = "UPDATE JD_OrgInfo SET `JD_Subscription_ClientKey`='" + clientKey + "' WHERE `Org_ID`='" + orgID + "' AND `JD_OrgID`='" + jdOrgID + "'"
    return update_JDSubClientKey_post

def update_JDSubName(orgID, jdOrgID, displayName):
    update_JDSubName_post = "UPDATE JD_OrgInfo SET `JD_Subscription_Name`='" + displayName + "' WHERE `Org_ID`='" + orgID + "' AND `JD_OrgID`='" + jdOrgID + "'"
    return update_JDSubName_post
    
def update_JDSubID(orgID, jdOrgID, subID):
    update_JDSubID_post = "UPDATE JD_OrgInfo SET `JD_Subscription_ID`='" + subID + "' WHERE `Org_ID`='" + orgID + "' AND `JD_OrgID`='" + jdOrgID + "'"
    return update_JDSubID_post
    
def update_JDSubFilters(orgID, jdOrgID, subFilters):
    update_JDSubFilters_post = "UPDATE JD_OrgInfo SET `JD_Subscription_Filters`=" + subFilters + " WHERE `Org_ID`='" + orgID + "' AND `JD_OrgID`='" + jdOrgID + "'"
    return update_JDSubFilters_post
    
def update_FarmName(farmName,farmID):
    update_FarmName_post = "UPDATE Farm_Info SET `Farm_Name`='" + farmName + "' WHERE `Farm_ID`='" + farmID + "'"
    return update_FarmName_post
    
def update_FieldName(fieldName, fieldID):
    update_FieldName_post = "UPDATE Field_Info SET `Field_Name`='" + fieldName + "' WHERE `Field_ID`='" + fieldID + "'"
    return update_FieldName_post

   
#   ************************************************************
#   ** Delete Table Information **
#   ************************************************************
def delete_User(userID):
    delete_User_post = "DELETE FROM User_Info WHERE `User_ID`='" + userID + "'"
    return delete_User_post

def delete_Org(orgID):
    delete_Org_post = "DELETE FROM Org_Info WHERE `Org_ID`='" + orgID + "'"
    return delete_Org_post
    
def delete_JDOrg(orgID,jdOrgID):
    delete_JDOrg_post = "DELETE FROM JD_OrgInfo WHERE `Org_ID`='" + orgID + "' AND `JD_OrgID`='" + jdOrgID + "'"
    return delete_Org_post
    
def delete_Farm(farmID):
    delete_Farm_post = "DELETE FROM Farm_Info WHERE `Farm_ID`='" + farmID + "'"
    return delete_Farm_post 
    
def delete_Field(fieldID):
    delete_Field_post = "DELETE FROM Field_Info WHERE `Field_ID`='" + fieldID + "'"
    return delete_Field_post
    
    
#   ************************************************************
#   ** Query Table Information **
#   ************************************************************

#       * JD Information
def select_JDAccessToken(orgID):
    select_JDAccessToken_query = "SELECT JD_AccessToken FROM Org_Info WHERE `Org_ID`='" + orgID + "'"
    return select_JDAccessToken_query

def select_JDRefreshToken(orgID):
    select_JDRefreshToken_query = "SELECT JD_RefreshToken FROM Org_Info WHERE `Org_ID`='" + orgID + "'"
    return select_JDRefreshToken_query
 
def select_JDTokenExpiration(orgID):
    select_JDTokenExpiration_query = "SELECT JD_TokenExpiration FROM Org_Info WHERE `Org_ID`='" + orgID + "'"
    return select_JDTokenExpiration_query
    
#       * JD Org Information Table
def select_JDOrgID(orgID, jdOrgID): #queries individual jd org id to check if jd org exists in database
    select_JDOrgID_query = "SELECT JD_OrgID FROM JD_OrgInfo WHERE `Org_ID`='" + orgID + "' AND `JD_OrgID`='" + jdOrgID + "'"
    return select_JDOrgID_query
    
def select_jd_api_orgIDs_by_ssorgID_query(orgID): #queries all jd org id's from database for specific org account
    select_JDOrgIDs_query = "SELECT JD_OrgID FROM JD_OrgInfo WHERE `Org_ID`='" + orgID + "'"
    return select_JDOrgIDs_query

def select_JDOrgName(orgID, jdOrgID):
    select_JDOrgName_query = "SELECT JD_OrgName FROM JD_OrgInfo WHERE `Org_ID`='" + orgID + "' AND `JD_OrgID`='" + jdOrgID + "'"
    return select_JDOrgName_query

def select_JDOrgType(orgID, jdOrgID):
    select_JDOrgType_query = "SELECT JD_OrgType FROM JD_OrgInfo WHERE `Org_ID`='" + orgID + "' AND `JD_OrgID`='" + jdOrgID + "'"
    return select_JDOrgType_query

def select_JDSubName(orgID, jdOrgID):
    select_JDSubName_query = "SELECT JD_Subscription_Name FROM JD_OrgInfo WHERE `Org_ID`='" + orgID + "' AND `JD_OrgID`='" + jdOrgID + "'"
    return select_JDSubName_query

def select_JDSubName_byJDToken(jdToken):
    select_JDSubName_byJDToken_query = "SELECT JD_Subscription_Name FROM JD_OrgInfo WHERE `JD_Subscription_Token`='" + jdToken + "'"
    return select_JDSubName_byJDToken_query

def select_JDSubToken(orgID, jdOrgID):
    select_JDSubToken_query = "SELECT JD_Subscription_Token FROM JD_OrgInfo WHERE `Org_ID`='" + orgID + "' AND `JD_OrgID`='" + jdOrgID + "'"
    return select_JDSubToken_query
    
def select_JDSubClientKey(orgID, jdOrgID):
    select_JDSubClientKey_query = "SELECT JD_Subscription_ClientKey FROM JD_OrgInfo WHERE `Org_ID`='" + orgID + "' AND `JD_OrgID`='" + jdOrgID + "'"
    return select_JDSubClientKey_query
    
def select_JDSubID(orgID, jdOrgID):
    select_JDSubID_query = "SELECT JD_Subscription_ID FROM JD_OrgInfo WHERE `Org_ID`='" + orgID + "' AND `JD_OrgID`='" + jdOrgID + "'"
    return select_JDSubID_query
    
def select_JDSubFilters(orgID, jdOrgID):
    select_JDSubFilters_query = "SELECT JD_Subscription_Filters FROM JD_OrgInfo WHERE `Org_ID`='" + orgID + "' AND `JD_OrgID`='" + jdOrgID + "'"
    return select_JDSubFilters_query
    

#       * Specific Information Sets
def select_UserID(password,email):
    select_UserID_query = "SELECT User_ID FROM User_Info WHERE `Password`='" + password + "' AND `Email`='" + email + "'"
    return select_UserID_query

def select_UserID_byOrgID(orgID):
    select_UserID_byOrgID_query = "SELECT User_ID FROM Org_Info WHERE `Org_ID`='" + orgID + "'"
    return select_UserID_byOrgID_query

def select_userID_by_username_query(userName):
    select_UserID_query = "SELECT User_ID FROM User_Info WHERE `UserName`='" + userName + "'" 
    return select_UserID_query

def select_UserName(userID):
    select_UserName_query = "SELECT UserName FROM User_Info WHERE `User_ID`='" + userID + "'"
    return select_UserName_query
    
def select_UserStatus(userID):
    select_UserStatus_query = "SELECT Status FROM User_Info WHERE `User_ID`='" + userID + "'"
    return select_UserStatus_query

def select_orgIDs_by_userID_query(userID):
    select_OrgID_query = "SELECT Org_ID FROM Org_Info WHERE `User_ID`='" + userID + "'"
    return select_OrgID_query

def select_OrgID_byJDToken(jdToken):
    select_OrgID_byJDToken_query = "SELECT Org_ID FROM JD_OrgInfo WHERE `JD_Subscription_Token`='" + jdToken + "'"
    return select_OrgID_byJDToken_query

def select_FarmID(orgID):
    select_FarmID_query = "SELECT Farm_ID FROM Farm_Info WHERE `Org_ID`='" + orgID + "'"
    return select_FarmID_query
    
def select_FarmID_byJDFarmIDssOrgID(jdFarmID,orgID):
    select_FarmID_byJDFarmIDssOrgID_query = "SELECT Farm_ID FROM Farm_Info WHERE `JD_FarmID`='" + jdFarmID + "' AND `Org_ID`='" + orgID + "'"
    return select_FarmID_byJDFarmIDssOrgID_query

def select_FarmID_byJDFieldID(jdFieldID):
    select_FarmID_byJDFieldID_query = "SELECT Farm_ID FROM Field_Info WHERE `JD_FieldID`='" + jdFieldID + "'"
    return select_FarmID_byJDFieldID_query

def select_FarmName(farmID):
    select_FarmName_query = "SELECT Farm_Name FROM Farm_Info WHERE `Farm_ID`='" + farmID + "'"
    return select_FarmName_query
    
def select_FieldID(farmID):
    select_FieldID_query = "SELECT Field_ID FROM Field_Info WHERE `Farm_ID`='" + farmID + "'"
    return select_FieldID_query
    
def select_FieldID_byJDFieldID(jdFieldID):
    select_FieldID_byJDFieldID_query = "SELECT Field_ID FROM Field_Info WHERE `JD_FieldID`='" + jdFieldID + "'"
    return select_FieldID_byJDFieldID_query

def select_FieldID_byJDFieldIDssFarmID(jdFieldID,farmID):
    select_FieldID_byJDFieldIDssFarmID_query = "SELECT Field_ID FROM Field_Info WHERE `JD_FieldID`='" + jdFieldID + "' AND `Farm_ID`='" + farmID +"'"
    return select_FieldID_byJDFieldIDssFarmID_query

def select_FieldName(fieldID):
    select_FieldName_query = "SELECT Field_Name FROM Field_Info WHERE `Field_ID`='" + fieldID + "'"
    return select_FieldName_query

def select_JDOrgFarmIDs(orgID,jdOrgID):
    select_JDOrgFarmIDs_query = "SELECT JD_FarmID FROM Farm_Info WHERE `Org_ID`='" + orgID + "' AND `JD_OrgID`='" + jdOrgID + "'"
    return select_JDOrgFarmIDs_query

def select_OrgFarmIDs(orgID):
    select_OrgFarmIDs_query = "SELECT Farm_ID FROM Farm_Info WHERE `Org_ID`='" + orgID + "'"
    return select_OrgFarmIDs_query

def select_OrgFarmIDs_JDOrg(orgID,jdOrgID):
    select_OrgFarmIDs_JDOrg_query = "SELECT Farm_ID FROM Farm_Info WHERE `Org_ID`='" + orgID + "' AND `JD_OrgID`='" + jdOrgID + "'"
    return select_OrgFarmIDs_JDOrg_query

def select_OrgFieldIDs(farmID):
    select_OrgFieldIDs_query = "SELECT JD_FieldID FROM Field_Info WHERE `Farm_ID`='" + farmID + "'"
    return select_OrgFieldIDs_query


#       * Entire Information Sets
def select_User(password,email):
    select_User_query = "SELECT * FROM User_Info WHERE `Password`='" + password + "' AND `Email`='" + email + "'"
    return select_User_query

def select_FarmInstance(orgID,jdOrgID,jdFarmID):
    select_FarmInstance_query = "SELECT * FROM Farm_Info WHERE `Org_ID`='"+orgID+"' AND `JD_OrgID`='"+jdOrgID+"' AND `JD_FarmID`='"+jdFarmID+"'"
    return select_FarmInstance_query
    
def select_FieldInstance(farmID,jdFieldID):
    select_FarmInstance_query = "SELECT * FROM Field_Info WHERE `Farm_ID`='" + farmID + "' AND `JD_FieldID`='" + jdFieldID + "'"
    return select_FarmInstance_query

def select_OrgInfo_byUserID(userID):
    select_OrgInfo_byUserID_query = "SELECT * FROM Org_Info WHERE `User_ID`='" + userID + "'"
    return select_OrgInfo_byUserID_query
    
def select_OrgInfo_byOrgID(orgID):
    select_OrgInfo_byOrgID_query = "SELECT * FROM Org_Info WHERE `Org_ID`='" + orgID + "'"
    return select_OrgInfo_byOrgID_query

def select_JDOrgInfo(orgID):
    select_JDOrgInfo_query = "SELECT * FROM JD_OrgInfo WHERE `Org_ID`='" + orgID + "'"
    return select_JDOrgInfo_query
   
def select_JDOrgInfo_byJDToken(jdToken):
    select_JDOrgInfo_byJDToken_QUERY = "SELECT * FROM JD_OrgInfo WHERE `JD_Subscription_Token`='" + jdToken + "'"
    return select_JDOrgInfo_byJDToken_QUERY

def select_Farms(orgID):
    select_Farms_query = "SELECT * FROM Farm_Info WHERE `Org_ID`='" + orgID + "'"
    return select_Farms_query   

def select_FarmInfo(farmID):
    select_FarmInfo_query = "SELECT * FROM Farm_Info WHERE `Farm_ID`='" + farmID + "'"
    return select_FarmInfo_query

def select_Fields(farmID):
    select_Fields_query = "SELECT * FROM Field_Info WHERE `Farm_ID`='" + farmID + "'"
    return select_Fields_query
    
def select_FieldInfo(fieldID):
    select_FieldInfo_query = "SELECT * FROM Field_Info WHERE `Field_ID`='" + fieldID + "'"
    return select_FieldInfo_query













def create_new_user(email, password, username):
    return f"INSERT INTO User_Info (email, password, username) VALUES ('{email}', '{password}', '{username}')"

def execute_query(connection, query):
    with connection.cursor() as cursor:
        cursor.execute(query)
        connection.commit()
