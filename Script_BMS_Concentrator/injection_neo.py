import psycopg2
import csv
from datetime import date

# Variables d'environnement
today = date.today()
date_jour = today.strftime("%Y-%m-%d")


def injection_neo(building_filter_app, final_file_name):
    try:
        print("tralala")

        with open(final_file_name, newline='') as f:
            final_list = []
            numero_ligne = 0
            reader = csv.reader(f)
            for row in reader:
                if row:
                    numero_ligne += 1
                    final_list.append(row)
                    print(f"{row} lu")

                    #############################################
                    # def of the function to find the id of the devices
                    query = f"SELECT pdcd.ID as DeviceDataID " \
                            f"FROM [fieldview].[dbo].[t_PollingDeviceConfigData] pdcd " \
                            f"INNER JOIN [fieldview].[dbo].[t_PollingDeviceFunctions] pdf ON pdf.ID = pdcd.FunctionID " \
                            f"INNER JOIN [fieldview].[dbo].[t_Device] dev ON dev.ID = pdcd.DeviceID " \
                            f"INNER JOIN [fieldview].[dbo].[t_PollingDeviceLocationData] pdld ON pdld.DeviceID = pdcd.DeviceID " \
                            f"INNER JOIN [fieldview].[dbo].[t_Locations] loc ON loc.ID = pdld.LocationID " \
                            f"WHERE loc.LocationName = '{building_filter_app}' AND dev.DeviceName = '{row[0]}' " \
                            f"AND pdf.FunctionName = '{row[1]}'"
                    #print("query : ", query)

                    # replace the value '5515' by the result of previous 'query'
                    query_value = 5515  # take result from 'query' in a variable to put it in 'last_query'

                    last_query = f"INSERT INTO @PollDataConverted " \
                                 f"SELECT {query_value}, '{row[2]}', {row[3]}, {row[4]}, {row[5]}"
                    print("last-query : ", last_query)

            # at the end of the 'PollDataConverted' inserts, we launch the stored proc from nlyte
            stocproc_nlyte = "CALL dbo.usp_update1Day"

            print("Appel de la procédure stockée réussi")

                    #############################################

    except (Exception, psycopg2.Error) as error:
        print("Erreur lors de la connexion à PostgreSQL", error)

