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
    #commented change
    try:
        connection = mysql.connector.connect(
            host = "132.148.180.201",
            user = "ssUser_Admin",
            password = "UNLSpraySafely1*",
            database = "ssUser_Info",
            time_zone = get_utc_offset_string()
        )

        if connection.is_connected():    
            #cursor = connection.cursor()
            #print(cursor)
            return connection
    except Error as e:
        print(e)


def get_utc_offset_string():
        import time

        utc_offset_seconds = time.localtime().tm_gmtoff
        
        minutes = int((utc_offset_seconds / 60) % 60)
        hours = int(((utc_offset_seconds / 60) - minutes) / 60)

        hours = str(hours).zfill(3)
        minutes = str(minutes).zfill(2)

        result_string = hours + ":" + minutes

        return result_string



#   ************************************************************
#   **** EXECUTE QUERY WITHIN MySQL DATABASE ****
#   * Description -  This procedure applies to any query within 
#                    this task file NOT requiring user information, 
#                    and applies to all spray-safely databases 
#                    designated within the query parameters.       
#   ************************************************************
def execute_create_query_vals(connection, sql_query, vals):
    from mysql.connector.errors import Error
    
    try:
        with connection.cursor(buffered=True) as cursor:
            cursor.execute(sql_query, vals)
            connection.commit()
            cursor.close()
    except Error as e:
        print(e)



#   ************************************************************
#   **** EXECUTE QUERY WITHIN MySQL DATABASE ****
#   * Description -  This procedure applies to any query within 
#                    this task file requiring user information, 
#                    and applies to all spray-safely databases 
#                    designated within the query parameters.       
#   ************************************************************
def execute_insert_update_delete_query(connection, sql_query, vals):
    from mysql.connector.errors import Error
    
    try:
        if connection:
            if vals:
                with connection.cursor() as cursor:
                    cursor.execute(sql_query, vals)
                    connection.commit()
                    last_row_id = cursor.lastrowid
                    cursor.close()
                    return last_row_id
            else:
                return "No information provided"
        else:
            return "Failed connection"
    except Error as e:
        print (e)
        


#   ************************************************************
#   **** EXECUTE QUERY WITHIN MySQL DATABASE ****
#   * Description -  This procedure applies to any query within 
#                    this task file requiring user information, 
#                    and applies to all spray-safely databases 
#                    designated within the query parameters.       
#   ************************************************************
def execute_select_query_vals(connection, sql_query, vals):
    from mysql.connector.errors import Error
    
    try:
        if connection:
            cursor = connection.cursor()  # ✅ FIX: Use `cursor()` without `with`
            cursor.execute(sql_query, vals)
            records = cursor.fetchall()
            cursor.close()
            return records if records else None  # ✅ Always return something
        else:
            return None
    except Error as e:
        print(f"Database query failed: {e}")
        return None




def execute_select_query(connection, sql_query):
    from mysql.connector.errors import Error
    
    try:
        if connection:
            with connection.cursor() as cursor:
                cursor.execute(sql_query)
                records = cursor.fetchall()
                cursor.close()
                return records
        else:
            return "Failed connection"
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
                                            Username text NOT NULL,
                                            Email text NOT NULL,
                                            Password text NOT NULL,
                                            Status text NOT NULL,
                                            PRIMARY KEY (User_ID)
                                         )"""
    return create_UserInfo_tbl_query
    
#   ************************************************************    
#   * Relational Tables *
#   ************************************************************
def create_UserOrgInfo_tbl():
    create_UserOrgInfo_tbl_query = """CREATE TABLE if not exists
                                        User_Org_Info(
                                            User_ID INT NOT NULL,
                                            Org_ID INT NOT NULL,
                                            FOREIGN KEY (User_ID)
                                                REFERENCES User_Info(User_ID),
                                            FOREIGN KEY (Org_ID)
                                                REFERENCES Org_Info(Org_ID)
                                        )"""
    return create_UserOrgInfo_tbl_query

def create_UserJDOrgInfo_tbl():
    create_UserJDOrgInfo_tbl_query = """CREATE TABLE if not exists
                                        User_JD_Org_Info(
                                            User_ID INT NOT NULL,
                                            JD_Org_ID INT NOT NULL,
                                            FOREIGN KEY (User_ID)
                                                REFERENCES User_Info(User_ID),
                                            FOREIGN KEY (JD_Org_ID)
                                                REFERENCES JD_Org_Info(JD_Org_ID)
                                        )"""
    return create_UserJDOrgInfo_tbl_query
 
def create_OrgInfo_tbl():
    create_OrgInfo_tbl_query = """CREATE TABLE if not exists
                                            Org_Info(
                                                Org_ID INT NOT NULL AUTO_INCREMENT,
                                                Org_Name text NOT NULL,
                                                Status text NOT NULL,
                                                PRIMARY KEY (Org_ID)
                                            )"""
    return create_OrgInfo_tbl_query

def create_JDOrgInfo_tbl():
    create_JDOrgInfo_tbl_query = """CREATE TABLE if not exists
                                            JD_Org_Info(
                                                JD_Org_ID INT NOT NULL AUTO_INCREMENT,
                                                JD_Org_Name text NOT NULL,
                                                JD_Subscription_Token text NOT NULL,
                                                JD_Subscription_Client_Key text NOT NULL,
                                                JD_Subscription_Name text NOT NULL,
                                                JD_Subscription_ID text NOT NULL,
                                                JD_Subscription_Filters text NOT NULL,
                                                JD_Org_Type text NOT NULL,
                                                JD_Username text NOT NULL,
                                                JD_Access_Level text NOT NULL,
                                                JD_Token_ID text NOT NULL,
                                                JD_Access_Token text NOT NULL,
                                                JD_Refresh_Token text NOT NULL,
                                                JD_Token_Expiration text NOT NULL,
                                                x_deere_signature text NOT NULL,
                                                JD_API_Org_ID INT NOT NULL
                                            )"""
    return create_JDOrgInfo_tbl_query

def create_FarmInfo_tbl():
    create_FarmInfo_tbl_query = """CREATE TABLE if not exists 
                                            Farm_Info(
                                                Farm_ID INT NOT NULL AUTO_INCREMENT,
                                                Farm_Name text NOT NULL,
                                                JD_Farm_ID text NOT NULL,
                                                Org_ID INT NOT NULL,
                                                JD_Org_ID INT NOT NULL,
                                                Status text NOT NULL,
                                                PRIMARY KEY (Farm_ID),
                                                FOREIGN KEY (Org_ID)
                                                    REFERENCES Org_Info(Org_ID),
                                                FOREIGN KEY (JD_Org_ID)
                                                    REFERENCES JD_Org_Info(JD_Org_ID)
                                            )"""
    return create_FarmInfo_tbl_query

def create_FieldInfo_tbl():
    create_FieldInfo_tbl_query = """CREATE TABLE if not exists 
                                            Field_Info(
                                                Field_ID INT NOT NULL AUTO_INCREMENT,
                                                Field_Name text NOT NULL,
                                                Farm_ID INT NOT NULL,
                                                JD_Field_ID text,
                                                Geometry longtext NOT NULL,
                                                PRIMARY KEY (Field_ID),
                                                FOREIGN KEY (Farm_ID)
                                                    REFERENCES Farm_Info(Farm_ID)
                                            )"""
    return create_FieldInfo_tbl_query

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
def insert_Applicator():
    insert_Applicator_post = """INSERT INTO 
                                Applicator_Info(
                                    First_Name,
                                    Last_Name,
                                    License_Type,
                                    License_Num,
                                    Licensed_Cat,
                                    License_Exp                                  
                                )
                                VALUES (%s,%s,%s,%s,%s,%s);"""
    return insert_Applicator_post


def insert_Applicator_Org_Info():
    insert_Applicator_Org_post = """INSERT INTO 
                                Applicator_Org_Info(
                                    Applicator_ID,
                                    Org_ID                                 
                                )
                                VALUES (%s,%s);"""
    return insert_Applicator_Org_post







# def insert_User():
#     insert_User_post = """INSERT INTO 
#                                 User_Info(
#                                     Username,
#                                     Email,
#                                     Password,
#                                     Status                                        
#                                 )
#                                 VALUES (%s,%s,%s,%s);"""
#     return insert_User_post
















    
def insert_UserOrg():
    insert_UserOrg_post = """INSERT INTO
                                User_Org_Info(
                                    User_ID,
                                    Org_ID
                                )
                                VALUES (%s,%s);"""
    return insert_UserOrg_post

