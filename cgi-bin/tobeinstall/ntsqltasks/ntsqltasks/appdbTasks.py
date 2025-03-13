# -*- coding: utf-8 -*-
#"""
#Created on Sat Jul 11 12:55:40 2020
#
#@author: thors
#"""


#   ************************************************************
#   ** Create 'ssAppData' Database Connection **
#   ************************************************************
def create_AppDB_Connection():
    import mysql.connector
    from mysql.connector.errors import Error
    
    try:
        connection = mysql.connector.connect(
            host = "132.148.180.201",
            user = "ssUser_Admin",
            password = "UNLSpraySafely1*",
            database = "ssUser_Info",
            )
        if connection.is_connected():    
            print(connection)
            #cursor = connection.cursor()
            #print(cursor)
            return connection
    except Error as e:
        print(e)

def close_AppDB_Connection(conn):
    import mysql.connector
    from mysql.connector.errors import Error
    
    if conn.is_connected():
        conn.close()
        
    conn = None

    return conn

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
            if vals:
                with connection.cursor() as cursor:
                    cursor.execute(sql_query, vals)
                    records = cursor.fetchall()
                    cursor.close()
                    return records
            else:
                return "No information provided"
        else:
            return "Failed connection"
    except Error as e:
        print (e)

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
#   ** Main App_Data EVENT DATABASE STRUCTURE **
#   ************************************************************

#   ************************************************************
#   * Create Main Table *
#   ************************************************************
def create_AppInfo_tbl():
    create_AppInfo_tbl_query = """CREATE TABLE IF NOT EXISTS 
                                        App_Info(
                                            Application_ID INT NOT NULL AUTO_INCREMENT,
                                            Field_ID INT NOT NULL,
                                            Applicator_ID INT NOT NULL,
                                            Tank_Mix_ID INT NOT NULL,
                                            App_Type text NOT NULL,
                                            Start_Time text NOT NULL,
                                            End_Time text NOT NULL,
                                            REI_Exp text NOT NULL,
                                            Equipment_Name text NOT NULL,
                                            Weather text NOT NULL,
                                            JD_Application_ID INT,
                                            Geometry longtext NOT NULL,
                                            PRIMARY KEY (Application_ID),
                                            FOREIGN KEY (Field_ID)
                                                REFERENCES Field_Info (Field_ID),
                                            FOREIGN KEY (Applicator_ID) 
                                                REFERENCES Applicator_Info (Applicator_ID),
                                            FOREIGN KEY (Tank_Mix_ID)
                                                REFERENCES Tank_Mix_Info (Tank_Mix_ID)
                                         )"""
    return create_AppInfo_tbl_query

#   ************************************************************    
#   * Create Relational Tables *
#   ************************************************************
def create_ApplicatorInfo_tbl():
    create_ApplicatorInfo_tbl_query = """CREATE TABLE IF NOT EXISTS 
                                                Applicator_Info(
                                                    Applicator_ID INT NOT NULL AUTO_INCREMENT,
                                                    First_Name text NOT NULL,
                                                    Last_Name text NOT NULL,
                                                    License_Type text NOT NULL,
                                                    License_Num text NOT NULL,
                                                    Licensed_Cat text NOT NULL,
                                                    License_Exp text NOT NULL,
                                                    PRIMARY KEY (Applicator_ID)
                                                )"""
    return create_ApplicatorInfo_tbl_query

def create_InstructorInfo_tbl():
    create_InstructorInfo_tbl_query = """CREATE TABLE IF NOT EXISTS 
                                                Instructor_Info(
                                                    Instructor_ID INT NOT NULL AUTO_INCREMENT,
                                                    First_Name text NOT NULL,
                                                    Last_Name text NOT NULL,
                                                    Contact_Num text NOT NULL,
                                                    Address text NOT NULL,
                                                    Email text NOT NULL,
                                                    Cert_Date text NOT NULL,
                                                    Cert_Exp text NOT NULL,
                                                    PRIMARY KEY (Instructor_ID)
                                                )"""
    return create_InstructorInfo_tbl_query

def create_TankMixInfo_tbl():
    create_TankMixInfo_tbl_query = """CREATE TABLE IF NOT EXISTS
                                                Tank_Mix_Info(
                                                    Tank_Mix_ID INT NOT NULL AUTO_INCREMENT,
                                                    Tank_Mix_Name text NOT NULL,
                                                    User_ID INT NOT NULL,
                                                    PRIMARY KEY (Tank_Mix_ID)
                                                    FOREIGN KEY (User_ID)
                                                        REFERENCES User_Info(User_ID)
                                                )"""
    return create_TankMixInfo_tbl_query

def create_TankMixCarrierInfo_tbl():
    create_TankMixCarrierInfo_tbl_query = """CREATE TABLE IF NOT EXISTS
                                                Tank_Mix_Carrier_Info(
                                                    Tank_Mix_ID INT NOT NULL,
                                                    Carrier_ID INT NOT NULL,
                                                    Rate double NOT NULL,
                                                    Units text NOT NULL,
                                                    FOREIGN KEY (Tank_Mix_ID)
                                                        REFERENCES Tank_Mix_Info (Tank_Mix_ID),
                                                    FOREGIN KEY (Carrier_ID)
                                                        REFERENCES Carrier_Info (Carrier_ID)
                                                )"""
    return create_TankMixCarrierInfo_tbl_query

