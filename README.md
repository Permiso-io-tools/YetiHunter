# YetiHunter
![image](.img/Yeti-Snowflake.png)
Permiso Security has created a tool to query snowflake environments for evidence of compromise, based on indicators from Permiso and the community.\
**Release Blog:** [[Introducing YetiHunter an open-source tool to detect and hunt for suspicious activity in snowflake](https://permiso.io/blog/introducing-yetihunter-an-open-source-tool-to-detect-and-hunt-for-suspicous-activity-in-snowflake)]
````

                ('-.   .-') _           ('-. .-.                  .-') _  .-') _     ('-.  _  .-')
              _(  OO) (  OO) )         ( OO )  /                 ( OO ) )(  OO) )  _(  OO)( \( -O )
  ,--.   ,--.(,------./     '._ ,-.-') ,--. ,--. ,--. ,--.   ,--./ ,--,' /     '._(,------.,------.
   \  `.'  /  |  .---'|'--...__)|  |OO)|  | |  | |  | |  |   |   \ |  |\ |'--...__)|  .---'|   /`. '
 .-')     /   |  |    '--.  .--'|  |  \|   .|  | |  | | .-') |    \|  | )'--.  .--'|  |    |  /  | |
(OO  \   /   (|  '--.    |  |   |  |(_/|       | |  |_|( OO )|  .     |/    |  |  (|  '--. |  |_.' |
 |   /  /\_   |  .--'    |  |  ,|  |_.'|  .-.  | |  | | `-' /|  |\    |     |  |   |  .--' |  .  '.'
 `-./  /.__)  |  `---.   |  | (_|  |   |  | |  |('  '-'(_.-' |  | \   |     |  |   |  `---.|  |\  \
   `--'       `------'   `--'   `--'   `--' `--'  `-----'    `--'  `--'     `--'   `------'`--' '--'
                                                                       by Permiso Security
````
## Installation
### Local Installation
To install, the only thing needed, is to install the required libraries.
````
python3 -m venv ./venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
````
Then, just run the tool by running **yetihunter.py**:
````
python3 yetihunter.py -h
usage: yetihunter [-h] [-u USER] [-p PASSWORD] [-w WAREHOUSE] [-a ACCOUNT] [-d DATABASE] [-s SCHEMA] [-am {SSO,USERPASS}] [-cf CONFIG_FILE_PATH] [-gcf] [-o OUTPUT_DIRECTORY]

Permiso Security has created a tool to query snowflake environments for evidence of compromise, based on indicators from Permiso and the community.

options:
  -h, --help            show this help message and exit
  -u USER, --user USER  The Snowflake user to authenticate as. Even if the authentication is SSO, the email of the identity authenticating should be added.
  -p PASSWORD, --password PASSWORD
                        This field is not required if the authentication is SSO, but required if the authentication is USERPASS. If needed and the field is empty, an imput will popup to ask for the password.
  -w WAREHOUSE, --warehouse WAREHOUSE
                        The Snowflake warehouse to connect to.
  -a ACCOUNT, --account ACCOUNT
                        The Snowflake Account to connect to. It should be in the format of <organization>-<account>
  -d DATABASE, --database DATABASE
                        The database name to connect to.
  -s SCHEMA, --schema SCHEMA
                        The name of the schema inside the database. This can be empty.
  -am {SSO,USERPASS}, --authentication-method {SSO,USERPASS}
  -cf CONFIG_FILE_PATH, --config-file-path CONFIG_FILE_PATH
                        If a config file is used, this option will have the path of the config file. No other flag is needed besides this.
  -gcf, --generate-config-file
                        If put, the tool will create an empty config file that can be filled by the user. The fields with null value can be left as null as they are not required.
  -o OUTPUT_DIRECTORY, --output-directory OUTPUT_DIRECTORY
                        The directory inside ./output/, where the query output files will be saved in.
````
### Docker
A Dockerfile is placed inside the main directory of the project. To build the image, inside the main directory of the project run:
````
docker build -t yetihunter .
````
Then run the container with directories **output** and **configfiles** mounted to host:
````
docker run -v ~/yetihunter/output:/yetihunter/output -v ~/yetihunter/configfiles:/yetihunter/configfiles -it yetihunter -h
usage: yetihunter [-h] [-u USER] [-p PASSWORD] [-w WAREHOUSE] [-a ACCOUNT] [-d DATABASE] [-s SCHEMA] [-am {SSO,USERPASS}] [-cf CONFIG_FILE_PATH] [-gcf] [-o OUTPUT_DIRECTORY]

Permiso Security has created a tool to query snowflake environments for evidence of compromise, based on indicators from Permiso and the community.

options:
  -h, --help            show this help message and exit
  -u USER, --user USER  The Snowflake user to authenticate as. Even if the authentication is SSO, the email of the identity authenticating should be added.
  -p PASSWORD, --password PASSWORD
                        This field is not required if the authentication is SSO, but required if the authentication is USERPASS. If needed and the field is empty, an imput will popup to ask for the password.
  -w WAREHOUSE, --warehouse WAREHOUSE
                        The Snowflake warehouse to connect to.
  -a ACCOUNT, --account ACCOUNT
                        The Snowflake Account to connect to. It should be in the format of <organization>-<account>
  -d DATABASE, --database DATABASE
                        The database name to connect to.
  -s SCHEMA, --schema SCHEMA
                        The name of the schema inside the database. This can be empty.
  -am {SSO,USERPASS}, --authentication-method {SSO,USERPASS}
  -cf CONFIG_FILE_PATH, --config-file-path CONFIG_FILE_PATH
                        If a config file is used, this option will have the path of the config file. No other flag is needed besides this.
  -gcf, --generate-config-file
                        If put, the tool will create an empty config file that can be filled by the user. The fields with null value can be left as null as they are not required.
  -o OUTPUT_DIRECTORY, --output-directory OUTPUT_DIRECTORY
                        The directory inside ./output/, where the query output files will be saved in.
````

## Usage
### Authenticating
#### Authenticating using user and password
To connect with a Snowflake user and a password, you need to pass those information, along with the account name, the warehouse name, the database name and optionally the database schema name:
````
$ python3 main.py -a <account id> -u <user> -w <warehouse> -d <database> -am USERPASS
[*] Successfully Authenticated to warehouse <warehouse> as user <user>!
````
#### Authenticating using SSO
To connect with a Snowflake user using SSO, you need to pass the user, along with the account name, the warehouse name, the database name and optionally the database schema name. Then go through the browser authentication and the tool will continue itself:
````
$ python3 main.py -a <account id> -u <user> -w <warehouse> -d <database> -am USERPASS
Initiating login request with your identity provider. A browser window should have opened for you to complete the login. If you can't see it, check existing browser windows, or your OS settings. Press CTRL+C to abort and try again...
Going to open: https://okta.permiso.io/app/snowflake/...<truncated> to authenticate...
[*] Successfully Authenticated to warehouse <warehouse>!
````
### Queries
The tool will search based on queries found on **./queries/queries.json**:
````
cat ./queries/queries.json
[
    {
        "name": "select_all_without_where",
        "description": "select * queries that do not contain a WHERE clause",
        "query": "SELECT query_id, user_name, query_text FROM snowflake.account_usage.query_history WHERE query_text ILIKE 'SELECT *' AND query_text NOT ILIKE '%WHERE%';"
    },
    ...
]
````
Each query has a name, a description and the query. New queries can be added to the JSON and they will be automatically executed by the tool.
### Output
When a query is executed, if there is output from it, a CSV file with the query's name is created and placed on the directory passed by option **-o** inside directory **output**:
````
ls output/testout/
10_largest_queries.csv  accountadmin_changes.csv  copy_http.csv  dbeaver_used.csv  impactful_modifications.csv  least_common_applications_used.csv  login_from_malicious_ips.csv  session_usage.csv  show_tables.csv
````
## References
UNC5537 Targets Snowflake Customer Instances for Data Theft and Extortion [[link](https://cloud.google.com/blog/topics/threat-intelligence/unc5537-snowflake-data-theft-extortion)]\
Detecting and Preventing Unauthorized User Access: Instructions [[link](https://community.snowflake.com/s/article/Communication-ID-0108977-Additional-Information)]\
A guide to threat hunting and monitoring in Snowflake [[link](https://securitylabs.datadoghq.com/articles/a-guide-to-threat-hunting-and-monitoring-in-snowflake/)]

