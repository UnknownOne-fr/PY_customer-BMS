import csv
import numpy


def transform_csv(date_debut_app, date_debut_fin, building_filter_app):
    date_debut = date_debut_app
    date_fin = date_debut_fin
    building_filter = building_filter_app

    fname = f"data_{building_filter}_{date_debut}_{date_fin}.csv"

    try:

        # Used only when data is transformed
        device_key = []
        function_key = []
        date_key = []

        # load all datas from csv file in a dictionary
        with open(fname, newline='') as f:
            test_dict = []
            numero_ligne = 0
            reader = csv.reader(f)
            for row in reader:
                if row:
                    numero_ligne += 1
                    test_dict.append(row)

                    # Add values to lists
                    if not row[2] in device_key:
                        device_key.append(row[2])
                    if not row[3] in function_key:
                        function_key.append(row[3])

            print(f"{numero_ligne} lignes lues")

            # truncate date to delete the time part

            for row in test_dict:
                date_temp = row[0]
                date_finale = date_temp[:10]
                row[0] = date_finale
                if not row[0] in date_key:
                    date_key.append(date_finale)

        test_dict.sort()

        tab_final = []
        old_id = []
        list_value = []

        i = 0

        for rows in test_dict:
            # print("")
            id = [rows[2], rows[3], rows[0]]

            if id != old_id:
                if i != 0:
                    old_id.append(list_value)
                    tab_final.append(old_id)

                list_value = []
                old_id = id
                list_value.append(rows[1])

            else:
                list_value.append(rows[1])

            i += 1

        if list_value:
            old_id.append(list_value)
            tab_final.append(old_id)

        tab_final_final = []

        for lignes in tab_final:
            new_list = [float(j) for j in lignes[3]]
            tab_final_final.append([lignes[0], lignes[1], lignes[2], numpy.round(numpy.mean(new_list), 2),
                                    numpy.min(new_list), numpy.max(new_list)])

        for youpi in tab_final_final:
            print(youpi)

        # Save the result in a csv file
        numero_ligne = 0
        with open(f"finaldata_{building_filter}_{date_debut}_{date_fin}.csv", "w", newline="") as csv_data_file:
            for items in tab_final_final:
                numero_ligne += 1
                #print(f"Résultat {numero_ligne} : {items}")
                csv_writer = csv.writer(csv_data_file, delimiter=',')
                csv_writer.writerow(items)
        print(f"Les {numero_ligne} lignes de données ont bien été enregistrées au format CSV dans "
              f"finaldata_{building_filter}_{date_debut}_{date_fin}.csv .\n")

    except:
        print("Error transform CSV file")