def create_CarrierInfo_tbl():
    create_CarrierInfo_tbl_query = """CREATE TABLE IF NOT EXISTS
                                                Carrier_Info(
                                                    Carrier_ID INT NOT NULL AUT_INCREMENT,
                                                    Carrier_Name text NOT NULL,
                                                    PRIMARY KEY (Carrier_ID)
                                                )"""
    return create_CarrierInfo_tbl_query

def create_TankMixProductInfo_tbl():
    create_TankMixProductInfo_tbl_query = """CREATE TABLE IF NOT EXISTS
                                                Tank_Mix_Product_Info(
                                                    Tank_Mix_ID INT NOT NULL,
                                                    Product_ID INT NOT NULL,
                                                    Rate double NOT NULL,
                                                    Units text NOT NULL,
                                                    FOREIGN KEY (Tank_Mix_ID)
                                                        REFERENCES Tank_Mix_Info (Tank_Mix_ID),
                                                    FOREGIN KEY (Product_ID)
                                                        REFERENCES Product_Info (Product_ID)
                                                )"""
    return create_TankMixProductInfo_tbl_query

def create_ProductInfo_tbl():
    create_ProductInfo_tbl_query = """CREATE TABLE IF NOT EXISTS
                                                Product_Info(
                                                    Product_ID INT NOT NULL AUT_INCREMENT,
                                                    Product_Name text NOT NULL,
                                                    REI_Time_Hours INT NOT NULL,
                                                    REI_Description text NOT NULL,
                                                    Is_Irregular tinyint NOT NULL
                                                    PRIMARY KEY (Product_ID)
                                                )"""
    return create_ProductInfo_tbl_query

            # NOTE: Owner_Info Table see 'Main Application Event Database 
            #       Structure' 
            # NOTE: User_Info Table see ' User Information Database Structure' 


#   ************************************************************
#   *** MANIPULATE DATABASE TABLE DATA ***
#   * Description - 
#   ************************************************************

        
#   ************************************************************
#   ** Insert Table Information **
#   ************************************************************
def insert_Application():
    insert_Application_query = """INSERT INTO 
                                    App_Info(
                                        Application_ID,
                                        Field_ID,
                                        Applicator_ID,
                                        Tank_Mix_ID,
                                        App_Type,
                                        Start_Time,
                                        End_Time,
                                        REI_Exp,
                                        Equipment_Name,
                                        Weather,
                                        JD_Application_ID,
                                        Geometry
                                    )
                                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    return insert_Application_query

def insert_Applicator():
    insert_Applicator_query = """INSERT INTO
                                    Applicator_Info(
                                        Applicator_ID,
                                        First_Name,
                                        Last_Name,
                                        License_Type,
                                        License_Num,
                                        Licensed_Cat,
                                        License_Exp
                                    )
                                    VALUES (%s,%s,%s,%s,%s,%s,%s)"""
    return insert_Applicator_query

def insert_Instructor():
    insert_Instructor_query = """INSERT INTO
                                    Instructor_Info(
                                        Instructor_ID,
                                        First_Name,
                                        Last_Name,
                                        Contact_Num,
                                        Address,
                                        Email,
                                        Cert_Date,
                                        Cert_Exp
                                    )
                                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
    return insert_Instructor_query
    
def insert_TankMix():
    insert_Tank_Mix_query = """INSERT INTO
                                    Tank_Mix_Info(
                                        Tank_Mix_ID,
                                        Tank_Mix_Name,
                                        User_ID
                                    )
                                    VALUES (%s,%s,%s)"""
    return insert_Tank_Mix_query

def insert_TankMixCarrier():
    insert_Tank_Mix_Carrier_query = """INSERT INTO
                                    Tank_Mix_Carrier_Info(
                                        Tank_Mix_Carrier_ID,
                                        Tank_Mix_ID,
                                        Carrier_ID,
                                        Rate,
                                        Units
                                    )
                                    VALUES (%s,%s,%s,%s,%s)"""
    return insert_Tank_Mix_Carrier_query

def insert_TankMixProduct():
    insert_Tank_Mix_Product_query = """INSERT INTO
                                    Tank_Mix_Product_Info(
                                        Tank_Mix_Product_ID,
                                        Tank_Mix_ID,
                                        Product_ID,
                                        Rate,
                                        Units
                                    )
                                    VALUES (%s,%s,%s,%s,%s)"""
    return insert_Tank_Mix_Product_query

def insert_Carrier():
    insert_Carrier_query = """INSERT INTO
                                    Carrier_Info(
                                        Carrier_ID,
                                        Carrier_Name
                                    )
                                    VALUES (%s,%s)"""
    return insert_Carrier_query

def insert_Product():
    insert_Product_query = """INSERT INTO
                                    Product_Info(
                                        Product_ID,
                                        Product_Name,
                                        REI_Time
                                    )
                                    VALUES (%s,%s,%s)"""
    return insert_Product_query

#   ************************************************************    
#   ** Update Table Information **
#   ************************************************************

#Application -
#    # Farm ID
# def update_App_FarmID(farmID,appID):
#     update_App_FarmID_post = "UPDATE App_Info SET `Farm_ID`= %s  WHERE `Application_ID`= %s;"
#     return update_App_FarmID_post
    #Field ID
