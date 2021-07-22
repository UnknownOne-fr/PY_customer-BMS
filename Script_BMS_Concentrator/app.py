# Contient tous les éléments de l'interface graphique
import copy_data_bmsConcentrator

from PySide2 import QtCore, QtWidgets


class App(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Téléchargement des données du BMS_Concentrator")
        self.setup_ui()
        self.setup_connections()

    # Définition du layout qui défini les éléments affichés
    def setup_ui(self):
        self.layout = QtWidgets.QVBoxLayout(self)
        self.date_debut = QtWidgets.QLineEdit("YYYY-MM-DD")
        self.date_fin = QtWidgets.QLineEdit("YYYY-MM-DD")
        self.batiment = QtWidgets.QLineEdit("DCXX")
        self.lancement_requete = QtWidgets.QPushButton("Lancer l'export au format CSV")

        self.layout.addWidget(self.date_debut)
        self.layout.addWidget(self.date_fin)
        self.layout.addWidget(self.batiment)
        self.layout.addWidget(self.lancement_requete)

    # Déclaration des actions qui vont déclencher les modifications
    def setup_connections(self):
        self.lancement_requete.clicked.connect(self.export_data)

    # Déclaration de la fonction que lance l'export
    def export_data(self):
        date_debut_app = self.date_debut.text()
        date_fin_app = self.date_fin.text()
        building_filter_app = self.batiment.text()

        copy_data_bmsConcentrator.main_function_export(date_debut_app, date_fin_app, building_filter_app)


app = QtWidgets.QApplication([])
win = App()
win.show()
app.exec_()
