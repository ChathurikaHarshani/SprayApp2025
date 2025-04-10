# import os
# import requests
# import mysql.connector
# import hmac
# import json
# from base64 import b64encode
# from datetime import datetime


# def build_cdms_authorization(schemeless_url, username, password):
#     current_datetime = datetime.now()
#     timestamp = '{0:%d%m%Y%H%M%S}'.format(current_datetime)
#     signature = hmac.new(password.encode(),
#                          '{0}{1}'.format(schemeless_url, timestamp).encode(),
#                          'md5').digest()
#     return '{0}:{1}:{2}'.format(username, b64encode(signature).decode(), timestamp)


# def get_pid_list(username, password):
#     #schemeless_url = 'test.cdms.net/LabelSvc/API/LabelData/?updatedAfter=1970-01-01'
#     schemeless_url = 'test.cdms.net/LabelSvc/API/LabelData/?updatedAfter=1970-01-01&listType=Combined'


#     headers = {
#         'Authorization': build_cdms_authorization(schemeless_url, username, password),
#     }
#     response = requests.get('http://{0}'.format(schemeless_url), headers=headers)

#     pid_and_names = {}
#     data = response.json()
#     print(len(data))
#     for pesticide in data:
#         pid = pesticide.get('PId')
#         name = pesticide.get('Code')
#         pid_and_names[pid] = name

#     return (pid_and_names)




# import re

# def parse_rei(text):
#     text = text.upper().strip()
#     hours_match = re.search(r'REI\s*=\s*(\d+)\s*(HRS|HOURS)?', text)
#     if not hours_match:
#         hours_match = re.search(r'(\d+)\s*(HRS|HOURS)', text)

#     if hours_match:
#         return int(hours_match.group(1)), None, 0  # (REI_Time_Hours, Description, Is_Irregular)
#     else:
#         return -1, text, 1  # If it's irregular, return full description










# def get_rei_times(pid_and_names, username, password):
#     rei_times = {}
#     for pid, name in pid_and_names.items():
#         schemeless_url = 'test.cdms.net/LabelSvc/API/LabelData/{0}/Wps/?dataSrc=M'.format(pid)
#         headers = {
#             'Authorization': build_cdms_authorization(schemeless_url, username, password),
#         }
#         response = requests.get('http://{0}'.format(schemeless_url), headers=headers)
#         response_json = response.json()
#         wps_data = response_json.get('WPS')
#         if wps_data is not None:
#             #rei = wps_data.get('rei')
#             #rei_times[name] = rei

#             rei_raw = wps_data.get('rei', '')
#             rei_hours, rei_desc, is_irregular = parse_rei(rei_raw)
#             rei_times[name] = {
#             "REI_Time_Hours": rei_hours,
#             "REI_Description": rei_desc,
#             "Is_Irregular": is_irregular
# }

#         else:
#             rei_times[name] = "No WPS Data"
#     return rei_times

# def insert_rei_time_into_db(names_and_rei):
#     try:
#         connection = mysql.connector.connect(
#             # host = "132.148.180.201",
#             # user="ssAppData_Admin",
#             # password="UNLSpraySafely1*",
#             # database="ssProducts"
#             host = "132.148.180.201",
#             user = "ssUser_Admin",
#             password = "UNLSpraySafely1*",
#             database = "ssUser_Info",
#         )
#         print(connection)
#     except mysql.connector.Error as error:
#         print("Error while connecting to the database: ", error)
#         return

#     try:
#         cursor = connection.cursor()
#         cursor.execute("LOCK TABLES Product WRITE")

#         # for product_name, rei_time in names_and_rei.items():
#         #     insert_query = "INSERT INTO Product (product_name, rei_time) VALUES (%s, %s)"
#         #     insert_values = (product_name, rei_time)

#         for product_name, rei_data in names_and_rei.items():
#             rei_hours = rei_data["REI_Time_Hours"]
#             rei_desc = rei_data["REI_Description"]
#             is_irregular = rei_data["Is_Irregular"]