def update_App_FieldID(fieldID,appID):
    update_App_FieldID_post = "UPDATE App_Info SET `Field_ID`= %s  WHERE `Application_ID`= %s;"
    return update_App_FieldID_post
    #Applicator ID
def update_App_ApplicatorID(applicatorID,appID):
    update_App_ApplicatorID_post = "UPDATE App_Info SET `Applicator_ID`= %s  WHERE `Application_ID`= %s;"
    return update_App_ApplicatorID_post
#     #Date
# def update_App_Date(date,appID):
#     update_App_Date_post = "UPDATE App_Info SET `Date`= %s  WHERE `Application_ID`= %s;"
#     return update_App_Date_post
    #TankMix
def update_App_TankMix(tankmix,appID):
    update_App_TankMix_post = "UPDATE App_Info SET `Tank_Mix_ID`= %s  WHERE `Application_ID`= %s;"
    return update_App_TankMix_post
    #App_Type
def update_App_AppType(appType,appID):
    update_App_AppType_post = "UPDATE App_Info SET `App_Type`= %s  WHERE `Application_ID`= %s;"
    return update_App_AppType_post
    #Start_Time
def update_App_StartTime(startTime,appID):
    update_App_StartTime_post = "UPDATE App_Info SET `Start_Time`= %s  WHERE `Application_ID`= %s;"
    return update_App_StartTime_post
    #End Time
def update_App_EndTime(endTime,appID):
    update_App_EndTime_post = "UPDATE App_Info SET `End_Time`= %s  WHERE `Application_ID`= %s;"
    return update_App_EndTime_post
    #REI Expiration
def update_App_REIExp(reiExp,appID):
    update_App_REIExp_post = "UPDATE App_Info SET `REI_Exp`= %s  WHERE `Application_ID`= %s;"
    return update_App_REIExp_post
    #Equipment Name
def update_App_EquipmentName(equipName,appID):
    update_App_EquipmentName_post = "UPDATE App_Info SET `Equipment_Name`= %s  WHERE `Application_ID`= %s;"
    return update_App_EquipmentName_post
    #Weather
def update_App_Weather(weather,appID):
    update_App_Weather_post = "UPDATE App_Info SET `Weather`= %s  WHERE `Application_ID`= %s;"
    return update_App_Weather_post
#     #JD Event ID
# def update_App_JDEventID(jdEventID,appID):
#     update_App_JDEventID_post = "UPDATE App_Info SET `JD_Event_ID`= %s  WHERE `Application_ID`= %s;"
#     return update_App_JDEventID_post
    #JD App ID
def update_App_JDAppID(jdAppID,appID):
    update_App_JDAppID_post = "UPDATE App_Info SET `JD_Application_ID`= %s  WHERE `Application_ID`= %s;"
    return update_App_JDAppID_post
    #Geometry
def update_App_Geometry(geometry,appID):
    update_App_Geometry_post = "UPDATE App_Info SET `Geometry`= %s  WHERE `Application_ID`= %s;"
    return update_App_Geometry_post  


#Applicator -
    #First_Name
def update_Appl_FirstName(firstName,applID):
    update_Appl_FirstName_post = "UPDATE Applicator_Info SET `First_Name`= %s  WHERE `Applicator_ID`= %s;"
    return update_Appl_FirstName_post
    #Last_Name
def update_Appl_LastName(lastName,applID):
    update_Appl_LastName_post = "UPDATE Applicator_Info SET `Last_Name`= %s  WHERE `Applicator_ID`= %s;"
    return update_Appl_LastName_post
    #License_Type
def update_Appl_LicType(licType,applID):
    update_Appl_LicType_post = "UPDATE Applicator_Info SET `License_Type`= %s  WHERE `Applicator_ID`= %s;"
    return update_Appl_LicType_post
    #License_Num
def update_Appl_LicNum(licNum,applID):
    update_Appl_LicNum_post = "UPDATE Applicator_Info SET `License_Num`= %s  WHERE `Applicator_ID`= %s;"
    return update_Appl_LicNum_post
    #Licensed_Categories
def update_Appl_LicCat(licCat,applID):
    update_Appl_LicCat_post = "UPDATE Applicator_Info SET `Licensed_Cat`= %s  WHERE `Applicator_ID`= %s;"
    return update_Appl_LicCat_post
    #License_Expiration
def update_Appl_LicExp(licExp,applID):
    update_Appl_LicExp_post = "UPDATE Applicator_Info SET `License_Exp`= %s  WHERE `Applicator_ID`= %s;"
    return update_Appl_LicExp_post


#Instructor -
    #First_Name
def update_Instr_FirstName(firstName,instrID):
    update_Instr_FirstName_post = "UPDATE Instructor_Info SET `First_Name`= %s  WHERE `Instructor_ID`= %s;"
    return update_Instr_FirstName_post
    #Last_Name
def update_Instr_lastName(lastName,instrID):
    update_Instr_LastName_post = "UPDATE Instructor_Info SET `Last_Name`= %s  WHERE `Instructor_ID`= %s;"
    return update_Instr_LastName_post
    #Contact_Num
def update_Instr_ContactNum(contactNum,instrID):
    update_Instr_ContactNum_post = "UPDATE Instructor_Info SET `Contact_Num`= %s  WHERE `Instructor_ID`= %s;"
    return update_Instr_ContactNum_post
    #Address