def insert_UserJDOrg():
    insert_UserJDOrg_post = """INSERT INTO
                                User_Org_Info(
                                    User_ID,
                                    JD_Org_ID
                                )
                                VALUES (%s,%s);"""
    return insert_UserJDOrg_post

def insert_Org():
    insert_Org_post = """INSERT INTO
                                Org_Info(
                                    Org_Name,
                                    Status
                                )
                                VALUES (%s,%s);"""
    return insert_Org_post

def insert_JDOrg():
    insert_JDOrg_post = """INSERT INTO
                                JD_Org_Info(
                                    JD_Org_Name,
                                    JD_Subscription_Token,
                                    JD_Subscription_Client_Key,
                                    JD_Subscription_Name,
                                    JD_Subscription_ID,
                                    JD_Subscription_Filters,
                                    JD_Org_Type,
                                    JD_Username,
                                    JD_Access_Level,
                                    JD_Token_ID,
                                    JD_Access_Token,
                                    JD_Refresh_Token,
                                    JD_Token_Expiration,
                                    x_deere_signature,
                                    JD_API_Org_ID
                                )
                                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"""
    return insert_JDOrg_post


def insert_Farm():
    insert_Farm_post = """INSERT INTO
                                Farm_Info(
                                    Farm_Name,
                                    JD_Farm_ID,
                                    Org_ID,
                                    JD_Org_ID,
                                    Status
                                )
                                VALUES (%s,%s,%s,%s,%s);"""

    return insert_Farm_post

def insert_Field():
    insert_Field_post = """INSERT INTO
                                Field_Info(                                                               
                                    Field_Name,
                                    Farm_ID,
                                    JD_Field_ID,
                                    Geometry
                                )
                                VALUES (%s,%s,%s,%s);"""
    return insert_Field_post


def insert_Tank_Mix():
    insert_Tank_Mix_post = """INSERT INTO
                                Tank_Mix_Info(                                                               
                                    Tank_Mix_Name,
                                    User_ID                                
                                )
                                VALUES (%s,%s);"""
    return insert_Tank_Mix_post

def insert_Tank_Mix_Carrier():
    insert_Tank_Mix_Carrier_post = """INSERT INTO
                                    Tank_Mix_Carrier_Info(                                                               
                                    Tank_Mix_ID,
                                    Carrier_ID,
                                    Rate,
                                    Units                                
                                    )
                                    VALUES (%s,%s,%s,%s);"""
    return insert_Tank_Mix_Carrier_post

def insert_Tank_Mix_Product():
    insert_Tank_Mix_Product_post = """INSERT INTO
                                    Tank_Mix_Product_Info(                                                               
                                    Tank_Mix_ID,
                                    Product_ID,
                                    Rate,
                                    Units                                
                                    )
                                    VALUES (%s,%s,%s,%s);"""
    return insert_Tank_Mix_Product_post

def insert_Application():
    insert_Application_post = """INSERT INTO
                                    App_Info(                                                               
                                    Field_ID,
                                    Applicator_ID,
                                    Tank_Mix_ID,
                                    Start_Time,
                                    End_Time,
                                    REI_Exp,
                                    App_Type,
                                    Equipment_Name,
                                    Weather,
                                    JD_Application_ID,
                                    Geometry                         
                                    )
                                    VALUES (%s,%s,%s,CONVERT_TZ(%s, 'SYSTEM', '+00:00'),CONVERT_TZ(%s, 'SYSTEM', '+00:00'),%s,%s,%s,%s,%s,%s);"""
    return insert_Application_post

    
#   ************************************************************    
#   ** Update Table Information **
#   ************************************************************

# TODO: update the Update Table Info code to match the new database structure

# def update_JDAccess(accLvl,tokenID,accToken,refToken,tokenExp,orgID):
#     update_JDAccess_post = "UPDATE Org_Info SET `JD_Access_lvl`='" + accLvl + "',`JD_TokenID`='" + tokenID + "',`JD_AccessToken`='" + accToken\
#                             + "',`JD_RefreshToken`='" + refToken + "',`JD_TokenExpiration`='" + tokenExp + "' WHERE `Org_ID`='" + orgID + "'"
#     # call parameter Structure - query, values = (JD_Access_lvl, JD_TokenID, JD_AccessToken, JD_RefreshToken, JD_TokenExpiration, Org_ID)exit
#     return update_JDAccess_post

def update_JDAccess():
    update_JDAccess_post = """
                            UPDATE JD_Org_Info a
                            JOIN User_JD_Org_Info b ON a.JD_Org_ID = b.JD_Org_ID
                            JOIN User_Org_Info c ON b.User_ID = c.User_ID
                            SET a.`JD_Access_Level` = %s,
                                a.`JD_Token_ID` = %s,
                                a.`JD_Access_Token` = %s,
                                a.`JD_Refresh_Token` = %s,
                                a.`JD_Token_Expiration` = %s
                            WHERE c.`Org_ID` = %s;"""
#     # call parameter Structure - query, values = (JD_Access_lvl, JD_TokenID, JD_AccessToken, JD_RefreshToken, JD_TokenExpiration, Org_ID)exit
    return update_JDAccess_post


# def update_UserPassword_byID(password,userID):
#     update_UserPassword_byID_post = "UPDATE User_Info SET `Password`='" + password + "' WHERE `User_ID`='" + userID + "'"
#     return update_UserPassword_byID_post

def update_UserPassword_byID():
    update_UserPassword_byID_post = "UPDATE User_Info SET `Password`= %s WHERE `User_ID`= %s;"
    return update_UserPassword_byID_post

# def update_UserPassword_byUserName(password,userName):
#     update_UserPassword_byUserName_post = "UPDATE User_Info SET `Password`='" + password + "' WHERE `UserName`='" + userName + "'"
#     return update_UserPassword_byUserName_post


def update_UserPassword_byUserName():
    update_UserPassword_byUserName_post = "UPDATE User_Info SET `Password`= %s WHERE `UserName`= %s;"
    return update_UserPassword_byUserName_post

# def update_UserPassword_byEmail(password,email):
#     update_UserPassword_byEmail_post = "UPDATE User_Info SET `Password`='" + password + "' WHERE `Email`='" + email + "'"
#     return update_UserPassword_byEmail_post

def update_UserPassword_byEmail():
    update_UserPassword_byEmail_post = "UPDATE User_Info SET `Password`= %s WHERE `Email`= %s;"
    return update_UserPassword_byEmail_post

# def update_UserStatus(status,userID):
#     update_UserStatus_post = "UPDATE User_Info SET `Status`='" + status + "' WHERE `User_ID`='" + userID + "'"
#     return update_UserStatus_post

def update_UserStatus():
    update_UserStatus_post = "UPDATE User_Info SET `Status`= %s WHERE `User_ID`= %s;"
    return update_UserStatus_post

# def update_UserStatus(status,userID):
#     update_UserStatus_post = "UPDATE User_Info SET `Status`='" + status + "' WHERE `User_ID`='" + userID + "'"
#     return update_UserStatus_post

def update_OrgName():
    update_OrgName_post = "UPDATE Org_Info SET `Org_Name`= %s WHERE `Org_ID`= %s;"
    return update_OrgName_post

# def update_UserStatus(status,userID):
#     update_UserStatus_post = "UPDATE User_Info SET `Status`='" + status + "' WHERE `User_ID`='" + userID + "'"
#     return update_UserStatus_post

def update_JDOrgID():
    update_JDOrgID_post = "UPDATE JD_Org_Info SET `JD_Org_ID`= %s WHERE `JD_Org_ID`= %s;"
    return update_JDOrgID_post

