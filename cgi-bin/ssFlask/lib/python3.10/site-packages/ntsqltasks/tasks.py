# -*- coding: utf-8 -*-
"""
Created on Sat Jul 11 12:55:40 2020

@author: thors
"""
import mysql.connector
from mysql.connector import Error




#   ************************************************************
#   **** EXECUTE QUERY WITHIN MySQL DATABASE ****
#   * Description -  This procedure applies to any query within 
#                    this task file NOT requiring user information, 
#                    and applies to all spray-safely databases 
#                    designated within the query parameters.       
#   ************************************************************
def execute_Create_query(connection, sql_query):

    try:
        with connection.cursor() as cursor:
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
def execute_Instance_query(connection, sql_query, info):
    
    try:
        if connection:
            if info:
                with connection.cursor() as cursor:
                    cursor.executemany(sql_query,info)
                    
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
#   **** 'ssAppData' DATABASE PROCEDURES ****
#   ************************************************************


        
#   ************************************************************
#   *** Main 'ssAppData' DATABASE QUERIES ***
#   ************************************************************


#   ************************************************************
#   ** Create Database Tables **
#   ************************************************************

#   ************************************************************
#   * Create Main Table *
#   ************************************************************
def createMain_db_tbl():
    create_Main_db_tbl_query = """CREATE TABLE IF NOT EXISTS 
                                        Main_db(
                                            ID INT NOT NULL,
                                            Owner_ID INT NOT NULL,
                                            Farm text NOT NULL,
                                            Field text NOT NULL,
                                            Applicator_ID INT NOT NULL,
                                            Date text NOT NULL,
                                            TankMix_ID INT NOT NULL,
                                            App_Type text NOT NULL,
                                            Equipment_Name text NOT NULL,
                                            Weather_ID INT NOT NULL,
                                            PRIMARY KEY (ID),
                                            FOREIGN KEY (Owner_ID) 
                                                REFERENCES Owner_Info(Owner_ID),
                                            FOREIGN KEY (Applicator_ID) 
                                                REFERENCES Applicator_Info (Applicator_ID),
                                            FOREIGN KEY (TankMix_ID) 
                                                REFERENCES TankMix_Info(TankMix_ID),
                                            FOREIGN KEY (Weather_ID) 
                                                REFERENCES Weather_Info(Weather_ID)
                                         )"""
    return create_Main_db_tbl_query
        
#   ************************************************************    
#   * Create Relational Tables *
#   ************************************************************
def createOwnerInfo_tbl():
    create_Owner_Info_table_query = """CREATE TABLE IF NOT EXISTS
                                            Owner_Info(
                                                Owner_ID INT NOT NULL,
                                                First_Name text NOT NULL,
                                                Last_Name text NOT NULL,
                                                Address text NOT NULL,
                                                Account_Name text NOT NULL,
                                                Email text NOT NULL,
                                                Username text NOT NULL,
                                                Password text NOT NULL,
                                                PRIMARY KEY (Owner_ID)
                                            )"""
    return create_Owner_Info_table_query
    
def createApplicatorInfo_tbl():
    create_Applicator_Info_table_query = """CREATE TABLE IF NOT EXISTS 
                                                Applicator_Info(
                                                    Applicator_ID INT NOT NULL,
                                                    First_Name text NOT NULL,
                                                    Last_Name text NOT NULL,
                                                    License_Type text NOT NULL,
                                                    Licensed_Categories text NOT NULL,
                                                    License_Expiration text NOT NULL,
                                                    PRIMARY KEY (Applicator_ID)
                                                )"""
    return create_Applicator_Info_table_query
    
def createTankMixInfo_tbl():
    create_Tank_Mix_Info_table_query = """CREATE TABLE IF NOT EXISTS 
                                                TankMix_Info(
                                                    TankMix_ID INT NOT NULL,
                                                    Product_ID INT NOT NULL,
                                                    p_Rate real NOT NULL,
                                                    p_Units text NOT NULL,
                                                    Class_Type text NOT NULL,
                                                    PRIMARY KEY (TankMix_ID),
                                                    FOREIGN KEY (Product_ID)
                                                        REFERENCES Product_Info (Product_ID)
                                                )"""
    return create_Tank_Mix_Info_table_query

