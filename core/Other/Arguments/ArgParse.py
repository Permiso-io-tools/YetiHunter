import argparse

CONFIGFILE = {
    "USER": "",
    "AUTHENTICATION_METHOD": "",
    "WAREHOUSE": "",
    "ACCOUNT": "",
    "DATABASE": "",
    "SCHEMA": "",
    "OUTPUTDIR": None,
    "PASSWORD": None
}

def parseArgs():
    parser = argparse.ArgumentParser(
        prog='YettiHunter',
        description='Permiso Security has created a tool to query snowflake environments for evidence of compromise, based on indicators from Permiso and the community.',
    )

    parser.add_argument('-u', '--user', help="The Snowflake user to authenticate as. Even if the authentication is SSO, the email of the identity authenticating should be added.")
    parser.add_argument('-p', '--password', help="This field is not required if the authentication is SSO, but required if the authentication is USERPASS. If needed and the field is empty, an imput will popup to ask for the password.")
    parser.add_argument('-w', '--warehouse', help="The Snowflake warehouse to connect to.")
    parser.add_argument('-a', '--account', help="The Snowflake Account to connect to. It should be in the format of <organization>-<account>")
    parser.add_argument('-d', '--database', help="The database name to connect to.")
    parser.add_argument('-s', '--schema', help="The name of the schema inside the database. This can be empty.")
    parser.add_argument('-am', '--authentication-method', choices=['SSO', 'USERPASS'])
    parser.add_argument('-cf', '--config-file-path', help="If a config file is used, this option will have the path of the config file. No other flag is needed besides this.")
    parser.add_argument('-gcf', '--generate-config-file', action="store_true", help="If put, the tool will create an empty config file that can be filled by the user. The fields with null value can be left as null as they are not required.")
    parser.add_argument('-o', '--output-directory', help="The directory inside ./output/, where the query output files will be saved in.")

    return parser.parse_args()

