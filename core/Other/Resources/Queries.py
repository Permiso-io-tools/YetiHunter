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
        malIPJSON["description"] = "Snowflake accessed from known malicious IPs"
        malIPJSON["query"] = malipquery
        queryJSON.append(malIPJSON)
    return queryJSON

QUERIES = generateMaliciousIPQuery()

