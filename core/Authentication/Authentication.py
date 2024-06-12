import sys

import snowflake.connector
from core.Other.PrintOutput.PrintOutput import printOutput

class Authentication:
    def __init__(self, warehouse, database, user, password, account, schema): #, oktaaccountname):
        self.warehouse = warehouse
        self.database = database
        self.user = user
        self.password = password
        self.account = account
        self.schema = schema

        self.conn = None

    def authToWarehouseUsingUserAndPass(self):
        try:
            printOutput(f"Authenticating to warehouse {self.warehouse} as user {self.user}", "loading")
            conn = snowflake.connector.connect(
                user=self.user,
                password=self.password,
                account=self.account,  #
                warehouse=self.warehouse,
                database=self.database,
                schema=self.schema,
                role="ACCOUNTADMIN"
            )
            printOutput(f"Successfully Authenticated to warehouse {self.warehouse} as user {self.user}", "success")
            self.conn = conn
            return conn
        except:
            printOutput(f"Error Authenticating to warehouse {self.warehouse} as user {self.user}: {str(sys.exc_info()[1])}", "failure")
            return None

    def authToWarehouseBrowserSSO(self):
        try:
            printOutput(f"Authenticating to warehouse {self.warehouse} using browser", "loading")
            conn = snowflake.connector.connect(
                #authenticator=f'https://{self.oktaaccountname}.okta.com',
                authenticator='externalbrowser',
                user=self.user,
                account=self.account,  #
                warehouse=self.warehouse,
                database=self.database,
                schema=self.schema,
                role="ACCOUNTADMIN"
            )

            printOutput(f"Successfully Authenticated to warehouse {self.warehouse}", "success")
            self.conn = conn
            return conn
        except:
            printOutput(f"Error Authenticating to warehouse {self.warehouse}: {str(sys.exc_info()[1])}", "failure")
            return None

    def closeConnectionToWareHouse(self):
        try:
            printOutput(f"Closing connection to warehouse {self.warehouse} as user {self.user}", "loading")
            if self.conn is not None:
                self.conn.close()
            printOutput(f"Successfully Closed connection to warehouse {self.warehouse} as user {self.user}", "success")
            return True
        except:
            printOutput(f"Error Closing connection to warehouse {self.warehouse} as user {self.user}: {str(sys.exc_info()[1])}", "failure")
            return False