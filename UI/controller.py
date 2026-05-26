import datetime

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._categoryValue = None

    def fillDDCategorie(self):
        categorie = self._model.getCategorie()
        categorieDDoptions = list(map(lambda x: ft.dropdown.Option(
            data=x,
            key = x.category_name,
            on_click = self._choiceCategory),
                                      categorie))

        self._view._ddcategory.options = categorieDDoptions
        self._view.update_page()

    def _choiceCategory(self, e):
        self._categoryValue = e.control.data

    def fillDDProdotti(self):
        allProdotti = self._model.getAllNodes()
        nodesDDoptionsStart = list(map(lambda x: ft.dropdown.Option(
            data=x,
            key = x.product_name,
            on_click = self._choiceProdStart),
                                      allProdotti))

        self._view._ddProdStart.options = nodesDDoptionsStart

        nodesDDoptionsEnd = list(map(lambda x: ft.dropdown.Option(
            data=x,
            key=x.product_name,
            on_click=self._choiceProdEnd),
                                       allProdotti))

        self._view._ddProdEnd.options = nodesDDoptionsEnd

        self._view.update_page()

    def _choiceProdStart(self, e):
        self._prodStartValue = e.control.data

    def _choiceProdEnd(self, e):
        self._prodEndValue = e.control.data

    def handleCreaGrafo(self, e):
        cat = self._categoryValue
        date1 = self._view._dp1.value
        date2 = self._view._dp2.value
        self._model.buildGraph(cat, date1, date2)
        nNodi, nArchi = self._model.getGraphDetails()

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text("Date selezionate :")
        )
        self._view.txt_result.controls.append(
            ft.Text(f"Start Date: {self._view._dp1.value.date()}")
        )
        self._view.txt_result.controls.append(
            ft.Text(f"End Date: {self._view._dp2.value.date()}")
        )
        self._view.txt_result.controls.append(
            ft.Text("Grafo creato:")
        )
        self._view.txt_result.controls.append(
            ft.Text(f"Numero di nodi: {nNodi}")
        )
        self._view.txt_result.controls.append(
            ft.Text(f"Numero di archi: {nArchi}")
        )
        self._view.update_page()

        self.fillDDProdotti()

    def handleBestProdotti(self, e):
        bestProdotti = self._model.getNodiPiuVenduti()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text("Di seguito i nodi maggiormente profittevoli :")
        )
        for p in bestProdotti:
            self._view.txt_result.controls.append(
                ft.Text(f"{p[0]} - score = {p[1]}")
            )
        self._view.update_page()

    def handleCercaCammino(self, e):
        if self._view._txtInLun.value == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Attenzione! Inserire un valore numerico in lun")
            )
            self._view.update_page()
            return

        try:
            lunInt = int(self._view._txtInLun.value)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Inserire un valore intero in lun")
            )
            self._view.update_page()
            return

        path, score = self._model.getBestPath(lunInt, self._prodStartValue, self._prodEndValue)

        if len(path) == 0:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text(f"Non ho trovato un cammino fra {self._prodStartValue} e {self._prodEndValue}")
            )
            self._view.update_page()
            return

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Ecco il cammino migliore fra {self._prodStartValue} e {self._prodEndValue}")
        )
        for p in path:
            self._view.txt_result.controls.append(ft.Text(p))
        self._view.txt_result.controls.append(ft.Text(f"Score: {score}"))
        self._view.update_page()

    def setDates(self):
        first, last = self._model.getDateRange()

        self._view._dp1.first_date = datetime.date(first.year, first.month, first.day)
        self._view._dp1.last_date = datetime.date(last.year, last.month, last.day)
        self._view._dp1.current_date = datetime.date(first.year, first.month, first.day)

        self._view._dp2.first_date = datetime.date(first.year, first.month, first.day)
        self._view._dp2.last_date = datetime.date(last.year, last.month, last.day)
        self._view._dp2.current_date = datetime.date(last.year, last.month, last.day)
