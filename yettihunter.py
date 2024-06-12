import json
import os
from getpass import getpass

from core.Authentication.Authentication import Authentication
from core.Other.Arguments.ArgParse import parseArgs, CONFIGFILE
from core.Other.PrintOutput.PrintOutput import printOutput
from core.Other.Resources.OutputDump import dumpCSV
from core.QueryActivity.QueryActivities import Query
from core.Other.Resources.Queries import QUERIES

args = parseArgs()

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

    user = configJson['USER']
    authentication_method = configJson['AUTHENTICATION_METHOD']
    warehouse = configJson['WAREHOUSE']
    account = configJson['ACCOUNT']
    database = configJson['DATABASE']
    outputdir = configJson['OUTPUTDIR']

    schema = configJson['SCHEMA']
    password = configJson['PASSWORD']

else:
    user = args.user
    authentication_method = args.authentication_method
    warehouse = args.warehouse
    account = args.account
    database = args.database
    schema = args.schema
    outputdir = args.output_directory

if outputdir is None or outputdir == "":
    printOutput(f"Output directory is a required option. Put the output directory name using -o flag", "failure")
    exit()

if os.path.exists(f'./output/{outputdir}'):
    printOutput(f"Output directory ./output/{outputdir} exists. put a new name", "failure")
    exit()
else:
    os.mkdir(f"./output/{outputdir}")

if authentication_method == "USERPASS":
    if args.password is None:
        password = getpass()
    else:
        password = args.password

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

