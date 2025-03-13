import os
import requests
import mysql.connector
import hmac
import json
from base64 import b64encode
from datetime import datetime


def build_cdms_authorization(schemeless_url, username, password):
    current_datetime = datetime.now()
    timestamp = '{0:%d%m%Y%H%M%S}'.format(current_datetime)
    signature = hmac.new(password.encode(),
                         '{0}{1}'.format(schemeless_url, timestamp).encode(),
                         'md5').digest()
    return '{0}:{1}:{2}'.format(username, b64encode(signature).decode(), timestamp)


def get_pid_list(username, password):
    schemeless_url = 'test.cdms.net/LabelSvc/API/LabelData/?updatedAfter=1970-01-01'

    headers = {
        'Authorization': build_cdms_authorization(schemeless_url, username, password),
    }
    response = requests.get('http://{0}'.format(schemeless_url), headers=headers)

    pid_and_names = {}
    data = response.json()
    print(len(data))
    for pesticide in data:
        pid = pesticide.get('PId')
        name = pesticide.get('Code')
        pid_and_names[pid] = name

    return (pid_and_names)



def get_rei_times(pid_and_names, username, password):
    rei_times = {}
    for pid, name in pid_and_names.items():
        schemeless_url = 'test.cdms.net/LabelSvc/API/LabelData/{0}/Wps/?dataSrc=M'.format(pid)
        headers = {
            'Authorization': build_cdms_authorization(schemeless_url, username, password),
        }
        response = requests.get('http://{0}'.format(schemeless_url), headers=headers)
        response_json = response.json()
        wps_data = response_json.get('WPS')
        if wps_data is not None:
            rei = wps_data.get('rei')
            rei_times[name] = rei
        else:
            rei_times[name] = "No WPS Data"
    return rei_times

def insert_rei_time_into_db(names_and_rei):
    try:
        connection = mysql.connector.connect(
            host="208.109.60.84",
            user="ssAppData_Admin",
            password="UNLSpraySafely1*",
            database="ssProducts"
        )
        print(connection)
    except mysql.connector.Error as error:
        print("Error while connecting to the database: ", error)
        return

    try:
        cursor = connection.cursor()
        cursor.execute("LOCK TABLES Product WRITE")

        for product_name, rei_time in names_and_rei.items():
            insert_query = "INSERT INTO Product (product_name, rei_time) VALUES (%s, %s)"
            insert_values = (product_name, rei_time)
            cursor.execute(insert_query, insert_values)

        connection.commit()

        print(cursor.rowcount, "record(s) inserted successfully into Product table")
    except mysql.connector.Error as error:
        print("Error while inserting data into Product table: ", error)
        connection.rollback()
    finally:
        cursor.execute("UNLOCK TABLES")
        cursor.close()
        connection.close()
        print("MySQL connection is closed")


def main():
    username = 'UNLTestWS'
    password = 'F7HU~wPcMP96H*'
    try:
        pid_and_names = get_pid_list(username, password)
    except requests.exceptions.RequestException as e:
        print("An error occurred while making the get_pid_list request: {0}".format(e))
        return

    try:
        names_and_rei = get_rei_times(pid_and_names, username, password)
    except requests.exceptions.RequestException as e:
        print("An error occurred while making the get_rei_times request: {0}".format(e))
        return

    try:
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'updated_names_and_rei.txt')
        with open(file_path, 'w') as f:
            f.write(str(names_and_rei))
            print("Success")
    except Exception as e:
        print("An error occurred while writing to the file: {0}".format(e))
        return

    insert_rei_times_into_db(names_and_rei)

if __name__ == '__main__':
    main()