def update_jd_api_org_ID():
    update_jd_api_org_ID_post = "UPDATE JD_Org_Info SET `JD_API_Org_ID`= %s WHERE `JD_API_Org_ID`= %s;"
    return update_jd_api_org_ID_post

# def update_UserStatus(status,userID):
#     update_UserStatus_post = "UPDATE User_Info SET `Status`='" + status + "' WHERE `User_ID`='" + userID + "'"
#     return update_UserStatus_post

def update_JDOrgName():
    update_JDOrgName_post = "UPDATE JD_Org_Info SET `JD_Org_Name`= %s WHERE `JD_Org_ID`= %s;"
    return update_JDOrgName_post
    
# def update_JDOrgType(jdOrgType,orgID,jdOrgID):
#     update_JDOrgType_post = "UPDATE JD_OrgInfo SET `JD_OrgType`='" + jdOrgType + "' WHERE `Org_ID`='" + orgID + "' AND `JD_OrgID`='" + jdOrgID + "'"
#     return update_JDOrgType_post
    
def update_JDOrgType():
    update_JDOrgType_post = """UPDATE JD_Org_Info a
                            JOIN User_JD_Org_Info b ON a.JD_Org_ID = b.JD_Org_ID
                            JOIN User_Org_Info c ON b.User_ID = c.User_ID
                            SET a.JD_Org_Type = %s
                            WHERE c.Org_ID = %s AND a.JD_API_Org_ID = %s;"""
    return update_JDOrgType_post
    
# def update_JDSubToken(orgID, jdOrgID, token):
#     update_JDSubToken_post = "UPDATE JD_OrgInfo SET `JD_Subscription_Token`='" + token + "' WHERE `Org_ID`='" + orgID + "' AND `JD_OrgID`='" + jdOrgID + "'"
#     return update_JDSubToken_post

#   write jd subscription info update
def update_JDSubToken():
    update_JDSubToken_post = """UPDATE JD_Org_Info a
                            JOIN User_JD_Org_Info b ON a.JD_Org_ID = b.JD_Org_ID
                            JOIN User_Org_Info c ON b.User_ID = c.User_ID
                            SET a.JD_Subscription_Token = %s
                            WHERE c.Org_ID = %s AND a.JD_API_Org_ID = %s;"""
    return update_JDSubToken_post

# def update_JDSubClientKey(orgID, jdOrgID, clientKey):
#     update_JDSubClientKey_post = "UPDATE JD_OrgInfo SET `JD_Subscription_ClientKey`='" + clientKey + "' WHERE `Org_ID`='" + orgID + "' AND `JD_OrgID`='" + jdOrgID + "'"
#     return update_JDSubClientKey_post

def update_JDSubClientKey():
    update_JDSubClientKey_post = """UPDATE JD_Org_Info a
                            JOIN User_JD_Org_Info b ON a.JD_Org_ID = b.JD_Org_ID
                            JOIN User_Org_Info c ON b.User_ID = c.User_ID
                            SET a.JD_Subscription_Client_Key = %s
                            WHERE c.Org_ID = %s AND a.JD_API_Org_ID = %s;"""
    return update_JDSubClientKey_post

# def update_JDSubName(orgID, jdOrgID, displayName):
#     update_JDSubName_post = "UPDATE JD_OrgInfo SET `JD_Subscription_Name`='" + displayName + "' WHERE `Org_ID`='" + orgID + "' AND `JD_OrgID`='" + jdOrgID + "'"
#     return update_JDSubName_post

def update_JDSubName():
    update_JDSubName_post = """UPDATE JD_Org_Info a
                            JOIN User_JD_Org_Info b ON a.JD_Org_ID = b.JD_Org_ID
                            JOIN User_Org_Info c ON b.User_ID = c.User_ID
                            SET a.JD_Subscription_Name = %s
                            WHERE c.Org_ID = %s AND a.JD_API_Org_ID = %s;"""
    return update_JDSubName_post
    
# def update_JDSubID(orgID, jdOrgID, subID):
#     update_JDSubID_post = "UPDATE JD_OrgInfo SET `JD_Subscription_ID`='" + subID + "' WHERE `Org_ID`='" + orgID + "' AND `JD_OrgID`='" + jdOrgID + "'"
#     return update_JDSubID_post

def update_JDSubID():
    update_JDSubID_post = """UPDATE JD_Org_Info a
                            JOIN User_JD_Org_Info b ON a.JD_Org_ID = b.JD_Org_ID
                            JOIN User_Org_Info c ON b.User_ID = c.User_ID
                            SET a.JD_Subscription_ID = %s
                            WHERE c.Org_ID = %s AND a.JD_API_Org_ID = %s;"""
    return update_JDSubID_post
    
# def update_JDSubFilters(orgID, jdOrgID, subFilters):
#     update_JDSubFilters_post = "UPDATE JD_OrgInfo SET `JD_Subscription_Filters`=" + subFilters + " WHERE `Org_ID`='" + orgID + "' AND `JD_OrgID`='" + jdOrgID + "'"
#     return update_JDSubFilters_post

def update_JDSubFilters():
    update_JDSubFilters_post = """UPDATE JD_Org_Info a
                            JOIN User_JD_Org_Info b ON a.JD_Org_ID = b.JD_Org_ID
                            JOIN User_Org_Info c ON b.User_ID = c.User_ID
                            SET a.JD_Subscription_Filters = %s
                            WHERE c.Org_ID = %s AND a.JD_API_Org_ID = %s;"""
    return update_JDSubFilters_post
    
# def update_FarmName(farmName,farmID):
#     update_FarmName_post = "UPDATE Farm_Info SET `Farm_Name`='" + farmName + "' WHERE `Farm_ID`='" + farmID + "'"
#     return update_FarmName_post

def update_FarmName():
    update_FarmName_post = "UPDATE Farm_Info SET `Farm_Name`= %s WHERE `Farm_ID`= %s;"
    return update_FarmName_post

# def update_FieldName(fieldName, fieldID):
#     update_FieldName_post = "UPDATE Field_Info SET `Field_Name`='" + fieldName + "' WHERE `Field_ID`='" + fieldID + "'"
#     return update_FieldName_post

def update_FieldName():
    update_FieldName_post = "UPDATE Field_Info SET `Field_Name`= %s WHERE `Field_ID`= %s;"
    return update_FieldName_post

def update_IsConfirmed_query():
    update_IsConfirmed_post = "UPDATE User_Info SET Is_Confirmed = %s WHERE User_ID = %s;"
    return update_IsConfirmed_post
   
#   ************************************************************
#   ** Delete Table Information **
#   ************************************************************

# TODO: update the Delete Table Info code to match the new database structure

def delete_User():
    delete_User_post = "DELETE FROM User_Info WHERE `User_ID`= %s;"
    return delete_User_post

def delete_Org():
    delete_Org_post = "DELETE FROM Org_Info WHERE `Org_ID`= %s"
    return delete_Org_post
    
def delete_JDOrg():
    delete_JDOrg_post = "DELETE FROM JD_Org_Info WHERE `JD_Org_ID`= %s;"
    return delete_JDOrg_post
    
def delete_Farm():
    delete_Farm_post = "DELETE FROM Farm_Info WHERE `Farm_ID`= %s"
    return delete_Farm_post 
    
def delete_Field():
    delete_Field_post = "DELETE FROM Field_Info WHERE `Field_ID`= %s"
    return delete_Field_post
    
    
#   ************************************************************
#   ** Query Table Information **
#   ************************************************************
def check_password_by_password_and_user_id_query():
    check_password_query = "SELECT CASE WHEN Password = %s THEN 1 ELSE 0 END AS Equals FROM `User_Info` WHERE User_ID = %s;"
    return check_password_query

def select_organization_owner_by_userID_query():
    select_organization_owner_query = "SELECT SQL_NO_CACHE Organization_Owner FROM User_Info WHERE User_ID = %s;"
    return select_organization_owner_query