#             insert_query = """
#                 INSERT INTO Product_Info (Product_Name, REI_Time_Hours, REI_Description, Is_Irregular)
#                 VALUES (%s, %s, %s, %s)
#             """
#             insert_values = (product_name, rei_hours, rei_desc, is_irregular)

#             cursor.execute(insert_query, insert_values)

#         connection.commit()

#         print(cursor.rowcount, "record(s) inserted successfully into Product table")
#     except mysql.connector.Error as error:
#         print("Error while inserting data into Product table: ", error)
#         connection.rollback()
#     finally:
#         cursor.execute("UNLOCK TABLES")
#         cursor.close()
#         connection.close()
#         print("MySQL connection is closed")






# def main():
#     username = 'UNLTestWS'
#     password = 'F7HU~wPcMP96H*'
#     try:
#         pid_and_names = get_pid_list(username, password)
#     except requests.exceptions.RequestException as e:
#         print("An error occurred while making the get_pid_list request: {0}".format(e))
#         return

#     try:
#         names_and_rei = get_rei_times(pid_and_names, username, password)

#         # names_and_rei["TEST_PRODUCT_REI"] = {
#         #         "REI_Time_Hours": 99,
#         #         "REI_Description": "Test Insert",
#         #         "Is_Irregular": 1
#         #     }




#     except requests.exceptions.RequestException as e:
#         print("An error occurred while making the get_rei_times request: {0}".format(e))
#         return

#     try:
#         file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'updated_names_and_rei.txt')
#         with open(file_path, 'w') as f:
#             f.write(str(names_and_rei))
#             print("Success")
#     except Exception as e:
#         print("An error occurred while writing to the file: {0}".format(e))
#         return

#     #insert_rei_times_into_db(names_and_rei)
#     insert_rei_time_into_db(names_and_rei)

# if __name__ == '__main__':
#     main()












import os
import requests
import mysql.connector
import hmac
import json
from base64 import b64encode
from datetime import datetime
import re


def build_cdms_authorization(schemeless_url, username, password):
    current_datetime = datetime.utcnow()
    timestamp = '{0:%d%m%Y%H%M%S}'.format(current_datetime)
    signature = hmac.new(password.encode(),
                         '{0}{1}'.format(schemeless_url, timestamp).encode(),
                         'md5').digest()
    return '{0}:{1}:{2}'.format(username, b64encode(signature).decode(), timestamp)


# def parse_rei(text):
#     text = text.upper().strip()
#     hours_match = re.search(r'REI\s*=\s*(\d+)\s*(HRS|HOURS)?', text)
#     if not hours_match:
#         hours_match = re.search(r'(\d+)\s*(HRS|HOURS)', text)

#     if hours_match:
#         return int(hours_match.group(1)), None, 0
#     else:
#         return -1, text, 1



def parse_rei(text):
    if not text:
        return -1, "", 1  # Treat missing REI as irregular

    text = text.upper().strip()
    hours_match = re.search(r'REI\s*=\s*(\d+)\s*(HRS|HOURS)?', text)
    if not hours_match:
        hours_match = re.search(r'(\d+)\s*(HRS|HOURS)', text)

    if hours_match:
        return int(hours_match.group(1)), None, 0
    else:
        return -1, text, 1


def get_pid_list(username, password):
    #schemeless_url = 'test.cdms.net/LabelSvc/API/LabelData/?updatedAfter=1970-01-01'
    schemeless_url = 'test.cdms.net/LabelSvc/API/LabelData/?updatedAfter=1970-01-01&listType=Combined'
    headers = {
        'Authorization': build_cdms_authorization(schemeless_url, username, password),
    }
    response = requests.get(f'http://{schemeless_url}', headers=headers)
    try:
        data = response.json()
    except json.JSONDecodeError:
        print("❌ Failed to parse product list JSON.")
        print("Response:", response.status_code, response.text[:300])
        return {}

    pid_and_names = {}
    for pesticide in data:
        if pesticide.get("deleted"):
            continue
        pid = pesticide.get('PId')
        name = pesticide.get('Name')
        if pid and name:
            pid_and_names[pid] = name
    return pid_and_names