def update_Instr_Address(address,instrID):
    update_Instr_Address_post = "UPDATE Instructor_Info SET `Address`= %s  WHERE `Instructor_ID`= %s;"
    return update_Instr_Address_post
    #Email
def update_Instr_Email(email,instrID):
    update_Instr_Email_post = "UPDATE Instructor_Info SET `Email`= %s  WHERE `Instructor_ID`= %s;"
    return update_Instr_Email_post
    #Cert_Date
def update_Instr_CertDate(certDate,instrID):
    update_Instr_CertDate_post = "UPDATE Instructor_Info SET `Cert_Date`= %s  WHERE `Instructor_ID`= %s;"
    return update_Instr_CertDate_post
    #Cert_Exp
def update_Instr_CertExp(certExp,instrID):
    update_Instr_CertExp_post = "UPDATE Instructor_Info SET `Cert_Exp`= %s  WHERE `Instructor_ID`= %s;"
    return update_Instr_CertExp_post

#Tank Mix Info -
    #Tank_Mix_Name
def update_TankMixInfo_Name(tankMixName,tankMixID):
    update_TankMixInfo_Name_post = "UPDATE Tank_Mix_Info SET `Tank_Mix_Name`= %s  WHERE `Tank_Mix_ID`= %s;"
    return update_TankMixInfo_Name_post

# Tank Mix Carrier Info -
    #Rate
def update_TankMixCarrierInfo_Rate(rate,tankMixID,carrierID):
    update_TankMixCarrierInfo_Rate_post = "UPDATE Tank_Mix_Carrier_Info SET `Rate`= %s  WHERE `Tank_Mix_ID`= %s  AND `Carrier_ID`= %s;"
    return update_TankMixCarrierInfo_Rate_post
    #Units
def update_TankMixCarrierInfo_Units(units,tankMixID,carrierID):
    update_TankMixCarrierInfo_Units_post = "UPDATE Tank_Mix_Carrier_Info SET `Units`= %s  WHERE `Tank_Mix_ID`= %s  AND `Carrier_ID`= %s;"
    return update_TankMixCarrierInfo_Units_post

# Tank Mix Product Info -
    #Rate
def update_TankMixProductInfo_Rate(rate,tankMixID,productID):
    update_TankMixProductInfo_Rate_post = "UPDATE Tank_Mix_Product_Info SET `Rate`= %s  WHERE `Tank_Mix_ID`= %s  AND `Product_ID`= %s;"
    return update_TankMixProductInfo_Rate_post
    #Units
def update_TankMixProductInfo_Units(units,tankMixID,productID):
    update_TankMixProductInfo_Units_post = "UPDATE Tank_Mix_Product_Info SET `Units`= %s  WHERE `Tank_Mix_ID`= %s  AND `Product_ID`= %s;"
    return update_TankMixProductInfo_Units_post

# Carrier
    #Name
def update_CarrierInfo_Name(name,carrierID):
    update_CarrierInfo_Name_post = "UPDATE Carrier_Info SET `Carrier_Name`= %s  WHERE `Carrier_ID`= %s;"
    return update_CarrierInfo_Name_post

# Product
    #Name
def update_ProductInfo_Name(name,productID):
    update_ProductInfo_Name_post = "UPDATE Product_Info SET `Product_Name`= %s  WHERE `Product_ID`= %s;"
    return update_ProductInfo_Name_post
    #REI_Time_Hours
def update_ProductInfo_REI_Time_Hours(reiTimeHours,productID):
    update_ProductInfo_REI_Time_Hours_post = "UPDATE Product_Info SET `REI_Time_Hours`= %s  WHERE `Product_ID`= %s;"
    return update_ProductInfo_REI_Time_Hours_post
    #REI_Description
def update_ProductInfo_REI_Description(reiDescription,productID):
    update_ProductInfo_REI_Description_post = "UPDATE Product_Info SET `REI_Description`= %s  WHERE `Product_ID`= %s;"
    return update_ProductInfo_REI_Description_post
    #Is_Irregular
def update_ProductInfo_Is_Irregular(isIrregular,productID):
    update_ProductInfo_Is_Irregular_post = "UPDATE Product_Info SET `Is_Irregular`= %s  WHERE `Product_ID`= %s;"
    return update_ProductInfo_Is_Irregular_post

#   ************************************************************
#   ** Delete Table Information **
#   ************************************************************

#Application
def delete_Application(appID):
    delete_Application_post = "DELETE FROM App_Info WHERE `Application_ID`= %s;"
    return delete_Application_post
#Applicator
def delete_Applicator(applID):
    delete_Applicator_post = "DELETE FROM Applicator_Info WHERE `Applicator_ID`= %s;"
    return delete_Applicator_post
#Instructor
def delete_Instructor(instrID):
    delete_Instructor_post = "DELETE FROM Instructor_Info WHERE `Instructor_ID`= %s;"
    return delete_Instructor_post
#TankMixInfo
def delete_TankMixInfo(tankMixID):
    delete_TankMixInfo_post = "DELETE FROM Tank_Mix_Info WHERE `Tank_Mix_ID`= %s;"
    return delete_TankMixInfo_post