def select_is_confirmed_by_userID_query():
    select_is_confirmed_query = "SELECT SQL_NO_CACHE Is_Confirmed FROM User_Info WHERE User_ID = %s;"
    return select_is_confirmed_query

def select_jd_org_name_by_orgID_and_JD_API_org_ID_query():
    select_jd_org_name_by_orgID_and_JD_API_org_ID_query ="""
                            SELECT SQL_NO_CACHE a.JD_Org_Name FROM JD_Org_Info AS a 
                            JOIN User_JD_Org_Info AS b 
                            ON a.JD_Org_ID = b.JD_Org_ID
                            JOIN User_Org_Info AS c
                            ON b.User_ID = c.User_ID
                            WHERE c.Org_ID = %s AND a.JD_API_Org_ID = %s;
                        """
    return select_jd_org_name_by_orgID_and_JD_API_org_ID_query

def select_jd_org_ID_by_orgID_and_JD_API_org_ID_query():
    select_jd_org_ID_by_orgID_and_JD_API_org_ID_query ="""
                            SELECT SQL_NO_CACHE a.JD_Org_ID FROM JD_Org_Info AS a 
                            JOIN User_JD_Org_Info AS b 
                            ON a.JD_Org_ID = b.JD_Org_ID
                            JOIN User_Org_Info AS c
                            ON b.User_ID = c.User_ID
                            WHERE c.Org_ID = %s AND a.JD_API_Org_ID = %s;
                        """
    return select_jd_org_ID_by_orgID_and_JD_API_org_ID_query

def select_jd_org_ID_by_orgID_query():
    select_jd_org_ID_by_orgID_query ="""
                            SELECT SQL_NO_CACHE JD_Org_ID FROM JD_Org_Info WHERE Org_ID = %s;
                        """
    return select_jd_org_ID_by_orgID_query

def select_userID_by_password_and_email_query():
    return "SELECT User_ID FROM User_Info WHERE Email = %s AND Password = %s;"

def select_hashed_password_query():
    return "SELECT User_ID, Password FROM User_Info WHERE Email = %s;"

def select_userID_by_username_query():
    select_UserID_query = "SELECT SQL_NO_CACHE User_ID FROM User_Info WHERE `Username`= %s;" 
    return select_UserID_query

def select_username_and_access_level_by_userID_query():
    select_UserName_and_Edit_Access_query = "SELECT SQL_NO_CACHE Username, Has_Edit_Access FROM User_Info WHERE `User_ID`= %s;"
    return select_UserName_and_Edit_Access_query

def select_userID_by_orgID_query():
    select_userID_by_OrgID_query = "SELECT SQL_NO_CACHE Org_ID FROM User_Org_Info;"
    return select_userID_by_OrgID_query

def select_orgIDs_by_userID_query():
    select_orgIDs_by_userID_query ="""
                            SELECT SQL_NO_CACHE b.Org_ID FROM User_Info AS a 
                            JOIN User_Org_Info AS b 
                                ON a.User_ID = b.User_ID
                            WHERE a.User_ID = %s;
                        """
    return select_orgIDs_by_userID_query

def select_OrgID_by_JD_Sub_Token_query():
    select_OrgID_by_JD_Sub_Token_query = "SELECT SQL_NO_CACHE Org_ID FROM JD_Org_Info where JD_Subscription_Token = %s;"
    
    return select_OrgID_by_JD_Sub_Token_query

def select_orgID_by_username_and_org_name_query():
    select_UserName_query = """
                            SELECT SQL_NO_CACHE c.Org_ID 
                            FROM User_Info AS a 
                            JOIN User_Org_Info AS b 
                                ON a.User_ID = b.User_ID
                            JOIN Org_Info AS c
                                ON b.Org_ID = c.Org_ID
                            WHERE a.Username = %s AND c.Org_Name = %s;
                            """
    return select_UserName_query

def select_jd_api_orgID_by_orgID_query():
    select_jd_api_orgID_by_orgID_query = """SELECT SQL_NO_CACHE c.JD_API_Org_ID 
                            FROM User_JD_Org_Info AS a 
                            JOIN User_Org_Info AS b 
                                ON a.User_ID = b.User_ID
                            JOIN JD_Org_Info AS c
                                ON a.JD_Org_ID = c.JD_Org_ID
                            WHERE b.Org_ID = %s;"""
    return select_jd_api_orgID_by_orgID_query

# Note: this means farm names must be unique for each user across all organizations
def select_farmID_by_username_and_farm_name_query():
    select_UserName_query = """
                                SELECT SQL_NO_CACHE f.Farm_ID
                                FROM User_Info AS a
                                LEFT JOIN User_Org_Info AS b
                                    ON a.User_ID = b.User_ID
                                LEFT JOIN Org_Info AS c
                                    ON b.Org_ID = c.Org_ID
                                LEFT JOIN User_JD_Org_Info AS d
                                    ON a.User_ID  = d.User_ID 
                                LEFT JOIN JD_Org_Info AS e
                                    ON d.JD_Org_ID = e.JD_Org_ID
                                JOIN Farm_Info AS f
                                    ON (f.Org_ID = c.Org_ID)
                                        OR (f.JD_Org_ID = e.JD_Org_ID)
                                WHERE a.Username = %s AND f.Farm_Name = %s;
                            """
    return select_UserName_query


def select_fieldID_by_username_and_farm_name_and_field_name_query():
    select_UserName_query = """
                                SELECT SQL_NO_CACHE g.Field_ID
                                FROM User_Info AS a
                                LEFT JOIN User_Org_Info AS b
                                    ON a.User_ID = b.User_ID
                                LEFT JOIN Org_Info AS c
                                    ON b.Org_ID = c.Org_ID
                                LEFT JOIN User_JD_Org_Info AS d
                                    ON a.User_ID  = d.User_ID 
                                LEFT JOIN JD_Org_Info AS e
                                    ON d.JD_Org_ID = e.JD_Org_ID
                                LEFT JOIN Farm_Info AS f
                                    ON (f.Org_ID = c.Org_ID)
                                        OR (f.JD_Org_ID = e.JD_Org_ID)
                                JOIN Field_Info AS g
                                    ON f.Farm_ID = g.Farm_ID
                                WHERE a.Username = %s AND f.Farm_Name = %s AND g.Field_Name = %s;
                            """
    return select_UserName_query



def select_app_info_by_orgID_query():
    select_apps_query ="""
                            SELECT SQL_NO_CACHE b.Farm_Name, c.Field_Name, d.Application_ID, d.App_Type, d.Start_Time, d.End_Time, d.REI_Exp, d.Weather, d.Equipment_Name, d.Tank_Mix_ID
                            FROM Org_Info AS a 
                            JOIN Farm_Info AS b 
                                ON a.Org_ID = b.Org_ID
                            JOIN Field_Info AS c
                                ON b.Farm_ID = c.Farm_ID
                            JOIN App_Info as d
                                ON c.Field_ID = d.Field_ID
                            WHERE a.Org_ID = %s;
                        """
    return select_apps_query

def select_app_geometry_by_appID_query():
    select_apps_query ="""
                            SELECT SQL_NO_CACHE Geometry
                            FROM App_Info
                            WHERE Application_ID = %s;
                        """
    return select_apps_query



def select_tank_mix_name_by_tank_mixID_query():
    select_tank_mix_name_query = """
                                SELECT SQL_NO_CACHE Tank_Mix_Name
                                FROM Tank_Mix_Info
                                WHERE Tank_Mix_ID = %s;
                            """
    return select_tank_mix_name_query



def select_tank_mix_products_by_tank_mixID_query():
    select_tank_mix_query = """
                                SELECT SQL_NO_CACHE c.Product_Name, b.Rate, b.Units
                                FROM Tank_Mix_Info AS a
                                JOIN Tank_Mix_Product_Info AS b
                                    ON a.Tank_Mix_ID = b.Tank_Mix_ID
                                JOIN Product_Info AS c
                                    ON b.Product_ID = c.Product_ID
                                WHERE a.Tank_Mix_ID = %s;
                            """
    return select_tank_mix_query


