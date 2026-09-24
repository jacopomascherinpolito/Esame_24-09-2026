from logging import exception

import flet as ft

from model.airport import Airport


class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model

    def handle_creaGrafo(self, e):
        try:
            aeroporti = int(self._view.txtNumAeroporti.value)
            if aeroporti <= 0:
                self._view.create_alert("Inserire valore numerico > 0")
        except ValueError:
            self._view.create_alert("Inserire valore numerico valido")
        nodes, edges, dictnodes = self._model.costruisci_grafo(aeroporti)
        self._view.txt_result.clean()
        nodi, archi = self._model.get_stats()
        self._view.txt_result.controls.append(ft.Text(f"Nodi: {nodi}, Archi: {archi}"))
        self._view.ddCompagnia.disabled = False
        self.popola_dropdown(nodes, dictnodes)
        self._view.update_page()

    def popola_dropdown(self, list, dict):
        self._view.ddCompagnia.options.clear()

        for nd in list:
            c = nd.ID
            try:
                self._view.ddCompagnia.options.append(
                    ft.dropdown.Option(key=c, text=f"{nd.IATA_CODE} - {nd.NAME}"))
            except KeyError:
                pass
        self._view.btnCompagnieConcorrenti.disabled = False

    def handle_compagnieConcorrenti(self, e):
        try:
            idnodo = self._view.ddCompagnia.value
        except AttributeError:
            self._view.create_alert("Scegliere un'opzione")

        self._view.txtNumCompagnie.disabled = False
        self._view.btnCercaSequenza.disabled = False

        vicini = self._model.vicini(idnodo)
        list_v =[]
        for v in vicini:
            list_v.append(v)
        list_v.sort(key=lambda x:peso , reverse=True)
        self._view.txt_result.controls.append(ft.Text(f"Compagnie concorrenti di {self._view.ddCompagnia.value}"))
        peso = 0
        for v in list_v:
            self._view.txt_result.controls.append(ft.Text(f"{v.IATA_CODE} - {v.NAME}: {peso} rotte in comune"))