#TankMixCarrierInfo
def delete_TankMixCarrierInfo(tankMixID,carrierID):
    delete_TankMixCarrierInfo_post = "DELETE FROM Tank_Mix_Carrier_Info WHERE `Tank_Mix_ID`= %s  AND `Carrier_ID`= %s;"
    return delete_TankMixCarrierInfo_post
#TankMixProductInfo
def delete_TankMixProductInfo(tankMixID,productID):
    delete_TankMixProductInfo_post = "DELETE FROM Tank_Mix_Product_Info WHERE `Tank_Mix_ID`= %s  AND `Product_ID`= %s;"
    return delete_TankMixProductInfo_post
#CarrierInfo
def delete_CarrierInfo(carrierID):
    delete_CarrierInfo_post = "DELETE FROM Carrier_Info WHERE `Carrier_ID`= %s;"
    return delete_CarrierInfo_post
#ProductInfo
def delete_ProductInfo(productID):
    delete_ProductInfo_post = "DELETE FROM Product_Info WHERE `Product_ID`= %s;"
    return delete_ProductInfo_post


#   ************************************************************
#   ** Query Table Information **
#   ************************************************************

#       * Specific Information Sets
#Application -
#     #ID by Org_ID
# def select_AppID_byOrgID(orgID):
#     select_AppID_byOrgID_query = "SELECT ID FROM App_Info WHERE `Org_ID`= %s;"
#     return select_AppID_byJDAppID_query
#     #ID by JD_Event_ID
# def select_AppID_byJDEventID(jdEventIDID):
#     select_AppID_byJDEventID_query = "SELECT ID FROM App_Info WHERE `JD_Event_ID`= %s;"
#     return select_AppID_byJDEventID_query
    #ID by JD_App_ID
def select_AppID_byJDAppID(jdAppID):
    select_AppID_byJDAppID_query = "SELECT Application_ID FROM App_Info WHERE `JD_Application_ID`= %s;"
    return select_AppID_byJDAppID_query
# def select_AppID_byOrgJDAppID(orgID,jdAppID):
#     select_AppID_byOrgJDAppID_query = "SELECT ID FROM App_Info WHERE `Org_ID`= %s  AND `JD_Application_ID`= %s;"
#     return select_AppID_byOrgJDAppID_query
#     #Org ID
# def select_AppOrgID(appID):
#     select_AppOrgID_query = "SELECT Org_ID FROM App_Info WHERE `ID`= %s;"
#     return select_AppOrgID_queryv
#     #Farm ID
# def select_AppFarmID(appID):
#     select_AppFarmID_query = "SELECT Farm_ID FROM App_Info WHERE `ID`= %s;"
#     return select_AppFarmID_query
    #Field ID
def select_AppFieldID(appID):
    select_AppFieldID_query = "SELECT Field_ID FROM App_Info WHERE `Application_ID`= %s;"
    return select_AppFieldID_query
    #Applicator ID
def select_AppApplicatorID(appID):
    select_AppApplicatorID_query = "SELECT Applicator_ID FROM App_Info WHERE `Application_ID`= %s;"
    return select_AppApplicatorID_query
#     #Date
# def select_AppDate(appID):
#     select_AppDate_query = "SELECT Date FROM App_Info WHERE `ID`= %s;"
#     return select_AppDate_query
    #TankMix
def select_AppTankMix(appID):
    select_AppTankMix_query = "SELECT Tank_Mix_ID FROM App_Info WHERE `Application_ID`= %s;"
    return select_AppTankMix_query
    #Application Type
def select_AppType(appID):
    select_AppType_query = "SELECT App_Type FROM App_Info WHERE `Application_ID`= %s;"
    return select_AppType_query
    #Start Time
def select_AppStartTime(appID):
    select_AppStartTime_query = "SELECT Start_Time FROM App_Info WHERE `Application_ID`= %s;"
    return select_AppStartTime_query
    #End Time
def select_AppEndTime(appID):
    select_AppEndTime_query = "SELECT End_Time FROM App_Info WHERE `Application_ID`= %s;"
    return select_AppEndTime_query
    #REI Expiration
def select_AppREIExp(appID):
    select_AppREIExp_query = "SELECT REI_Exp FROM App_Info WHERE `Application_ID`= %s;"
    return select_AppREIExp_query
    #Equipment Name
def select_AppEquipName(appID):
    select_AppEquipName_query = "SELECT Equipment_Name FROM App_Info WHERE `Application_ID`= %s;"
    return select_AppEquipName_query
    #Weather
def select_AppWeather(appID):
    select_AppWeather_query = "SELECT Weather FROM App_Info WHERE `Application_ID`= %s;"
    return select_AppWeather_query
#     #JD Event ID
# def select_AppJDEventID(appID):
#     select_AppJDEventID_query = "SELECT JD_Event_ID FROM App_Info WHERE `ID`= %s;"
#     return select_AppJDEventID_query    
    #JD App ID
def select_AppJDAppID(appID):
    select_AppJDAppID_query = "SELECT JD_Application_ID FROM App_Info WHERE `Application_ID`= %s;"
    return select_AppJDAppID_query
    #Geometry
def select_AppGeometry(appID):
    select_AppGeometry_query = "SELECT Geometry FROM App_Info WHERE `ID`= %s;"
    return select_AppGeometry_query

#Applicator -
    #Applicator ID by FirstName/LastName
