import json

import os


def generateMaliciousIPQuery():
    with open("./queries/queries.json") as malipfile:
        queryJSON = json.load(malipfile)

    if os.path.exists("./queries/known_bad_ips"):
        with open("./queries/known_bad_ips") as malipfile:
            KNOWN_BAD_IPS = malipfile.readlines()

        malipquery = "SELECT * FROM snowflake.account_usage.login_history WHERE client_ip IN ("

        for ip in KNOWN_BAD_IPS:
            if ip == '\n':
                continue
            else:
                malipquery += f"'{ip.strip()}',"
        malipquery = malipquery[:-1]
        malipquery += ") ORDER BY event_timestamp;"
        malIPJSON = {}
        malIPJSON["name"] = "login_from_malicious_ips"
        malIPJSON["description"] = "Snowflake accessed from known malicious IPs with read accounts"
        malIPJSON["query"] = malipquery
        queryJSON.append(malIPJSON)

        # Read AccountUsage

        malipqueryread = "SELECT * FROM snowflake.reader_account_usage.login_history WHERE client_ip IN ("
        for ip in KNOWN_BAD_IPS:
            if ip == '\n':
                continue
            else:
                malipqueryread += f"'{ip.strip()}',"
        malipqueryread = malipqueryread[:-1]
        malipqueryread += ") ORDER BY event_timestamp;"
        malIPJSONRead = {}
        malIPJSONRead["name"] = "login_from_malicious_ips_on_reader_account"
        malIPJSONRead["description"] = "Snowflake accessed from known malicious IPs"
        malIPJSONRead["query"] = malipqueryread
        queryJSON.append(malIPJSONRead)
    return queryJSON

QUERIES = generateMaliciousIPQuery()



