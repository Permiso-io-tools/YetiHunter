import json
import os
from getpass import getpass

from core.Authentication.Authentication import Authentication
from core.Other.Arguments.ArgParse import parseArgs, CONFIGFILE
from core.Other.PrintOutput.PrintOutput import printOutput
from core.Other.Resources.OutputDump import dumpCSV
from core.QueryActivity.QueryActivities import Query
from core.Other.Resources.Queries import QUERIES
from core.Other.Arguments.Banner import printBanner
args = parseArgs()

printBanner()

if not os.path.exists("./configfiles"):
    os.mkdir("./configfiles")

if not os.path.exists("./output"):
    os.mkdir("./output")

if args.generate_config_file:
    with open("./configfiles/config.conf", 'w') as configfile:
        json.dump(CONFIGFILE, configfile, indent=4, default=str)
    printOutput("Successfully created config file ./configfiles/config.conf", "success")
    configfile.close()
    exit()

if args.config_file_path is not None:
    with open(args.config_file_path, 'r') as toolconfigfile:
        configJson = json.load(toolconfigfile)
        toolconfigfile.close()

    check = 0

    user = configJson['USER']
    authentication_method = configJson['AUTHENTICATION_METHOD']
    warehouse = configJson['WAREHOUSE']
    account = configJson['ACCOUNT']
    database = configJson['DATABASE']
    outputdir = configJson['OUTPUTDIR']
    schema = configJson['SCHEMA']
    password = configJson['PASSWORD']

    if user is None or user == "":
        printOutput("User is a required option. Please provide a user on USER field of the config file", "failure")
        check = 1

    if authentication_method is None or authentication_method == "":
        printOutput("Authentication method is a required option. Please provide an Authentication Method on AUTHENTICATION_METHOD field of the config file", "failure")
        check = 1

    if warehouse is None or warehouse == "":
        printOutput("Warehouse is a required option. Please provide a warehouse on WAREHOUSE field of the config file", "failure")
        check = 1

    if account is None or account == "":
        printOutput("Account is a required option. Please provide an account on ACCOUNT field of the config file", "failure")
        check = 1

    if database is None or database == "":
        printOutput("Database is a required option. Please provide a database on DATABASE field of the config file", "failure")
        check = 1

    if outputdir is None or outputdir == "":
        printOutput(f"Output directory is a required option. Put the output directory name on OUTPUTDIR field of the config file", "failure")
        check = 1

    if check != 0:
        exit()

else:
    user = args.user
    authentication_method = args.authentication_method
    warehouse = args.warehouse
    account = args.account
    database = args.database
    schema = args.schema
    outputdir = args.output_directory
    password = args.password

    check = 0
    if user is None or user == "":
        printOutput("User is a required option. Please provide a user using -u flag", "failure")
        check = 1


    if authentication_method is None or authentication_method == "":
        printOutput("Authentication method is a required option. Please provide an Authentication Method using -am flag", "failure")
        check = 1


    if warehouse is None or warehouse == "":
        printOutput("Warehouse is a required option. Please provide a warehouse using -w flag", "failure")
        check = 1


    if account is None or account == "":
        printOutput("Account is a required option. Please provide an account using -a flag", "failure")
        check = 1


    if database is None or database == "":
        printOutput("Database is a required option. Please provide a database using -d flag", "failure")
        check = 1


    if outputdir is None or outputdir == "":
        printOutput(f"Output directory is a required option. Put the output directory name using -o flag", "failure")
        check = 1

    if check != 0:
        exit()

if os.path.exists(f'./output/{outputdir}'):
    printOutput(f"Output directory ./output/{outputdir} exists. put a new name", "failure")
    exit()
else:
    os.mkdir(f"./output/{outputdir}")

if authentication_method == "USERPASS":
    if password is None:
        password = getpass()

    authenticationObj = Authentication(
        warehouse=warehouse,
        database=database,
        user=user,
        password=password,
        account=account,
        schema=schema
    )

    conn = authenticationObj.authToWarehouseUsingUserAndPass()

elif authentication_method == "SSO":
    authenticationObj = Authentication(
        warehouse=warehouse,
        database=database,
        user=user,
        password=None,
        account=account,
        schema=schema
    )
    conn = authenticationObj.authToWarehouseBrowserSSO()

else:
    authenticationObj = None
    conn = None

if conn is None:
    exit()

results = {}
printOutput(f"Loaded {str(len(QUERIES))} queries to check", "success")
for queryDict in QUERIES:
    query = queryDict['query']
    name = queryDict['name']
    description = queryDict['description']

    queryObj = Query(
        conn=conn,
        query=query,
        name=name
    )

    results[name] = queryObj.executeQuery()

    if results[name] is not None:
        if len(results[name]) > 1:
            csvinfo = results[name]
            dumpCSV(csvinfo, outputdir, name)

    printinfo = results[name]
    queryObj.printQueryOutput(name, printinfo)

authenticationObj.closeConnectionToWareHouse()

