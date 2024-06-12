import os
import sys
import prettytable
from core.Other.PrintOutput.PrintOutput import printOutput
import pandas as pd

class Query:
    def __init__(self, conn, query, name):
        self.conn = conn
        self.query = query
        self.name = name

    def executeQuery(self):
        try:
            printOutput(f"Executing Query {self.name}", "loading")

            cursor = self.conn.cursor()
            cursor.execute(self.query)

            pd.set_option('display.max_colwidth', None)
            pd.set_option('display.max_rows', None)
            data = []
            headers = []

            for header in cursor.description:
                headers.append(str(header[0]).strip())

            data.append(headers)

            for result in cursor.fetchall():
                singleresult = []
                for sresult in list(result):
                    singleresult.append(str(sresult).strip())
                data.append(singleresult)

            printOutput(f"Successfully Executed Query", "success")

            return data

        except:
            printOutput(f"Error Executing Query {self.name}: {str(sys.exc_info()[1])}", "failure")
            return None

    def printQueryOutput(self, name, queryResult):
        printOutput(
            "----------------------------------------------------",
            "Loading"
        )
        printOutput(
            name,
            "successful"
        )
        printOutput(
            "----------------------------------------------------",
            "Loading"
        )


        if queryResult is None:
            printOutput("Error in result", "failure")

        else:
            if len(queryResult) == 1:
                printOutput(
                    "No values for this query",
                    "success"
                )

            else:
                #print(tabulate(queryResult, headers='keys', tablefmt='psql'))
                column_width, row_width = os.get_terminal_size(0)
                len(queryResult[0])
                if int(os.get_terminal_size().columns/len(queryResult[0]) - 5) > 5:
                    maxwidth = int(os.get_terminal_size().columns/len(queryResult[0]) - 5)
                else:
                    maxwidth = 5
                table = prettytable.PrettyTable(
                    max_table_width=column_width,
                    field_names=queryResult[0],
                    align='l',
                    max_width=maxwidth
                )

                del(queryResult[0])
                table.set_style(prettytable.DOUBLE_BORDER)
                table.add_rows(queryResult)

                print(table)


        printOutput('-' * (os.get_terminal_size().columns - 10), "success")