def select_tank_mix_carrier_by_tank_mixID_query():
    select_tank_mix_query = """
                                SELECT SQL_NO_CACHE c.Carrier_Name, b.Rate, b.Units
                                FROM Tank_Mix_Info AS a
                                JOIN Tank_Mix_Carrier_Info AS b
                                    ON a.Tank_Mix_ID = b.Tank_Mix_ID
                                JOIN Carrier_Info AS c
                                    ON b.Carrier_ID = c.Carrier_ID
                                WHERE a.Tank_Mix_ID = %s;
                            """
    return select_tank_mix_query


def select_applicatorID_by_firstName_and_lastName_and_orgID_query():
    select_applicatorID_query = """
                                SELECT SQL_NO_CACHE a.Applicator_ID
                                FROM Applicator_Info AS a
                                JOIN Applicator_Org_Info AS b
                                    ON a.Applicator_ID = b.Applicator_ID
                                JOIN Org_Info AS c
                                    ON b.Org_ID = c.Org_ID
                                WHERE a.First_Name = %s AND a.Last_Name = %s AND c.Org_ID = %s;
                            """
    return select_applicatorID_query



# QUERIES FOR ADD TANK MIX PROCESS
def select_all_carrier_names_query():
    select_carrier_names_query = """
                                SELECT SQL_NO_CACHE Carrier_Name
                                FROM Carrier_Info;
                            """
    return select_carrier_names_query

def select_all_product_names_query():
    select_all_product_names_query = """
                                SELECT SQL_NO_CACHE Product_Name
                                FROM Product_Info;
                            """
    return select_all_product_names_query

def select_tankMixID_by_tankMix_name_and_username_query():
    select_tank_mixID_query = """
                                SELECT SQL_NO_CACHE b.Tank_Mix_ID
                                FROM User_Info a
                                JOIN Tank_Mix_Info b
                                    ON a.User_ID = b.User_ID
                                WHERE b.Tank_Mix_Name = %s AND a.Username = %s;
                            """
    return select_tank_mixID_query


def select_productID_by_product_name_query():
    select_productID_query =  """
                                SELECT SQL_NO_CACHE Product_ID
                                FROM Product_Info 
                                WHERE Product_Name = %s;
                            """
    return select_productID_query


def select_carrierID_by_carrier_name_query():
    select_carrierID_query =  """
                                SELECT SQL_NO_CACHE Carrier_ID
                                FROM Carrier_Info 
                                WHERE Carrier_Name = %s;
                            """
    return select_carrierID_query



# QUERIES FOR ADD APPLICATION PROCESS
def select_field_geometry_by_fieldID_query():
    select_geometry_query =  """
                                SELECT SQL_NO_CACHE Geometry
                                FROM Field_Info 
                                WHERE Field_ID = %s;
                            """
    return select_geometry_query







def select_farmIDs_by_orgID_query():
    select_FarmID_query = "SELECT SQL_NO_CACHE Farm_ID FROM Farm_Info WHERE `Org_ID`= %s;"
    return select_FarmID_query


def select_farm_name_by_farmID_query():
    select_FarmName_query = "SELECT SQL_NO_CACHE Farm_Name FROM Farm_Info WHERE `Farm_ID`= %s;"
    return select_FarmName_query
    
def select_fieldIDs_by_farm_ID_query():
    select_FieldID_query = "SELECT SQL_NO_CACHE Field_ID FROM Field_Info WHERE `Farm_ID`= %s;"
    return select_FieldID_query

def select_field_name_by_fieldID_query():
    select_FieldName_query = "SELECT SQL_NO_CACHE Field_Name FROM Field_Info WHERE `Field_ID`= %s;"
    return select_FieldName_query

# QUERIES FOR EDIT APPLICATION PROCESS



def select_application_details_by_appID_query():
    select_AppDetails_query = """
                                SELECT SQL_NO_CACHE c.Farm_Name, b.Field_Name, CONCAT(e.Last_Name, ', ', e.First_Name, ' - ', g.Org_Name) AS Applicator, 
                                    CONVERT_TZ(a.End_Time, '+00:00', 'SYSTEM') AS End_DateTime, d.Tank_Mix_Name, a.App_Type, a.Equipment_Name
                                FROM App_Info AS a

                                JOIN Field_Info AS b
                                    ON a.Field_ID = b.Field_ID
                                JOIN Farm_Info AS c
                                    ON b.Farm_ID = c.Farm_ID


                                JOIN Tank_Mix_Info AS d
                                    ON a.Tank_Mix_ID = d.Tank_Mix_ID

                                
                                JOIN Applicator_Info AS e
                                    ON a.Applicator_ID = e.Applicator_ID
                                JOIN Applicator_Org_Info AS f
                                    ON e.Applicator_ID = f.Applicator_ID
                                JOIN Org_Info AS g
                                    ON f.Org_ID = g.Org_ID

                                WHERE a.Application_ID = %s;
                            """
    return select_AppDetails_query


def update_application_by_appID_query():
    update_application_query = """
                                UPDATE App_Info
                                SET Field_ID = %s,
                                    Applicator_ID = %s,
                                    Tank_Mix_ID = %s,
                                    Start_Time = CONVERT_TZ(%s, 'SYSTEM', '+00:00'),
                                    End_Time = CONVERT_TZ(%s, 'SYSTEM', '+00:00'),
                                    REI_Exp = %s,
                                    App_Type = %s,
                                    Equipment_Name = %s,
                                    Weather = %s,
                                    JD_Application_ID = %s,
                                    Geometry = %s           
                                WHERE Application_ID = %s;
                            """
    return update_application_query


def delete_application_by_appID_query():
    delete_application_query = """
                                DELETE FROM App_Info
                                WHERE Application_ID = %s;
                            """
    return delete_application_query











#   ************************************************************
#   ** Query All Records in a Table **
#   ************************************************************

def select_all_farm_names_by_username_query():
    select_farm_names_query = """
                                SELECT SQL_NO_CACHE f.Farm_Name
                                FROM User_Info AS a
                                LEFT JOIN User_Org_Info AS b
                                    ON a.User_ID = b.User_ID
                                LEFT JOIN Org_Info AS c
                                    ON b.Org_ID = c.Org_ID
                                LEFT JOIN User_JD_Org_Info AS d
                                    ON a.User_ID  = d.User_ID 
                                LEFT JOIN JD_Org_Info AS e
                                    ON d.JD_Org_ID = e.JD_Org_ID
                                JOIN Farm_Info AS f
                                    ON (f.Org_ID = c.Org_ID)
                                        OR (f.JD_Org_ID = e.JD_Org_ID)
                                WHERE a.Username = %s;
                            """
    return select_farm_names_query

def select_all_field_names_by_farm_name_and_username_query():
    select_field_names_query = """
                                SELECT SQL_NO_CACHE g.Field_Name
                                FROM User_Info AS a
                                LEFT JOIN User_Org_Info AS b
                                    ON a.User_ID = b.User_ID
                                LEFT JOIN Org_Info AS c
                                    ON b.Org_ID = c.Org_ID
                                LEFT JOIN User_JD_Org_Info AS d
                                    ON a.User_ID  = d.User_ID 
                                LEFT JOIN JD_Org_Info AS e
                                    ON d.JD_Org_ID = e.JD_Org_ID
                                JOIN Farm_Info AS f
                                    ON (f.Org_ID = c.Org_ID)
                                        OR (f.JD_Org_ID = e.JD_Org_ID)
                                JOIN Field_Info AS g
                                    ON f.Farm_ID = g.Farm_ID
                                WHERE a.Username = %s AND f.Farm_Name = %s;
                            """
    
    # """
    #                             SELECT Field_Name
    #                             FROM Farm_Info AS a
    #                             JOIN Field_Info AS b
    #                                 ON a.Farm_ID = b.Farm_ID
    #                             WHERE a.Farm_Name = %s;
    #                         """
    return select_field_names_query




