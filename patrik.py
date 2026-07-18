from dataclasses import dataclass, asdict
import json
from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Collapsible, TextArea, TabbedContent, TabPane, Label, Rule
from textual.containers import VerticalGroup
from textual.events import Resize

app_title = "\
     _/\/\/\/\/\__________________/\/\__________________/\/\____/\/\_______\n\
    _/\/\____/\/\__/\/\/\______/\/\/\/\/\__/\/\__/\/\__________/\/\__/\/\_  \n\
   _/\/\/\/\/\________/\/\______/\/\______/\/\/\/\____/\/\____/\/\/\/\___   \n\
  _/\/\__________/\/\/\/\______/\/\______/\/\________/\/\____/\/\/\/\___    \n\
 _/\/\__________/\/\/\/\/\____/\/\/\____/\/\________/\/\/\__/\/\__/\/\_     \n\
______________________________________________________________________     "


app_title_2 = "\
/$$$$$$$             /$$               /$$ /$$       \n\
| $$__  $$           | $$              |__/| $$      \n\
| $$  \ $$ /$$$$$$  /$$$$$$    /$$$$$$  /$$| $$   /$$\n\
| $$$$$$$/|____  $$|_  $$_/   /$$__  $$| $$| $$  /$$/\n\
| $$____/  /$$$$$$$  | $$    | $$  \__/| $$| $$$$$$/ \n\
| $$      /$$__  $$  | $$ /$$| $$      | $$| $$_  $$ \n\
| $$     |  $$$$$$$  |  $$$$/| $$      | $$| $$ \  $$\n\
|__/      \_______/   \___/  |__/      |__/|__/  \__/\n\
                                                     "


@dataclass
class Excercise:
    name: str
    time: int
    description: str
    notes: str


class ExcerciseDisplay(VerticalGroup):

    def __init__(self, excercise: Excercise, offset: int):
        super().__init__()
        self.excercise = excercise
        self.whitespace_offset = offset
    
    def compose(self):
        #whitespace = self.whitespace_offset - len(self.excercise.name) - len(str(self.excercise.time))
        #title = self.excercise.name + " "*whitespace + str(self.excercise.time) + " min"
        with Collapsible(classes="excercise"):
            ta = TextArea(classes="notes", text=self.excercise.notes)
            ta.border_title = "Notas"
            yield ta

    def on_text_area_changed(self, event: TextArea.Changed):
        self.excercise.notes = event.text_area.text
        self.app.save_data() #Is this a terrile way to do this?

    def on_collapsible_expanded(self, event):
        tab_pane = self.parent
        for coll in tab_pane.query("ExcerciseDisplay Collapsible"):
            if coll != event.collapsible:
                coll.collapsed = True

    def on_resize(self, event: Resize):
        self.update_title()

    def update_title(self):
        coll = self.query_one("Collapsible")
        whitespace = self.size.width - len(self.excercise.name) - len(str(self.excercise.time)) - 7
        coll.title = self.excercise.name + " "*whitespace + str(self.excercise.time) + " min"


class PatrickApp(App):
    """Musical practice aid for the terminal"""
    
    CSS_PATH = "patrik.tcss"
    sessions = []

    def compose(self) -> ComposeResult:
        self.load_data()

        yield Header()
        yield Label(app_title_2, classes="app_title")
        with TabbedContent():
            for i, session in enumerate(self.sessions):
                with TabPane(f"v{i+1}"):
                    max_name_len = max([len(ex.name) for ex in session])
                    offset = max_name_len + 30
                    for excercise in session:
                        yield ExcerciseDisplay(excercise, offset)
        yield Footer()


    def on_mount(self):
        self.animation_level = "none"

    def load_data(self):
        try:
            with open("data.json", "r") as file:
                self.sessions = [[Excercise(**x) for x in s] for s in json.load(file)]
        except:
            self.sessions = [[]]


    def save_data(self):
        data = [[asdict(x) for x in s ] for s in self.sessions]
        with open("data.json", "w") as file:
            json.dump(data, file, indent = 4)



if __name__ == "__main__":
    app = PatrickApp()
    app.run()