def select_ApplID_byFirstLastName(firstName,lastName):
    select_ApplID_byFirstLastName_query = "SELECT Applicator_ID FROM Applicator_Info WHERE `First_Name`= %s  AND `Last_Name`= %s;"
    return select_ApplID_byFirstLastName_query    
    #Applicator ID by License Number
def select_ApplID_byLicNum(licNum):
    select_ApplID_byLicNum_query = "SELECT Applicator_ID FROM Applicator_Info WHERE `License_Num`= %s;"
    return select_ApplID_byLicNum_query 
    #First Name
def select_ApplFirstName(applID):
    select_ApplFirstName_query = "SELECT First_Name FROM Applicator_Info WHERE `Applicator_ID`= %s;"
    return select_ApplFirstName_query
    #Last Name
def select_ApplLastName(applID):
    select_ApplLastName_query = "SELECT Last_Name FROM Applicator_Info WHERE `Applicator_ID`= %s;"
    return select_ApplLastName_query
    #License Type
def select_ApplLicType(applID):
    select_ApplLicType_query = "SELECT License_Type FROM Applicator_Info WHERE `Applicator_ID`= %s;"
    return select_ApplLicType_query
    #License Number
def select_ApplLicNum(applID):
    select_ApplLicNum_query = "SELECT License_Num FROM Applicator_Info WHERE `Applicator_ID`= %s;"
    #License Categories
def select_ApplLicCat(applID):
    select_ApplLicCat_query = "SELECT Licensed_Cat FROM Applicator_Info WHERE `Applicator_ID`= %s;"
    return select_ApplLicCat_query
    #License_Expiration
def select_ApplLicExp(applID):
    select_ApplLicExp_query = "SELECT License_Exp FROM Applicator_Info WHERE `Applicator_ID`= %s;"
    return select_ApplLicExp_query

    
#Instructor -
    #Instructor ID by FirstName/LastName
def select_InstrID_byFirstLastName(firstName,lastName):
    select_InstrID_byFirstLastName_query = "SELECT Instructor_ID FROM Instructor_Info WHERE `First_Name`= %s  AND `Last_Name`= %s;"
    return select_InstrID_byFirstLastName_query
    #Applicator ID by License Number
def select_InstrID_byEmail(email):
    select_InstrID_byEmail_query = "SELECT Instructor_ID FROM Instructor_Info WHERE `Email`= %s;"
    return select_InstrID_byEmail_query
    #Contact Number
def select_InstrContactNum(instrID):
    select_InstrContactNum_query = "SELECT Contact_Num FROM Instructor_Info WHERE `Instructor_ID`= %s;"
    return select_InstrContactNum_query
    #Address
def select_InstrAddress(instrID):
    select_InstrAddress_query = "SELECT Address FROM Instructor_Info WHERE `Instructor_ID`= %s;"
    return select_InstrAddress_query
    #Email
def select_InstrEmail(instrID):
    select_InstrEmail_query = "SELECT Email FROM Instructor_Info WHERE `Instructor_ID`= %s;"
    return select_InstrEmail_query
    #Certification Date
def select_InstrCertDate(instrID):
    select_InstrCertDate_query = "SELECT Cert_Date FROM Instructor_Info WHERE `Instructor_ID`= %s;"
    return select_InstrCertDate_query
    #Certification Expiration
def select_InstrCertExp(instrID):
    select_InstrCertExp_query = "SELECT Cert_Exp FROM Instructor_Info WHERE `Instructor_ID`= %s;"
    return select_InstrCertExp_query


#TankMix -
    #TankMix ID by TankMixName
def select_TankMixID_byTankMixName(tankMixName):
    select_TankMixID_byTankMixName_query = "SELECT Tank_Mix_ID FROM Tank_Mix_Info WHERE `Tank_Mix_Name`= %s;"
    return select_TankMixID_byTankMixName_query
    #TankMix ID by UserID
def select_TankMixID_byUserID(userID):
    select_TankMixID_byUserID_query = "SELECT Tank_Mix_ID FROM Tank_Mix_Info WHERE `User_ID`= %s;"
    return select_TankMixID_byUserID_query
    #TankMixName
def select_TankMixName(tankMixID):
    select_TankMixName_query = "SELECT Tank_Mix_Name FROM Tank_Mix_Info WHERE `Tank_Mix_ID`= %s;"
    return select_TankMixName_query


#TankMixCarrierInfo -
    #TankMix ID by CarrierID
def select_TankMixID_byCarrierID(carrierID):
    select_TankMixID_byCarrierID_query = "SELECT Tank_Mix_ID FROM Tank_Mix_Carrier_Info WHERE `Carrier_ID`= %s;"
    return select_TankMixID_byCarrierID_query
    #Carrier ID by TankMixID
def select_CarrierID_byTankMixID(tankMixID):
    select_CarrierID_byTankMixID_query = "SELECT Carrier_ID FROM Tank_Mix_Carrier_Info WHERE `Tank_Mix_ID`= %s;"
    return select_CarrierID_byTankMixID_query
    #Rate
def select_TankMixCarrierRate(tankMixID,carrierID):
    select_Rate_query = "SELECT Rate FROM Tank_Mix_Carrier_Info WHERE `Tank_Mix_ID`= %s  AND `Carrier_ID`= %s;"
    return select_Rate_query
    #Units
