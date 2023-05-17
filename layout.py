from rich.console import RenderableType
from textual import events
from textual.app import App, ComposeResult
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Static, DataTable, Label, ProgressBar

import json
import format_for_table as fft
import req_ships as rs

class LabeledProgressBar(Widget):

    DEFAULT_CSS = """
    ProgressBar ETAStatus {
        display: none;
    }
    ProgressBar {
    margin: 0 2;
    }
    """

    labelText = reactive("", layout=True)
    progressBarTotal = reactive(0, layout=True)
    progressBarProgress = reactive(0, layout=True)

    def __init__(self, labelText: str = "", progressBarTotal: int = 0, progressBarProgress: int = 0) -> None:
        super().__init__()
        self.labelText = labelText
        self.progressBarTotal = progressBarTotal
        self.progressBarProgress = progressBarProgress

    def compose(self) -> ComposeResult:
        yield Label(self.labelText)
        yield ProgressBar()

    def on_mount(self) -> None:
        pb = self.query_one(ProgressBar)
        pb.total = self.progressBarTotal
        pb.progress = self.progressBarProgress

    def update(self, total: float, progress: float, advance: float) -> None:
        pb = self.query_one(ProgressBar)
        pb.update(total=total, progress=progress, advance=advance)

    # def on_mount(self) -> None:
    #     shipInfo = json.loads(rs.get_one('JOLIBUB-1'))
    #     pb = self.query_one(ProgressBar)
    #     pb.total = shipInfo["data"]["cargo"]["capacity"]
    #     pb.progress = shipInfo["data"]["cargo"]["units"]

    

class ShipInfoViewer(Static):

    shipSymbol = reactive("JOLIBUB-1", layout=True) #################               #TODO

    def __init__(self, renderable: RenderableType = "", *, shipSymbol: str = "", expand: bool = False, shrink: bool = False, markup: bool = True, name: str | None = None, id: str | None = None, classes: str | None = None, disabled: bool = False) -> None:
        super().__init__(renderable, expand=expand, shrink=shrink, markup=markup, name=name, id=id, classes=classes, disabled=disabled)


    def compose(self) -> ComposeResult:
        yield Label(self.shipSymbol)
        yield LabeledProgressBar(labelText="Cargo:")
        yield LabeledProgressBar(labelText="Fuel:")

    def on_mount(self) -> None:
        self.update_content()

    def set_ship_symbol(self, shipSymbol: str):
        self.shipSymbol = shipSymbol
        self.update_content()

    def update_content(self):
        shipInfo = json.loads(rs.get_one(self.shipSymbol))
        label = self.query(Label)[0]
        label.update(self.shipSymbol)
        lpb = self.query(LabeledProgressBar)
        for i, x in enumerate(lpb):
            if i == 0:
                x.update(total=shipInfo["data"]["cargo"]["capacity"], progress=shipInfo["data"]["cargo"]["units"], advance=None)
            elif i == 1:
                x.update(total=shipInfo["data"]["fuel"]["capacity"], progress=shipInfo["data"]["fuel"]["current"], advance=None)
        

ROWS = fft.get_ships()
class SpacetradersTUI(App):
    CSS_PATH = "layout.css"

    def compose(self) -> ComposeResult:
        yield DataTable(classes="box", id="main")
        yield ShipInfoViewer(classes="box")
        yield Static("Two", classes="box")
    
    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.cursor_type = "row"
        table.add_columns(*ROWS[0])
        for row in ROWS[1:]:
            table.add_row(*row, key=row[0])

    def on_data_table_row_selected(self, message: DataTable.RowSelected) -> None:
        shipInfoViewer = self.query_one(ShipInfoViewer)
        shipInfoViewer.set_ship_symbol(message.row_key.value)

app = SpacetradersTUI()
if __name__ == "__main__":
    app.run()