def get_rei_times(pid_and_names, username, password):
    rei_times = {}
    for pid, name in pid_and_names.items():
        schemeless_url = f'test.cdms.net/LabelSvc/API/LabelData/{pid}/Wps/?dataSrc=M'
        headers = {
            'Authorization': build_cdms_authorization(schemeless_url, username, password),
        }
        response = requests.get(f'http://{schemeless_url}', headers=headers)
        try:
            data = response.json()
        except json.JSONDecodeError:
            print(f"⚠️ Failed to parse REI for {name} (PID: {pid})")
            continue

        wps_data = data.get('WPS', {})
        rei_raw = wps_data.get('rei', '')
        rei_hours, rei_desc, is_irregular = parse_rei(rei_raw)

        rei_times[name] = {
            "REI_Time_Hours": rei_hours,
            "REI_Description": rei_desc,
            "Is_Irregular": is_irregular
        }
    return rei_times


# def insert_rei_time_into_db(names_and_rei):
#     connection = mysql.connector.connect(
#         # host='localhost',
#         # database='ssUser_Info',
#         # user='root',
#         # password='password'
#         host = "132.148.180.201",
#         #host="129.93.161.225",
#         user = "ssUser_Admin",
#         password = "UNLSpraySafely1*",
#         database = "ssUser_Info",
#     )
#     cursor = connection.cursor()

#     for product_name, rei_data in names_and_rei.items():
#         rei_hours = rei_data["REI_Time_Hours"]
#         rei_desc = rei_data["REI_Description"]
#         is_irregular = rei_data["Is_Irregular"]

#         # insert_query = '''
#         #     INSERT INTO Product_Info (Product_Name, REI_Time_Hours, REI_Description, Is_Irregular)
#         #     VALUES (%s, %s, %s, %s)
#         # '''

#         insert_query = '''
#                 INSERT INTO Product_Info (Product_Name, REI_Time_Hours, REI_Description, Is_Irregular)
#                 VALUES (%s, %s, %s, %s)
#                 ON DUPLICATE KEY UPDATE
#                     REI_Time_Hours = VALUES(REI_Time_Hours),
#                     REI_Description = VALUES(REI_Description),
#                     Is_Irregular = VALUES(Is_Irregular)
#         '''

#         insert_values = (product_name, rei_hours, rei_desc, is_irregular)
#         cursor.execute(insert_query, insert_values)

#     connection.commit()
#     print(cursor.rowcount, "record(s) inserted successfully into Product_Info table.")
#     cursor.close()
#     connection.close()

def insert_rei_time_into_db(names_and_rei):
    connection = mysql.connector.connect(
        host = "132.148.180.201",
        user = "ssUser_Admin",
        password = "UNLSpraySafely1*",
        database = "ssUser_Info",
    )
    cursor = connection.cursor()

    for product_name, rei_data in names_and_rei.items():
        rei_hours = rei_data["REI_Time_Hours"]
        rei_desc = rei_data["REI_Description"]or ""
        is_irregular = rei_data["Is_Irregular"]

        insert_query = '''
            INSERT INTO Product_Info (Product_Name, REI_Time_Hours, REI_Description, Is_Irregular)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                REI_Time_Hours = VALUES(REI_Time_Hours),
                REI_Description = VALUES(REI_Description),
                Is_Irregular = VALUES(Is_Irregular)
        '''
        insert_values = (product_name, rei_hours, rei_desc, is_irregular)
        cursor.execute(insert_query, insert_values)

    connection.commit()
    print(cursor.rowcount, "record(s) inserted or updated successfully into Product_Info table.")
    cursor.close()
    connection.close()



def main():
    username = 'UNLTestWS'
    password = 'F7HU~wPcMP96H*'

    if not username or not password:
        print("CDMS_USERNAME and CDMS_PASSWORD must be set as environment variables.")
        return

    pid_and_names = get_pid_list(username, password)
    if not pid_and_names:
        print("❌ No products found.")
        return

    names_and_rei = get_rei_times(pid_and_names, username, password)
    insert_rei_time_into_db(names_and_rei)


if __name__ == '__main__':
    main()
