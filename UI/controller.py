import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._choiceDD = None

    def handleCreaGrafo(self, e):
        dMinTxt= self._view._txtInDurata.value
        if dMinTxt is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f" Inserisci una durata", color = "red"))
            self._view.update_page()
            return
        try:
            dMinTxtInt = int(dMinTxt)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f" Inserisci un valore numerico", color="red"))
            self._view.update_page()
            return

        self._model.buildGraph(dMinTxtInt)
        n,a = self._model.getGraphDetails()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Grafo correttamente creato. " f"Il grafo è costituito di {n} nodi e {a} archi"))
        self.fillDD(self._model.getAllNodes())
        self._view.update_page()

    def getSelectedAlbum(self, e):
        pass

    def handleAnalisiComp(self, e):
        if self._choiceDD is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text(f"Seleziona un album", color = "red"))
            self._view.update_page()
            return
        size, dTotCC= self._model.getInfoConnessa(self._choiceDD)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"La componente connessa che contiene {self._choiceDD} ha {size} nodi e una durata totale di {dTotCC} minuti"))
        self._view.update_page()
        return


    def handleGetSetAlbum(self, e):
        sogliaTxt= self._view._txtInSoglia.value
        if sogliaTxt=="":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Inserisci una soglia", color = "red"))
            self._view.update_page()
            return
        try:
            sogliaTxtInt = int(sogliaTxt)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Inserisci una soglia numerica", color="red"))
            self._view.update_page()
            return
        if self._choiceDD is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Attenzione, selezionare una voce dal DD", color = "red"))
            self._view.update_page()
            return
        setofNodes, sumDurate=self._model.getSetOfNodes(self._choiceDD, sogliaTxtInt)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Ho trovato un set di album che soddisfa le specifiche, dimensione = {len(setofNodes)}, durata totale= {sumDurate}." f"Di seguito gli album che fanno parte della soluzione trovata: "))
        for n in setofNodes:
            self._view.txt_result.controls.append(ft.Text(n))

        self._view.update_page()



    def fillDD(self, listOfNodes):
        listOfNodes.sort(key=lambda x: x.Title)
        listOfOtions=map(lambda x: ft.dropdown.Option(text=x.Title, data=x, on_click=self._readDDValue), listOfNodes)
        self._view._ddAlbum.options=list(listOfOtions)

    def _readDDValue(self, e):
        if e.control.data is None:
            self._choiceDD=None
            print("error in reading DD")
        self._choiceDD=e.control.data