def select_all_applicator_names_by_username_query():
    select_all_applicator_names_query = """
                                            SELECT SQL_NO_CACHE CONCAT(h.Last_Name, ', ', h.First_Name, ' - ', c.Org_Name)
                                            FROM User_Info AS a
                                            LEFT JOIN User_Org_Info AS b
                                                ON a.User_ID = b.User_ID
                                            LEFT JOIN Org_Info AS c
                                                ON b.Org_ID = c.Org_ID
                                            LEFT JOIN User_JD_Org_Info AS d
                                                ON a.User_ID  = d.User_ID 
                                            LEFT JOIN JD_Org_Info AS e
                                                ON d.JD_Org_ID = e.JD_Org_ID
                                            LEFT JOIN Applicator_Org_Info AS f
                                                ON f.Org_ID = c.Org_ID
                                            LEFT JOIN Applicator_JD_Org_Info AS g
                                                ON g.JD_Org_ID = e.JD_Org_ID
                                            JOIN Applicator_Info AS h
                                                ON (h.Applicator_ID = f.Applicator_ID)
                                                    OR (h.Applicator_ID = g.Applicator_ID)
                                            WHERE a.Username = %s;
                                        """
    return select_all_applicator_names_query







def select_all_org_names_by_username_query():
    select_org_names_query = """
                                SELECT SQL_NO_CACHE c.Org_Name
                                FROM User_Info AS a
                                JOIN User_Org_Info AS b
                                    ON a.User_ID = b.User_ID
                                JOIN Org_Info AS c
                                    ON b.Org_ID = c.Org_ID
                                WHERE a.Username = %s;
                            """
    return select_org_names_query

def select_all_tank_mix_names_by_username_query():
    select_tank_mix_names_query = """
                                SELECT SQL_NO_CACHE b.Tank_Mix_Name
                                FROM User_Info AS a
                                JOIN Tank_Mix_Info AS b
                                    ON a.User_ID = b.User_ID
                                WHERE a.Username = %s;
                            """
    return select_tank_mix_names_query

#3/2/2023
def select_product_name_and_tank_mix_query():
    select_product_name_and_tank_mix_query = """
                               SELECT SQL_NO_CACHE tp.Product_ID, p.Product_Name, MAX(p.REI_Time_Hours) as MaxREITime
                                FROM Tank_Mix_Info as ti
                                JOIN Tank_Mix_Product_Info as tp ON ti.Tank_Mix_ID = tp.Tank_Mix_ID
                                JOIN Product_Info as p ON tp.Product_ID = p.Product_ID
                                WHERE ti.Tank_Mix_Name = 'Test_Tank_Mix_1'
                                GROUP BY tp.Product_ID, p.Product_Name
                                ORDER BY MaxREITime DESC
                                LIMIT 1;
                            """
    return select_product_name_and_tank_mix_query

def select_REI_time_from_application_query():
    select_REI_time_from_application = """
                                SELECT SQL_NO_CACHE p.REI_Time_Hours as MaxREITime
                                FROM App_Info AS a 
                                JOIN Tank_Mix_Info AS ti ON a.Tank_Mix_ID = ti.Tank_Mix_ID 
                                JOIN Tank_Mix_Product_Info AS tp ON ti.Tank_Mix_ID = tp.Tank_Mix_ID 
                                JOIN Product_Info AS p ON tp.Product_ID = p.Product_ID 
                                WHERE a.Application_ID = %s
                                GROUP BY tp.Product_ID, p.Product_Name, p.REI_Description 
                                ORDER BY MaxREITime DESC 
                                LIMIT 1
                            """
    return select_REI_time_from_application
#TODO: Select REI time by tank mix name/ID? Select irregular entries/descriptions by tank mix name/ID?








def select_past_applications_by_orgID_query():
    select_past_applications_by_orgID_query = """
                                SELECT SQL_NO_CACHE b.Farm_Name, c.Field_Name, d.Application_ID, d.App_Type, CONVERT_TZ(d.Start_Time, '+00:00', 'SYSTEM') AS Converted_Start, CONVERT_TZ(d.End_Time, '+00:00', 'SYSTEM') AS Converted_End, d.REI_Exp, d.Weather, d.Equipment_Name, d.Tank_Mix_ID, 'Past' AS App_Time_Type
                                FROM Org_Info AS a 
                                JOIN Farm_Info AS b 
                                    ON a.Org_ID = b.Org_ID
                                JOIN Field_Info AS c
                                    ON b.Farm_ID = c.Farm_ID
                                JOIN App_Info as d
                                    ON c.Field_ID = d.Field_ID
                                JOIN Tank_Mix_Info AS ti 
                                    ON d.Tank_Mix_ID = ti.Tank_Mix_ID 
                                JOIN Tank_Mix_Product_Info AS tp 
                                    ON ti.Tank_Mix_ID = tp.Tank_Mix_ID 
                                JOIN Product_Info AS p 
                                    ON tp.Product_ID = p.Product_ID 

                                WHERE a.Org_ID = %s

                                GROUP BY d.Application_ID

                                HAVING NOW()
                                    BETWEEN 
                                        TIMESTAMPADD(hour, GREATEST(0, MAX(p.REI_Time_Hours)), Converted_End)
                                        AND
                                        TIMESTAMPADD(hour, GREATEST(0, MAX(p.REI_Time_Hours)) + 24, Converted_End);
                            """
    return select_past_applications_by_orgID_query


def select_current_applications_by_orgID_query():
    select_current_applications_by_orgID_query = """
                                SELECT SQL_NO_CACHE b.Farm_Name, c.Field_Name, d.Application_ID, d.App_Type, CONVERT_TZ(d.Start_Time, '+00:00', 'SYSTEM') AS Converted_Start, CONVERT_TZ(d.End_Time, '+00:00', 'SYSTEM') AS Converted_End, d.REI_Exp, d.Weather, d.Equipment_Name, d.Tank_Mix_ID, 'Current' AS App_Time_Type
                                FROM Org_Info AS a 
                                JOIN Farm_Info AS b 
                                    ON a.Org_ID = b.Org_ID
                                JOIN Field_Info AS c
                                    ON b.Farm_ID = c.Farm_ID
                                JOIN App_Info as d
                                    ON c.Field_ID = d.Field_ID
                                JOIN Tank_Mix_Info AS ti 
                                    ON d.Tank_Mix_ID = ti.Tank_Mix_ID 
                                JOIN Tank_Mix_Product_Info AS tp 
                                    ON ti.Tank_Mix_ID = tp.Tank_Mix_ID 
                                JOIN Product_Info AS p 
                                    ON tp.Product_ID = p.Product_ID 

                                WHERE a.Org_ID = %s

                                GROUP BY d.Application_ID

                                HAVING NOW()
                                    BETWEEN 
                                        Converted_End
                                        AND
                                        TIMESTAMPADD(hour, GREATEST(0, MAX(p.REI_Time_Hours)), Converted_End);
                            """
    return select_current_applications_by_orgID_query


def select_future_applications_by_orgID_query():
    select_future_applications_by_orgID_query = """
                                SELECT SQL_NO_CACHE b.Farm_Name, c.Field_Name, d.Application_ID, d.App_Type, CONVERT_TZ(d.Start_Time, '+00:00', 'SYSTEM') AS Converted_Start, CONVERT_TZ(d.End_Time, '+00:00', 'SYSTEM') AS Converted_End, d.REI_Exp, d.Weather, d.Equipment_Name, d.Tank_Mix_ID, 'Future' AS App_Time_Type
                                FROM Org_Info AS a 
                                JOIN Farm_Info AS b 
                                    ON a.Org_ID = b.Org_ID
                                JOIN Field_Info AS c
                                    ON b.Farm_ID = c.Farm_ID
                                JOIN App_Info as d
                                    ON c.Field_ID = d.Field_ID
                                JOIN Tank_Mix_Info AS ti 
                                    ON d.Tank_Mix_ID = ti.Tank_Mix_ID 
                                JOIN Tank_Mix_Product_Info AS tp 
                                    ON ti.Tank_Mix_ID = tp.Tank_Mix_ID 
                                JOIN Product_Info AS p 
                                    ON tp.Product_ID = p.Product_ID 

                                WHERE a.Org_ID = %s

                                GROUP BY d.Application_ID

                                HAVING NOW()
                                    BETWEEN 
                                        TIMESTAMPADD(hour, -24, Converted_End)
                                        AND
                                        Converted_End;
                            """
    return select_future_applications_by_orgID_query








