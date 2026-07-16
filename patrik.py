from dataclasses import dataclass
from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Collapsible, TextArea, TabbedContent, TabPane, Label


app_title = "     _/\/\/\/\/\__________________/\/\__________________/\/\____/\/\_______\n\
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

chop_builder = Excercise("Chop Builder", 10, "desc", None)
notas = Excercise("Encontrar notas", 5, None, "")

v1 = [chop_builder, notas]



class PatrickApp(App):
    """Musical practice aid for the terminal"""
    
    CSS_PATH = "patrik.tcss"

    def compose(self) -> ComposeResult:
        yield Header()

        yield Label(app_title_2, classes="app_title")

        with TabbedContent():
            with TabPane("v1"):

                for ex in v1:
                    with Collapsible(title=ex.name):
                        if ex.description:
                            yield Label(ex.description)
                        ta = TextArea(classes="notes")
                        ta.border_title = "Notas"
                        yield ta

            with TabPane("v2"):
                yield Label("v2")

        yield Footer()


    def on_mount(self):
        self.animation_level = "none"

if __name__ == "__main__":
    app = PatrickApp()
    app.run()