def createWeatherInfo_tbl():
    create_Weather_Info_table_query = """CREATE TABLE IF NOT EXISTS 
                                                Weather_Info(
                                                    Weather_ID INT NOT NULL,
                                                    Wind_Speed real NOT NULL,
                                                    Wind_Direction text NOT NULL,
                                                    Humidity real NOT NULL,
                                                    Dew_Point real NOT NULL,
                                                    Temperature real NOT NULL,
                                                    PRIMARY KEY (Weather_ID)
                                                )"""
    return create_Weather_Info_table_query

def createProductInfo_tbl():
    create_Product_Info_table_query = """CREATE TABLE IF NOT EXISTS 
                                                Product_Info(
                                                    Product_ID INT NOT NULL,
                                                    Product text NOT NULL,
                                                    EPA_Num text NOT NULL,
                                                    REI text NOT NULL,
                                                    SOA text NOT NULL,
                                                    Chem_Family text NOT NULL,
                                                    RUP INT NOT NULL,
                                                    Pest_Type text NOT NULL,
                                                    Prod_Format text NOT NULL,
                                                    Status text NOT NULL,
                                                    PRIMARY KEY (Product_ID)
                                                )"""
    return create_Product_Info_table_query


#   ************************************************************    
#   ** Field Viweing Permissions Database Structure ** 
#   ************************************************************

#   ************************************************************
#   * Create Main Table *
#   ************************************************************
def createFieldAccess_tbl():
    create_Field_Access_table_query = """CREATE TABLE IF NOT EXISTS 
                                                Field_Access(
                                                    ID INT NOT NULL,
                                                    User_ID INT NOT NULL,
                                                    Farm_ID INT NOT NULL,
                                                    Field_ID INT NOT NULL,
                                                    Permission INT NOT NULL,
                                                    PRIMARY KEY (ID),
                                                    FOREIGN KEY (User_ID) 
                                                        REFERENCES User_Info(User_ID),
                                                    FOREIGN KEY (Farm_ID) 
                                                        REFERENCES Farm_Info(Farm_ID),
                                                    FOREIGN KEY (Field_ID) 
                                                        REFERENCES Field_Info(Field_ID)
                                                )"""
    return create_Field_Access_table_query

#   ************************************************************    
#   * Create Relational Tables *
#   ************************************************************
def createFarmInfo_tbl():
    create_Farm_Info_table_query = """CREATE TABLE IF NOT EXISTS 
                                            Farm_Info(
                                                Farm_ID INT NOT NULL,
                                                Owner_ID INT NOT NULL,
                                                Farm_Name text NOT NULL,
                                                Status text NOT NULL,
                                                PRIMARY KEY (Farm_ID),
                                                FOREIGN KEY (Owner_ID) 
                                                    REFERENCES Owner_Info(Owner_ID)
                                            )"""
    return create_Farm_Info_table_query

def createFieldInfo_tbl():
    create_Field_Info_table_query = """CREATE TABLE IF NOT EXISTS 
                                            Field_Info(
                                                Field_ID INT NOT NULL,
                                                Farm_ID INT NOT NULL,
                                                Field_Name text NOT NULL,
                                                Latitude real NOT NULL,
                                                Longitude real NOT NULL,
                                                Boundary_ID INT NOT NULL,
                                                Status text NOT NULL,
                                                PRIMARY KEY (Field_ID),
                                                FOREIGN KEY (Farm_ID) 
                                                    REFERENCES Farm_Info(Farm_ID)
                                            )"""
    return create_Field_Info_table_query
    
def createInstructorInfo_tbl():
    create_Instructor_Info_table_query = """CREATE TABLE IF NOT EXISTS 
                                                Instructor_Info(
                                                    Instructor_ID INT NOT NULL,
                                                    First_Name text NOT NULL,
                                                    Last_Name text NOT NULL,
                                                    Contact_Num text NOT NULL,
                                                    Address text NOT NULL,
                                                    Email text NOT NULL,
                                                    Cert_Date NOT NULL,
                                                    Cert_Exp NOT NULL,
                                                    PRIMARY KEY (Instructor_ID)
                                                )"""
    return create_Instructor_Info_table_query

            # NOTE: Owner_Info Table see 'Main Application Event Database 
            #       Structure' 
            # NOTE: User_Info Table see ' User Information Database Structure' 