# TODO: go through the following commented out lines and update the queries to match the new database structure
#       * JD Information
# def select_JDAccessToken(orgID):
#     select_JDAccessToken_query = "SELECT JD_AccessToken FROM Org_Info WHERE `Org_ID`='" + orgID + "'"
#     return select_JDAccessToken_query

#      * JD Information
def select_JD_Org_Name_by_JD_Org_ID():
    select_JD_Org_Name_by_JD_Org_ID_query = "SELECT SQL_NO_CACHE JD_Org_Name FROM JD_Org_Info WHERE 'JD_Org_ID'= %s;"

def select_JD_org_ID_by_User_ID_from_User_JD_Org_Info_query():
    select_JD_org_ID_from_User_JD_Org_Info_query = "SELECT SQL_NO_CACHE JD_Org_ID FROM User_JD_Org_Info WHERE `User_ID`= %s;"
    return select_JD_org_ID_from_User_JD_Org_Info_query

def select_JD_org_name_by_JD_org_ID_query():
    select_JD_org_name_by_JD_org_ID_query = "SELECT SQL_NO_CACHE JD_Org_Name FROM JD_Org_Info WHERE `JD_Org_ID`= %s;"
    return select_JD_org_name_by_JD_org_ID_query

def select_JD_subscription_token_by_JD_org_ID_query():
    select_JD_subscription_token_by_JD_org_ID_query = "SELECT SQL_NO_CACHE JD_Subscription_Token FROM JD_Org_Info WHERE `JD_Org_ID`= %s;"
    return select_JD_subscription_token_by_JD_org_ID_query
    
def select_JD_subscription_client_key_by_JD_org_ID_query():
    select_JD_subscription_client_key_by_JD_org_ID_query = "SELECT SQL_NO_CACHE JD_Subscription_Client_Key FROM JD_Org_Info WHERE `JD_Org_ID`= %s;"
    return select_JD_subscription_client_key_by_JD_org_ID_query
    
def select_JD_subscription_name_by_JD_org_ID_query():
    select_JD_subscription_name_by_JD_org_ID_query = "SELECT SQL_NO_CACHE JD_Subscription_Name FROM JD_Org_Info WHERE `JD_Org_ID`= %s;"
    return select_JD_subscription_name_by_JD_org_ID_query

def select_JD_subscription_name_by_JD_API_org_ID_query():
    select_JD_subscription_name_by_JD_API_org_ID_query = """
                            SELECT SQL_NO_CACHE a.JD_Subscription_Name FROM JD_Org_Info AS a 
                            JOIN User_JD_Org_Info AS b 
                            ON a.JD_Org_ID = b.JD_Org_ID
                            JOIN User_Org_Info AS c
                            ON b.User_ID = c.User_ID
                            WHERE c.Org_ID = %s AND a.JD_API_Org_ID = %s;"""
    return select_JD_subscription_name_by_JD_API_org_ID_query

def select_JD_subscription_ID_by_JD_org_ID_query():
    select_JD_subscription_ID_by_JD_org_ID_query = "SELECT SQL_NO_CACHE JD_Subscription_ID FROM JD_Org_Info WHERE `JD_Org_ID`= %s;"
    return select_JD_subscription_ID_by_JD_org_ID_query

def select_JD_subscription_ID_by_Org_ID_and_JD_API_org_ID_query():
    select_JD_subscription_ID_by_Org_ID_and_JD_API_org_ID_query = """
                                                    SELECT SQL_NO_CACHE JD_Subscription_ID FROM JD_Org_Info AS a
                                                    JOIN User_JD_Org_Info as b
                                                    ON a.JD_Org_ID = b.JD_Org_ID
                                                    JOIN User_Org_Info as c
                                                    ON b.User_ID = c.User_ID
                                                    WHERE Org_ID = %s AND JD_API_Org_ID = %s;"""
    return select_JD_subscription_ID_by_Org_ID_and_JD_API_org_ID_query

def select_JD_subscription_ID_by_JD_API_org_ID_query():
    select_JD_subscription_ID_by_JD_org_ID_query = "SELECT SQL_NO_CACHE JD_Subscription_ID FROM JD_Org_Info WHERE `JD_API_Org_ID`= %s;"
    return select_JD_subscription_ID_by_JD_org_ID_query


def select_JD_subscription_filters_by_Org_ID_and_JD_API_org_ID_query():
    select_JD_subscription_filters_by_Org_ID_and_JD_API_org_ID_query = """
                            SELECT SQL_NO_CACHE a.JD_Subscription_Filters FROM JD_Org_Info AS a 
                            JOIN User_JD_Org_Info AS b 
                            ON a.JD_Org_ID = b.JD_Org_ID
                            JOIN User_Org_Info AS c
                            ON b.User_ID = c.User_ID
                            WHERE c.Org_ID = %s AND a.JD_API_Org_ID = %s;"""
    return select_JD_subscription_filters_by_Org_ID_and_JD_API_org_ID_query

def select_JD_org_type_by_JD_org_ID_query():
    select_JD_org_type_by_JD_org_ID_query = "SELECT SQL_NO_CACHE JD_Org_Type FROM JD_Org_Info WHERE `JD_Org_ID`= %s;"
    return select_JD_org_type_by_JD_org_ID_query

def select_JD_username_by_JD_Org_ID_query():
    select_JD_username_by_JD_Org_ID_query = "SELECT SQL_NO_CACHE JD_Username FROM JD_Org_Info WHERE `JD_Org_ID`= %s;"
    return select_JD_username_by_JD_Org_ID_query

def select_JD_access_level_by_JD_org_ID_query():
    select_JD_access_level_by_JD_org_ID_query = "SELECT SQL_NO_CACHE JD_Access_Level FROM JD_Org_Info WHERE `JD_Org_ID`= %s;"
    return select_JD_access_level_by_JD_org_ID_query

def select_JD_token_ID_by_JD_org_ID_query():
    select_JD_token_ID_by_JD_org_ID_query = "SELECT SQL_NO_CACHE JD_Token_ID FROM JD_Org_Info WHERE `JD_Org_ID`= %s;"
    return select_JD_token_ID_by_JD_org_ID_query

def select_JD_access_token_by_JD_org_ID_query():
    select_JD_access_token_query = "SELECT SQL_NO_CACHE JD_Access_Token FROM JD_Org_Info WHERE `JD_Org_ID`= %s;"
    return select_JD_access_token_query

def select_JD_refresh_token_by_JD_org_ID_query():
    select_JD_refresh_token_by_JD_org_ID_query = "SELECT SQL_NO_CACHE JD_Refresh_Token FROM JD_Org_Info WHERE `JD_Org_ID`= %s;"
    return select_JD_refresh_token_by_JD_org_ID_query
 
def select_JD_token_expiration_by_JD_org_ID_query():
    select_JDTokenExpiration_query = "SELECT SQL_NO_CACHE JD_Token_Expiration FROM JD_Org_Info WHERE `JD_Org_ID`= %s;"
    return select_JDTokenExpiration_query
    
def select_x_deere_signature_by_JD_org_ID_query():
    select_x_deere_signature_by_JD_org_ID_query = "SELECT SQL_NO_CACHE x_deere_signature FROM JD_Org_Info WHERE `JD_Org_ID`= %s;"
    return select_x_deere_signature_by_JD_org_ID_query

def select_JD_API_Org_ID_by_JD_org_ID_query():
    select_JD_API_Org_ID_by_JD_org_ID_query = "SELECT SQL_NO_CACHE JD_API_Org_ID FROM JD_Org_Info WHERE `JD_Org_ID`= %s;"
    return select_JD_API_Org_ID_by_JD_org_ID_query


