# Code written by Thomas Deleforge
# v1 : 2021-05-16

import psycopg2
import csv
from datetime import date
from transform_script import transform_csv
from injection_neo import injection_neo

# Variables d'environnement
today = date.today()
date_jour = today.strftime("%Y-%m-%d")


def main_function_export(date_debut_app, date_debut_fin, building_filter_app):
    try:
        conn = psycopg2.connect(
            user="bms_concentrator",
            password="bms_concentrator",
            host="10.0.41.20",
            port="5432",
            database="bms_concentrator"
        )
        cur = conn.cursor()

        # Afficher la version de PostgreSQL
        cur.execute("SELECT version();")
        version = cur.fetchone()
        print("Version : ", version, "\n")

        # Date utilisées dans les filtres
        date_debut = date_debut_app
        date_fin = date_debut_fin

        # Liste des DC + celui utilisé pour le filtre
        # print("DC01 / DC02 / DC03 / DC04 / DC05 / DC06 / DC07 / DC08 / DC09 / DC10 / D3 / DB")
        building_filter = building_filter_app

        # Requête de récupération des données pour le DC08 pour la date d'hier
        # Retirer le 'limit 10' qd test terminés
        cur.execute(
            f"SELECT date_time, data_value, data_device, data_type FROM exchange_data "
            f"INNER JOIN mappings_data ON exchange_data.data_code = mappings_data.data_code "
            f"WHERE building = '{building_filter}' AND date_time BETWEEN '{date_debut}' and '{date_fin}';")
        select_query = cur.fetchall()

        numero_ligne = 0
        with open(f"data_{building_filter}_{date_debut}_{date_fin}.csv", "w", newline="") as csv_data_file:
            for items in select_query:
                numero_ligne += 1
                #print(f"Résultat {numero_ligne} : {items}")
                csv_writer = csv.writer(csv_data_file, delimiter=',')
                csv_writer.writerow(items)
        print(f"Les {numero_ligne} lignes de données ont bien été enregistrées au format CSV.\n")

        # fermeture de la connexion à la base de données
        cur.close()
        conn.close()
        print("La connexion PostgreSQL est fermée")

        transform_csv(date_debut, date_fin, building_filter)

        final_file_name = f"finaldata_{building_filter}_{date_debut}_{date_fin}.csv"

        injection_neo(building_filter, final_file_name)

    except (Exception, psycopg2.Error) as error:
        print("Erreur lors de la connexion à PostgreSQL", error)