#   ************************************************************
#   ** User Information Database Structure ** 
#   ************************************************************
    
#   ************************************************************
#   * Create Main Table *
#   ************************************************************
def createUserInfo_tbl():
    create_User_Info_table_query = """CREATE TABLE IF NOT EXISTS 
                                            User_Info(
                                                User_ID INT NOT NULL,
                                                Owner_ID INT NOT NULL,
                                                First_Name text NOT NULL,
                                                Last_Name text NOT NULL,
                                                Email text NOT NULL,
                                                Username text NOT NULL,
                                                Password text NOT NULL,
                                                Access_Type text NOT NULL,
                                                User_Type text NOT NULL,
                                                Training_Date text NOT NULL,
                                                Instructor_ID INT NOT NULL,
                                                Status text NOT NULL,
                                                PRIMARY KEY (User_ID),
                                                FOREIGN KEY (Owner_ID) 
                                                    REFERENCES Owner_Info(Owner_ID),
                                                FOREIGN KEY (Instructor_ID) 
                                                    REFERENCES Instructor_Info(Instructor_ID)
                                            )"""
    return create_User_Info_table_query

#   ************************************************************    
#   * Relational Table References *
#   ************************************************************
            # NOTE: Owner_Info Table see 'Main Application Event Database 
            #       Structure' 
            # NOTE: Instructor_Info Table see 'Field Viewing Permissions 
            #       Database Structure' 



#   ************************************************************
#   *** Manipulate 'ssAppData' Database Tables ***
#   * Description - Drives all procedures for the ssAppData
#                   database.
#   ************************************************************

        
#   ************************************************************
#   ** Insert New Application Information **
#   ************************************************************
def insert_Application():
    
    insert_Application_query = """INSERT INTO 
                                    Main_db(
                                        ID,
                                        Owner_ID,
                                        Farm,
                                        Field,
                                        Applicator_ID,
                                        Date,
                                        Tank_Mix_ID,
                                        App_Type,
                                        Equipment_Name,
                                        Weather_ID
                                    )
                                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    return insert_Application_query
    
def insert_Farm():
    insert_Farm_query = """INSERT INTO
                            Farm_Info(
                                Farm_ID,
                                Owner_ID,
                                Farm_Name,
                                Status
                            )
                            VALUES (%s,%s,%s,%s)"""
    return insert_Farm_query

def insert_Field():
    insert_Field_query = """INSERT INTO
                            Field_Info(
                                Field_ID,
                                Farm_ID,
                                Field_Name,
                                Latitude,
                                Longitude,
                                Boundary_ID,
                                Status
                            )
                            VALUES (%s,%s,%s,%s,%s,%s,%s)"""
    return insert_Field_query
    
def insert_Applicator():
    insert_Applicator_query = """INSERT INTO
                                    Applicator_Info(
                                        Applicator_ID,
                                        First_Name,
                                        Last_Name,
                                        License_Type,
                                        Licensed_Categories,
                                        License
                                    )
                                    VALUES (%s,%s,%s,%s,%s,%s)"""
    return insert_Applicator_query

def insert_Product():
    insert_Product_query = """INSERT INTO
                                Product_Info(
                                    Product_ID,
                                    Product,
                                    EPA_Num,
                                    REI,
                                    SOA,
                                    Chem_Family,
                                    RUP INT,
                                    Pest_Type,
                                    Prod_Format,
                                    Status
                                )
                                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""    
    return insert_Product_query
 



#   ************************************************************
#   **** 'ssUser_Info' DATABASE PROCEDURES ****
#   ************************************************************ 
    
    
    
#   ************************************************************
#   *** MAIN 'ssUser_Info' EVENT DATABASE STRUCTURE ***
#   ************************************************************


#   ************************************************************
#   ** Create Database Tables **
#   ************************************************************