#       * Specific Information Sets
# def select_UserID(password,email):
#     select_UserID_query = "SELECT User_ID FROM User_Info WHERE `Password`='" + password + "' AND `Email`='" + email + "'"
#     return select_UserID_query

# def select_UserID_byOrgID(orgID):
#     select_UserID_byOrgID_query = "SELECT User_ID FROM Org_Info WHERE `Org_ID`='" + orgID + "'"
#     return select_UserID_byOrgID_query

def select_User_ID_by_UserName():
    select_UserID_query = "SELECT SQL_NO_CACHE User_ID FROM User_Info WHERE `UserName`= %s;" 
    return select_UserID_query

# def select_UserName(userID):
#     select_UserName_query = "SELECT UserName FROM User_Info WHERE `User_ID`='" + userID + "'"
#     return select_UserName_query
    
# def select_UserStatus(userID):
#     select_UserStatus_query = "SELECT Status FROM User_Info WHERE `User_ID`='" + userID + "'"
#     return select_UserStatus_query

def select_OrgID_by_User_ID():
    select_OrgID_query = "SELECT SQL_NO_CACHE Org_ID FROM User_Org_Info WHERE `User_ID`= %s;"
    return select_OrgID_query

def select_OrgID_From_User_Org_Info():
    select_OrgID_query = "SELECT SQL_NO_CACHE Org_ID FROM User_Org_Info WHERE `User_ID`= %s;"
    return select_OrgID_query

# def select_OrgID_byJDToken(jdToken):
#     select_OrgID_byJDToken_query = "SELECT Org_ID FROM JD_OrgInfo WHERE `JD_Subscription_Token`='" + jdToken + "'"
#     return select_OrgID_byJDToken_query

# def select_FarmID(orgID):
#     select_FarmID_query = "SELECT Farm_ID FROM Farm_Info WHERE `Org_ID`='" + orgID + "'"
#     return select_FarmID_query
    
def select_FarmID_byJDFarmIDssOrgID():
    select_FarmID_byJDFarmIDssOrgID_query = "SELECT SQL_NO_CACHE Farm_ID FROM Farm_Info WHERE `JD_Farm_ID`=%s AND `Org_ID`=%s;"
    return select_FarmID_byJDFarmIDssOrgID_query

# def select_FarmID_byJDFieldID(jdFieldID):
#     select_FarmID_byJDFieldID_query = "SELECT Farm_ID FROM Field_Info WHERE `JD_FieldID`='" + jdFieldID + "'"
#     return select_FarmID_byJDFieldID_query

# def select_FarmName(farmID):
#     select_FarmName_query = "SELECT Farm_Name FROM Farm_Info WHERE `Farm_ID`='" + farmID + "'"
#     return select_FarmName_query
    
# def select_FieldID(farmID):
#     select_FieldID_query = "SELECT Field_ID FROM Field_Info WHERE `Farm_ID`='" + farmID + "'"
#     return select_FieldID_query
    
# def select_FieldID_byJDFieldID(jdFieldID):
#     select_FieldID_byJDFieldID_query = "SELECT Field_ID FROM Field_Info WHERE `JD_FieldID`='" + jdFieldID + "'"
#     return select_FieldID_byJDFieldID_query

def select_FieldID_byJDFieldIDssFarmID():
    select_FieldID_byJDFieldIDssFarmID_query = "SELECT SQL_NO_CACHE Field_ID FROM Field_Info WHERE `JD_Field_ID`=%s AND `Farm_ID`=%s;"
    return select_FieldID_byJDFieldIDssFarmID_query

# def select_FieldName(fieldID):
#     select_FieldName_query = "SELECT Field_Name FROM Field_Info WHERE `Field_ID`='" + fieldID + "'"
#     return select_FieldName_query

# def select_JDOrgFarmIDs(orgID,jdOrgID):
#     select_JDOrgFarmIDs_query = "SELECT JD_FarmID FROM Farm_Info WHERE `Org_ID`='" + orgID + "' AND `JD_OrgID`='" + jdOrgID + "'"
#     return select_JDOrgFarmIDs_query

# def select_OrgFarmIDs(orgID):
#     select_OrgFarmIDs_query = "SELECT Farm_ID FROM Farm_Info WHERE `Org_ID`='" + orgID + "'"
#     return select_OrgFarmIDs_query

def select_OrgFarmIDs_JDOrg():
    select_OrgFarmIDs_JDOrg_query = "SELECT SQL_NO_CACHE Farm_ID FROM Farm_Info as a JOIN JD_Org_Info AS b ON a.JD_Org_ID = b.JD_Org_ID WHERE a.Org_ID=%s AND b.JD_API_Org_ID=%s;"
    return select_OrgFarmIDs_JDOrg_query


def select_OrgFieldIDs():
    select_OrgFieldIDs_query = "SELECT SQL_NO_CACHE JD_Field_ID FROM Field_Info WHERE `Farm_ID`=%s"
    return select_OrgFieldIDs_query


# #       * Entire Information Sets
# def select_User(password,email):
#     select_User_query = "SELECT * FROM User_Info WHERE `Password`='" + password + "' AND `Email`='" + email + "'"
#     return select_User_query

def select_FarmInstance():
    select_FarmInstance_query = """SELECT SQL_NO_CACHE * FROM Farm_Info AS a
                                JOIN JD_Org_Info as b ON a.JD_Org_ID = b.JD_Org_ID
                                WHERE a.Org_ID=%s AND b.JD_API_Org_ID=%s AND a.JD_Farm_ID=%s;"""
    return select_FarmInstance_query
    
def select_FieldInstance():
    select_FarmInstance_query = "SELECT SQL_NO_CACHE * FROM Field_Info WHERE `Farm_ID`=%s AND `JD_Field_ID`=%s;"
    return select_FarmInstance_query

# def select_OrgInfo_byUserID(userID):
#     select_OrgInfo_byUserID_query = "SELECT * FROM Org_Info WHERE `User_ID`='" + userID + "'"
#     return select_OrgInfo_byUserID_query
    
def select_OrgInfo_byOrgID():
    select_OrgInfo_byOrgID_query = "SELECT SQL_NO_CACHE * FROM Org_Info WHERE `Org_ID`=%s;"
    return select_OrgInfo_byOrgID_query

def select_JD_Org_Info_byOrgID():
    select_OrgInfo_byOrgID_query = """SELECT SQL_NO_CACHE * FROM JD_Org_Info AS a 
                            JOIN User_JD_Org_Info AS b 
                            ON a.JD_Org_ID = b.JD_Org_ID
                            JOIN User_Org_Info AS c
                            ON b.User_ID = c.User_ID
                            WHERE c.Org_ID = %s"""
    return select_OrgInfo_byOrgID_query

# def select_JDOrgInfo(orgID):
#     select_JDOrgInfo_query = "SELECT * FROM JD_OrgInfo WHERE `Org_ID`='" + orgID + "'"
#     return select_JDOrgInfo_query
   
# def select_JDOrgInfo_byJDToken(jdToken):
#     select_JDOrgInfo_byJDToken_QUERY = "SELECT * FROM JD_OrgInfo WHERE `JD_Subscription_Token`='" + jdToken + "'"
#     return select_JDOrgInfo_byJDToken_QUERY

# def select_Farms(orgID):
#     select_Farms_query = "SELECT * FROM Farm_Info WHERE `Org_ID`='" + orgID + "'"
#     return select_Farms_query   

# def select_FarmInfo(farmID):
#     select_FarmInfo_query = "SELECT * FROM Farm_Info WHERE `Farm_ID`='" + farmID + "'"
#     return select_FarmInfo_query

# def select_Fields(farmID):
#     select_Fields_query = "SELECT * FROM Field_Info WHERE `Farm_ID`='" + farmID + "'"
#     return select_Fields_query
    
# def select_FieldInfo(fieldID):
#     select_FieldInfo_query = "SELECT * FROM Field_Info WHERE `Field_ID`='" + fieldID + "'"
#     return select_FieldInfo_query