def select_TankMixCarrierUnits(tankMixID,carrierID):
    select_Units_query = "SELECT Units FROM Tank_Mix_Carrier_Info WHERE `Tank_Mix_ID`= %s  AND `Carrier_ID`= %s;"
    return select_Units_query


#TankMixProductInfo -
    #TankMix ID by ProductID
def select_TankMixID_byProductID(productID):
    select_TankMixID_byProductID_query = "SELECT Tank_Mix_ID FROM Tank_Mix_Product_Info WHERE `Product_ID`= %s;"
    return select_TankMixID_byProductID_query
    #Product ID by TankMixID
def select_ProductID_byTankMixID(tankMixID):
    select_ProductID_byTankMixID_query = "SELECT Product_ID FROM Tank_Mix_Product_Info WHERE `Tank_Mix_ID`= %s;"
    return select_ProductID_byTankMixID_query
    #Rate
def select_TankMixProductRate(tankMixID,productID):
    select_Rate_query = "SELECT Rate FROM Tank_Mix_Product_Info WHERE `Tank_Mix_ID`= %s  AND `Product_ID`= %s;"
    return select_Rate_query
    #Units
def select_TankMixProductUnits(tankMixID,productID):
    select_Units_query = "SELECT Units FROM Tank_Mix_Product_Info WHERE `Tank_Mix_ID`= %s  AND `Product_ID`= %s;"
    return select_Units_query


#CarrierInfo -
    #Carrier ID by CarrierName
def select_CarrierID_byCarrierName(carrierName):
    select_CarrierID_byCarrierName_query = "SELECT Carrier_ID FROM Carrier_Info WHERE `Carrier_Name`= %s;"
    return select_CarrierID_byCarrierName_query
    #CarrierName
def select_CarrierName(carrierID):
    select_CarrierName_query = "SELECT Carrier_Name FROM Carrier_Info WHERE `Carrier_ID`= %s;"
    return select_CarrierName_query


#ProductInfo -
    #Product ID by ProductName
def select_ProductID_byProductName(productName):
    select_ProductID_byProductName_query = "SELECT Product_ID FROM Product_Info WHERE `Product_Name`= %s;"
    return select_ProductID_byProductName_query
    #ProductName
def select_ProductName(productID):
    select_ProductName_query = "SELECT Product_Name FROM Product_Info WHERE `Product_ID`= %s;"
    return select_ProductName_query
    #REI_Time_Hours
def select_REI_Time_Hours(productID):
    select_REI_Time_Hours_query = "SELECT REI_Time_Hours FROM Product_Info WHERE `Product_ID`= %s;"
    return select_REI_Time_Hours_query
    #REI_Description
def select_REI_Description(productID):
    select_REI_Description_query = "SELECT REI_Description FROM Product_Info WHERE `Product_ID`= %s;"
    return select_REI_Description_query
    #is_Irregular
def select_Is_Irregular(productID):
    select_Is_Irregular_query = "SELECT Is_Irregular FROM Product_Info WHERE `Product_ID`= %s;"
    return select_Is_Irregular_query


#       * Entire Information Sets
#Application
# def select_App_byOrgID(orgID):
#     select_App_byOrgID_query = "SELECT * FROM App_Info WHERE `Org_ID`= %s;"
#     return select_App_byOrgID_query

def select_App_byAppID():
    select_App_byAppID_query = "SELECT SQL_NO_CACHE * FROM App_Info WHERE `Application_ID`= %s;"
    return select_App_byAppID_query

def select_App_byOrgJDAppID_query():
    select_App_byOrgJDAppID_query = "SELECT SQL_NO_CACHE * FROM App_Info WHERE `Org_ID`= %s  AND `JD_Application_ID`= %s;"
    return select_App_byOrgJDAppID_query
    
# def select_App_byFarmFieldID(farmID,fieldID):
#     select_App_byFarmFieldID_query = "SELECT * FROM App_Info WHERE `Farm_ID`= %s  AND `Field_ID`= %s;"
#     return select_App_byFarmFieldID_query
    
# def select_App_byFarmOrgID(farmID,orgID):
#     select_App_byFarmOrgID_query = "SELECT * FROM App_Info WHERE `Org_ID`= %s  AND `Farm_ID`='" + farmID +  "'"
#     return select_App_byFarmOrgID_query

# def select_App_byFieldOrgID(fieldID,orgID):
#     select_App_byFieldOrgID_query = "SELECT * FROM App_Info WHERE `Org_ID`= %s  AND `Field_ID`= %s;"
#     return select_App_byFieldOrgID_query
    
# def select_App_byFarmFieldOrgID(farmID,fieldID,orgID):
#     select_App_byFarmFieldOrgID_query = "SELECT * FROM App_Info WHERE `Farm_ID`= %s  AND `Field_ID`= %s  AND `Org_ID`= %s;"
#     return select_App_byFarmFieldOrgID_query
    
# def select_App_byJDEventID(jdEventID):
#     select_App_byJDEventID_query = "SELECT * FROM App_Info WHERE `JD_Event_ID`= %s;"
#     return select_App_byJDEventID_query

def select_App_byJDAppID(jdAppID):
    select_App_byJDAppID_query = "SELECT * FROM App_Info WHERE `JD_Application_ID`= %s;"
    return select_App_byJDAppID_query
    