#   ************************************************************
#   * Create Main Table *
#   ************************************************************
def create_UserInfo_tbl():
    create_UserInfo_tbl_query = """CREATE TABLE IF NOT EXISTS 
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
#   * Create Relational Tables *
#   ************************************************************
def create_OrgInfo_tbl():
    create_OrgInfo_table_query = """CREATE TABLE IF NOT EXISTS
                                            Org_Info(
                                                Org_ID INT NOT NULL AUTO_INCREMENT,
                                                Org_Name text NOT NULL,
                                                User_ID INT NOT NULL,
                                                JD_Org_ID INT NOT NULL,
                                                JD_Org_Name text NOT NULL,
                                                JD_Access_lvl text NOT NULL,
                                                JD_TokenID text NOT NULL,
                                                JD_AccessToken text NOT NULL,
                                                JD_RefreshToken text NOT NULL,
                                                JD_TokenExpiration text NOT NULL,
                                                Status text NOT NULL,
                                                PRIMARY KEY (Org_ID),
                                                FOREIGN KEY (User_ID)
                                                    REFERENCES User_Info(User_ID)
                                            )"""
    return create_OrgInfo_table_query
    
def create_FarmInfo_tbl():
    create_FarmInfo_table_query = """CREATE TABLE IF NOT EXISTS 
                                            Farm_Info(
                                                Farm_ID INT NOT NULL AUTO_INCREMENT,
                                                Farm_Name text NOT NULL,
                                                Org_ID INT NOT NULL,                                         
                                                PRIMARY KEY (Farm_ID),
                                                FOREIGN KEY (Org_ID)
                                                    REFERENCES Org_Info(Org_ID)
                                            )"""
    return create_FarmInfo_table_query

def create_FieldInfo_tbl():
    create_FieldInfo_table_query = """CREATE TABLE IF NOT EXISTS 
                                            Field_Info(
                                                Field_ID INT NOT NULL AUTO_INCREMENT,
                                                Field_Name text NOT NULL,
                                                Farm_ID INT NOT NULL,
                                                PRIMARY KEY (Field_ID),
                                                FOREIGN KEY (Farm_ID)
                                                    REFERENCES Farm_Info(Farm_ID)
                                            )"""
    return create_FieldInfo_table_query



#   ************************************************************
#   *** MANIPULATE 'ssUser_Info' DATABASE TABLE DATA ***
#   * Description - Drives all procedures succeeding the 
#                   execute_Instance_query, for the 
#                   ssUser_Info database.
#   ************************************************************
def execute_Instance_query(connection, sql_query, info):
    
    try:
        if connection:
            if info:
                with connection.cursor() as cursor:
                    cursor.executemany(sql_query,info)
                    
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
#   ** Insert Table Information **
#   ************************************************************
def insert_User():
    insert_User_query = """INSERT INTO 
                                    User_Info(
                                        UserName,
                                        Email,
                                        Password,
                                        Status                                        
                                    )
                                    VALUES (%s,%s,%s,%s);"""
    return insert_User_query
    
def insert_Org():
    insert_Org_query = """INSERT INTO
                                    Org_Info(
                                        Org_Name,
                                        User_ID,
                                        JD_Org_ID,
                                        JD_Org_Name,
                                        JD_Access_lvl,
                                        JD_TokenID,
                                        JD_AccessToken,
                                        JD_RefreshToken,
                                        JD_TokenExpiration,
                                        Status
                                    )
                                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"""
    return insert_Org_query    

def insert_Farm():
    insert_Farm_query = """INSERT INTO
                            Farm_Info(
                                Farm_Name,
                                Org_ID
                            )
                            VALUES (%s,%s);"""
    return insert_Farm_query

def insert_Field():
    insert_Field_query = """INSERT INTO
                            Field_Info(                                                               
                                Field_Name,
                                Farm_ID
                            )
                            VALUES (%s,%s);"""
    return insert_Field_query
    
    
#   ************************************************************    
#   ** Update Table Information **
#   ************************************************************
def update_JDAccess()
    update_JDAccess_query = """UPDATE Org_Info SET
                                        JD_Access_lvl = %s,
                                        JD_TokenID = %s,
                                        JD_AccessToken = %s,
                                        JD_RefreshToken = %s,
                                        JD_TokenExpiration = %s
                                    WHERE Org_ID = %s"""
    # call parameter Structure - query, values = (JD_Access_lvl, JD_TokenID, JD_AccessToken, JD_RefreshToken, JD_TokenExpiration, Org_ID)
    return update_JDAccess_query
    
def update_UserPassword_byID()
    update_UserPassword_byID_query = """UPDATE User_Info SET Password = %s WHERE User_ID = %s"""
    return update_UserPassword_byID_query

def update_UserPassword_byUserName()
    update_UserPassword_byUserName_query = """UPDATE User_Info SET Password = %s WHERE UserName = %s"""
    return update_UserPassword_byUserName_query

def update_UserPassword_byEmail()
    update_UserPassword_byEmail_query = """UPDATE User_Info SET Password = %s WHERE Email = %s"""
    return update_UserPassword_byEmail_query

def update_UserStatus ()
    update_UserStatus_query = """UPDATE User_Info SET Status = %s WHERE User_ID = %s"""
    return update_UserStatus_query

def update_OrgName()
    update_OrgName_query = """UPDATE Org_Info SET Org_Name = %s WHERE Org_ID = %s"""
    return update_OrgName_query

def update_JDOrgName()
    update_JDOrgName_query = """ UPDATE Org_Info SET JD_Org_Name = %s WHERE Org_ID = %s"""
    return update_JDOrgName_query
    
def update_FarmName()
    update_FarmName_query = """UPDATE Farm_Info SET Farm_Name = %s WHERE Farm_ID = %s"""
    return update_FarmName_query
    
def update_FieldName()
    update_FieldName_query = """UPDATE Field_Info SET Field_Name = %s WHERE Field_ID = %s"""
    return update_FieldName_query

   
#   ************************************************************
#   ** Delete Table Information **
#   ************************************************************
def delete_User()
    delete_User_query = """DELETE FROM User_Info WHERE User_ID = %s"""
    return delete_User_query

def delete_Org()
    delete_Org_query = """DELETE FROM Org_Info WHERE Org_ID = %s"""
    return delete_Org_query
    
 def delete_Farm()
    delete_Farm_query = """DELETE FROM Farm_Info WHERE Farm_ID = %s"""
    return delete_Farm_query 
    
def delete_Field()
    delete_Field_query = """DELETE FROM Field_Info WHERE Field_ID = %s"""
    return delete_Field_query
    
    
#   ************************************************************
#   ** Query Table Information **
#   ************************************************************

#   ************************************************************
#   * JD Information *
#   ************************************************************
def select_JDAccessToken()
    select_JDAccessToken_query = """SELECT JD_AccessToken FROM Org_Info WHERE Org_ID = %s"""
    return select_JDAccessToken_query

def select_JDRefreshToken()
    select_JDRefreshToken_query = """SELECT JD_RefreshToken FROM Org_Info WHERE Org_ID = %s"""
    return select_JDRefreshToken_query
 
def select_JDTokenExpiration()
    select_JDTokenExpiration_query = """SELECT JD_TokenExpiration FROM Org_Info WHERE Org_ID = %s"""
    return select_JDTokenExpiration_query

#   ************************************************************
#   * Specific Information Sets *
#   ************************************************************
def select_UserID()
    select_UserID_query = """SELECT User_ID FROM User_Info WHERE Password = %s AND Email = %s"""
    return select_UserID_query

def select_UserName()
    select_UserName_query = """SELECT UserName FROM User_Info WHERE User_ID = %s"""
    return select_UserName_query
    
def select_UserStatus()
    select_UserStatus_query = """SELECT Status FROM User_Info WHERE User_ID = %s"""
    return select_UserStatus_query

def select_OrgID()
    select_OrgID_query = """SELECT Org_ID FROM Org_Info WHERE User_ID = %s"""
    return select_OrgID_query

def select_FarmID()
    select_FarmID_query = """SELECT Farm_ID FROM Farm_Info WHERE Org_ID =%s"""
    return select_FarmID_query
    
def select_FieldID()
    select_FieldID_query = """SELECT Field_ID FROM Field_Info WHERE Farm_ID = %s"""
    return select_FieldID_query
    
    
#   ************************************************************
#   * Entire Information Sets *
#   ************************************************************
def select_OrgInfo()
    select_OrgInfo_query = """SELECT * FROM Org_Info WHERE User_ID = %s"""
    return select_OrgInfo_query

def select_FarmInfo()
    select_FarmInfo_query = """SELECT * FROM Farm_Info WHERE Org_ID = %s"""
    return select_FarmInfo_query
    
def select_FieldInfo()
    select_FieldInfo_query = """SELECT * FROM Field_Info WHERE Farm_ID = %s"""
    return select_FieldInfo_query