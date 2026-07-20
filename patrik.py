from dataclasses import dataclass, asdict
import json
from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Collapsible, TextArea, TabbedContent, TabPane, Label, Rule, Digits, Button
from textual.containers import VerticalGroup, HorizontalGroup, Horizontal, Vertical
from textual.events import Resize
import random
import pyfiglet
import time

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

    def __init__(self, excercise: Excercise):
        super().__init__()
        self.excercise = excercise
    
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
        whitespace = self.size.width - len(self.excercise.name) - len(str(self.excercise.time)) - 8
        coll.title = self.excercise.name + " "*whitespace + str(self.excercise.time) + " min"


class NotePicker(Horizontal):

    BINDINGS = [
            ("up", "inc_interval", "Increment interval"),
            ("down", "dec_interval", "Decrease interval"),
            ("space", "toggle", "Start/Stop")
            ]

    notes = ['Ab', 'A', 'A#', 'Bb', 'B', 'C', 'C#', 'Db', 'D', 'D#', 'Eb', 'E', 'F', 'F#', 'Gb', 'G', 'G#']
    started = False
    interval = 2.5;

    def compose(self) -> ComposeResult:
        #note = text2art(random.choice(self.notes), font="future") #future smblock tarty3 dos_rebel
        #note = pyfiglet.figlet_format(random.choice(self.notes), font="smblock")
        self.border_title = "Random Note Picker"
        self.note_display = Label("", classes="note")
        self.choose_note()
        yield self.note_display
        with Horizontal(classes="interval_picker"):
            self.interval_display = Digits(str(self.interval), classes="interval")
            yield self.interval_display
            with Vertical():
                yield Button(">", id="inc")
                yield Button("<", id="dec")
                yield Button("Start", id="start")
                yield Button("Stop", id="stop")


    def action_dec_interval(self):
        if self.interval >= 1:
            self.interval -= 0.5
            self.interval_display.update(str(self.interval))
            if self.started:
                self.start()

    def action_inc_interval(self):
        self.interval += 0.5
        self.interval_display.update(str(self.interval))
        if self.started:
            self.start()

    def action_toggle(self):
        if self.started:
            self.stop()
        else:
            self.start()

    def on_mount(self):
        self.timer = self.set_interval(self.interval, self.choose_note, pause=True)

    def start(self):
        self.started = True
        self.add_class("started")
        self.choose_note()
        self.timer.stop()
        self.timer = self.set_interval(self.interval, self.choose_note, pause=False)

    def stop(self):
        if self.started:
            self.started = False
            self.remove_class("started")
            self.timer.pause()
        

    def choose_note(self):
        note = pyfiglet.figlet_format(random.choice(self.notes), font="smblock")
        self.note_display.update(note)

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "start":
            self.start()
        if event.button.id == "stop":
            self.stop()
        if event.button.id == "inc":
            self.action_inc_interval()
        if event.button.id == "dec":
            self.action_dec_interval()


class PatrickApp(App):
    """Musical practice aid for the terminal"""
    
    CSS_PATH = "patrik.tcss"
    sessions = []

    def compose(self) -> ComposeResult:
        self.load_data()

        yield Header()
        yield Label(app_title_2, classes="app_title")
        #yield NotePicker()
        yield Label("Sessoins", classes="section_title")
        with TabbedContent(classes="sessions"):
            for i, session in enumerate(self.sessions):
                with TabPane(f"v{i+1}"):
                    for excercise in session:
                        yield ExcerciseDisplay(excercise)

        yield Label("Tools", classes="section_title")
        with TabbedContent(classes="tools"):
            with TabPane("Note Picker"):
                yield NotePicker()
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