# def select_App_byREIExp(reiExp):
#     select_App_byREIExp_query = "SELECT * FROM App_Info WHERE `REI_Exp`.Date>='" + Convert(datetime,reiExp) + "'"
#     return select_App_byREIExp_query

#Applicator
def select_Appl_byApplID(applID):
    select_Appl_byApplID_query = "SELECT * FROM Applicator_Info WHERE `Applicator_ID`= %s;"
    return select_Appl_byApplID_query

def select_Appl_byFirstLastName(firstName,lastName):
    select_Appl_byFirstLastName_query = "SELECT * FROM Applicator_Info WHERE `First_Name`= %s  AND `Last_Name`= %s;"
    return select_Appl_byFirstLastName_query

def select_Appl_byLicNum(licNum):
    select_Appl_byLicNum_query = "SELECT * FROM Applicator_Info WHERE `License_Num`= %s;"
    return select_Appl_byLicNum_query

def select_Appl_byLicExp(licExp):
    select_Appl_byLicNum_query = "SELECT * FROM Applicator_Info WHERE `License_Exp`<= %s;"
    return select_Appl_byLicNum_query
    
#Instructor
def select_Instr_byInstrID(instrID):
    select_Instr_byInstrID_query = "SELECT * FROM Instructor_Info WHERE `Instructor_ID`= %s;"
    return select_Instr_byInstrID_query
    
def select_Instr_byEmail(email):
    select_Instr_byEmail_query = "SELECT * FROM Instructor_Info WHERE `Email`= %s;"
    return select_Instr_byEmail_query
    
def select_Instr_byFirstLastName(firstName,lastName):
    select_Instr_byFirstLastName_query = "SELECT * FROM Instructor_Info WHERE `First_Name`= %s  AND `Last_Name`= %s;"
    return select_Instr_byFirstLastName_query    

#TankMixInfo
def select_TankMix_ByTankMixID(tankMixID):
    select_TankMix_ByTankMixID_query = "SELECT * FROM Tank_Mix_Info WHERE `Tank_Mix_ID`= %s;"
    return select_TankMix_ByTankMixID_query

def select_TankMix_ByTankMixName(tankMixName):
    select_TankMix_ByTankMixName_query = "SELECT * FROM Tank_Mix_Info WHERE `Tank_Mix_Name`= %s;"
    return select_TankMix_ByTankMixName_query

def select_TankMix_ByUserID(userID):
    select_TankMix_ByUserID_query = "SELECT * FROM Tank_Mix_Info WHERE `User_ID`= %s;"
    return select_TankMix_ByUserID_query

#TankMixCarrierInfo
def select_TankMixCarrier_ByTankMixID(tankMixID):
    select_TankMixCarrier_ByTankMixID_query = "SELECT * FROM Tank_Mix_Carrier_Info WHERE `Tank_Mix_ID`= %s;"
    return select_TankMixCarrier_ByTankMixID_query

def select_TankMixCarrier_ByCarrierID(carrierID):
    select_TankMixCarrier_ByCarrierID_query = "SELECT * FROM Tank_Mix_Carrier_Info WHERE `Carrier_ID`= %s;"
    return select_TankMixCarrier_ByCarrierID_query

def select_TankMixCarrier_ByTankMixID_And_CarrierID(tankMixID,carrierID):
    select_TankMixCarrier_ByTankMixID_And_CarrierID_query = "SELECT * FROM Tank_Mix_Carrier_Info WHERE `Tank_Mix_ID`= %s  AND `Carrier_ID`= %s;"
    return select_TankMixCarrier_ByTankMixID_And_CarrierID_query

#TankMixProductInfo
def select_TankMixProduct_ByTankMixID(tankMixID):
    select_TankMixProduct_ByTankMixID_query = "SELECT * FROM Tank_Mix_Product_Info WHERE `Tank_Mix_ID`= %s;"
    return select_TankMixProduct_ByTankMixID_query

def select_TankMixProduct_ByProductID(productID):
    select_TankMixProduct_ByProductID_query = "SELECT * FROM Tank_Mix_Product_Info WHERE `Product_ID`= %s;"
    return select_TankMixProduct_ByProductID_query

def select_TankMixProduct_ByTankMixID_And_ProductID(tankMixID,productID):
    select_TankMixProduct_ByTankMixID_And_ProductID_query = "SELECT * FROM Tank_Mix_Product_Info WHERE `Tank_Mix_ID`= %s  AND `Product_ID`= %s;"
    return select_TankMixProduct_ByTankMixID_And_ProductID_query

#CarrierInfo
def select_Carrier_ByCarrierID(carrierID):
    select_Carrier_ByCarrierID_query = "SELECT * FROM Carrier_Info WHERE `Carrier_ID`= %s;"
    return select_Carrier_ByCarrierID_query

def select_Carrier_ByCarrierName(carrierName):
    select_Carrier_ByCarrierName_query = "SELECT * FROM Carrier_Info WHERE `Carrier_Name`= %s;"
    return select_Carrier_ByCarrierName_query

#ProductInfo
def select_Product_ByProductID(productID):
    select_Product_ByProductID_query = "SELECT * FROM Product_Info WHERE `Product_ID`= %s;"
    return select_Product_ByProductID_query

def select_Product_ByProductName(productName):
    select_Product_ByProductName_query = "SELECT * FROM Product_Info WHERE `Product_Name`= %s;"
    return select_Product_ByProductName_query
