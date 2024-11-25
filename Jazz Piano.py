import sys,mido,json,random,os
from PyQt6.QtWidgets import QApplication, QMainWindow, QListWidget, QVBoxLayout, QWidget, QHBoxLayout, QPushButton,QLabel,QGraphicsScene, QGraphicsPixmapItem, QGraphicsView
from PyQt6.QtGui import QPixmap, QFont,QIcon
from PyQt6.QtCore import Qt, pyqtSignal,QTimer
from playsound3 import playsound
import threading
#TODO :SOUND
#TODO :SCORE
#TODO: ECONOMISE THE CODE WHERE POSSIBLE
class MainApp(QMainWindow):
    note_on_signal = pyqtSignal(int, str)
    note_off_signal = pyqtSignal(int)
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: darkgreen;")
        self.theory1,self.theory2,self.theory3,self.theory4 ,self.last_selected_scale, self.last_selected_note = None,None,None,None,None,None
        self.setWindowTitle('Note Handler')
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.setFixedWidth(1080)
        self.pixmap_item = {}
        self.circledegree = 0
        self.main_layout = QVBoxLayout(self.central_widget)
        self.horizontal_layout = QHBoxLayout()
        self.listwidget1 = QListWidget()
        self.listwidget1.addItems(['Notes', 'Scales', 'Chords'])
        self.listwidget1.setStyleSheet("QListWidget { color: white; }")
        self.listwidget2 = QListWidget()
        self.listwidget3 = QListWidget()
        self.listwidget4 = QListWidget()
        self.listwidget4 = QListWidget()
        self.listwidget2.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.listwidget1.setFixedSize(75, 100)
        self.listwidget2.setFixedSize(125, 100)
        self.listwidget3.setFixedSize(75, 100)
        self.listwidget4.setFixedSize(75, 100)  # Set width to 200px and height to 300px

        self.listwidget2.setStyleSheet("QListWidget { color: white; }")
        self.listwidget3.setStyleSheet("QListWidget { color: white; }")
        self.listwidget4.setStyleSheet("QListWidget { color: white; }")
        self.label1 = QLabel('')
        self.label1.setFont(QFont("Arial", 32))
        self.label1.setStyleSheet("QLabel { color: white; }")  # Set font color to white
        self.label2 = QLabel('')
        self.label2.setStyleSheet("QLabel { color: white; }")  # Set font color to white
        self.label2.setFont(QFont("Arial", 20))
        self.label3 = QLabel('')
        self.label3.setStyleSheet("QLabel { color: white; }")  # Set font color to white

        self.vlayout = QVBoxLayout()
        self.listwidget1.currentItemChanged.connect(self.listwidget1changed)
        self.listwidget2.currentItemChanged.connect(self.listwidget2changed)
        self.listwidget3.currentItemChanged.connect(self.listwidget3changed)
        self.listwidget4.currentItemChanged.connect(self.listwidget4changed)
        self.horizontal_layout.addWidget(self.listwidget1)
        self.horizontal_layout.addWidget(self.listwidget2)
        self.horizontal_layout.addWidget(self.listwidget3)
        self.horizontal_layout.addWidget(self.listwidget4)
        self.theory_button = QPushButton('Go!')
        self.theory_button.setStyleSheet("QPushButton { color: white; }")
        self.reveal_button = QPushButton('Reveal')
        self.reveal_button.setStyleSheet("QPushButton { color: white; }")
        self.theory_button.setEnabled(False)
        self.reveal_button.setEnabled(False)
        self.reveal_button.clicked.connect (self.reveal_button_clicked)
        self.required_notes =[0]
        self.pressed_notes = []
        self.scale_degree_number = 0
        self.vlayout.addWidget(self.label1)
        self.vlayout.addWidget(self.label2)
        self.vlayout.addWidget(self.label3)
        self.vlayout.addWidget(self.reveal_button)

        self.vlayout.addWidget(self.theory_button)

        self.horizontal_layout.addLayout(self.vlayout)
        self.horizontal_layout.setStretch(0, 1)  # listwidget1
        self.horizontal_layout.setStretch(1, 1)  # listwidget2
        self.horizontal_layout.setStretch(2, 1)  # listwidget3
        self.horizontal_layout.setStretch(3, 1)  # listwidget4
        self.horizontal_layout.setStretch(4, 3)  # vlayout containing labels and button
        self.main_layout.addLayout(self.horizontal_layout)
        self.Scene = QGraphicsScene()
        self.BackgroundPixmap = QPixmap("keys.png")
        self.BackgroundItem = QGraphicsPixmapItem(self.BackgroundPixmap)
        self.Scene.addItem(self.BackgroundItem)
        self.View = QGraphicsView(self.Scene)
        self.View.setFixedSize(self.BackgroundPixmap.size())
        self.View.setSceneRect(0, 0, self.BackgroundPixmap.width(), self.BackgroundPixmap.height())
        self.View.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.View.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.main_layout.addWidget(self.View)
        self.note_on_signal.connect(self.insert_note)
        self.note_off_signal.connect(self.delete_note)
        self.theory_button.clicked.connect(self.choose_mode)
        self.listwidget1.clicked.connect(self.listwidget1_clicked)
        self.listwidget2.clicked.connect(self.listwidget2_clicked)
        self.listwidget3.clicked.connect(self.listwidget3_clicked)
        self.listwidget4.clicked.connect(self.listwidget4_clicked)
        self.theory1 = None
        self.load_data()
    def load_data(self):
        with open('theory.json', 'r') as file: self.Theory = json.load(file)
    def listwidget1changed(self, current):
        if current:  self.theory1 = current.text()
    def listwidget2changed(self, current):
        if current: self.theory2 = current.text()
    def listwidget3changed(self, current):
        if current:self.theory3 = current.text()
    def listwidget4changed(self, current):
        if current: self.theory4 = current.text()
    def listwidget1_clicked(self):
        self.theory_button.setEnabled(False)
        self.reveal_button.setEnabled(False)
        self.required_notes = []
        self.listwidget2.clear()
        self.listwidget3.clear()
        self.listwidget4.clear()
        match self.listwidget1.currentItem().text():
            case 'Notes':self.listwidget2.addItems(['Naturals','Sharps','Flats'])
            case 'Scales':self.listwidget2.addItems(['Major','Minor','Harmonic','Melodic','Modes'])
            case 'Chords':self.listwidget2.addItems(['Triads','Sevenths','Shells'])
    def listwidget2_clicked(self):
        self.listwidget3.clear()
        self.listwidget4.clear()
        match self.listwidget2.currentItem().text():
            case 'Naturals' | 'Sharps' | 'Flats' :
                self.theory_button.setEnabled(True)
                self.reveal_button.setEnabled(True)
            case 'Major' | 'Minor' | 'Harmonic' | 'Melodic' : self.theory_button.setEnabled(True)
            case 'Triads':self.listwidget3.addItems(['Major', 'Minor'])
            case 'Sevenths':self.listwidget3.addItems(['Major','Minor','m7♭5','Dim7','Dom7'])
            case 'Shells':self.listwidget3.addItems(['Major','Minor','Dominant'])
    def listwidget3_clicked(self):
        self.listwidget4.clear()
        self.theory_button.setEnabled(False)
        self.reveal_button.setEnabled(False)
        match self.listwidget2.currentItem().text():
            case 'Sevenths':self.listwidget4.addItems(['Root','First','Second','Third'])
            case 'Shells':self.listwidget4.addItems(['0','1'])
            case 'Triads':self.listwidget4.addItems(['Root','First','Second'])
    def listwidget4_clicked(self):
        match self.listwidget4.currentItem().text():
            case 'Root' | 'First'| 'Second'| 'Third' | '0' | '1':
                self.theory_button.setEnabled(True)
                self.reveal_button.setEnabled(True)

    def choose_mode(self):
        self.label1.clear()
        self.label2.clear()
        self.label3.clear()

        match self.theory1:
            case "Notes":
                self.handle_notes_case()

            case "Scales":
                self.handle_scales_case()

            case "Chords":
                self.handle_chords_case()

    def reveal_button_clicked(self):
        # Set the time delay between strobe for each note (in milliseconds)
        delay = 500  # 200ms, adjust as needed

        def emit_note_on(index):
            if index < len(self.required_notes):
                note = self.required_notes[index]
                self.note_on_signal.emit(note, "green")

                # Set a timer to turn the note off after a short duration
                QTimer.singleShot(delay, lambda: self.note_off_signal.emit(note))

                # Move to the next note after the delay
                QTimer.singleShot(delay, lambda: emit_note_on(index + 1))

        # Start emitting the first note
        emit_note_on(0)

    def handle_notes_case(self):

        self.reveal_button.setEnabled(False)
        selected_scale = random.choice(self.Theory['Notes'][self.theory2])
        while selected_scale == self.last_selected_note:
            selected_scale = random.choice(self.Theory['Notes'][self.theory2])

        self.last_selected_note = selected_scale
        self.required_notes = selected_scale + 60

        if self.theory2 in ["Naturals", "Sharps"]:
            self.label1.setText(self.Theory['Chromatic'][selected_scale])
        elif self.theory2 == "Flats":
            self.label1.setText(self.Theory['Enharmonic'][selected_scale])

    def handle_scales_case(self):
        self.reveal_button.setEnabled(True)
        self.load_data()
        match self.theory2:
            case "Modes":
                print("Code Required")  # Placeholder for Modes, add code as necessary
            case _:
                selected_scale = self.Theory["Circle"][self.theory1][self.theory2][self.circledegree]
                intervals = self.Theory['Scales'][self.theory2][selected_scale]
                self.circledegree = (self.circledegree + 1) % 12
                self.label1.setText(selected_scale)
                self.label2.setText(", ".join(map(str, self.Theory['Theory'][selected_scale])))
                self.label3.setText(
                    ", ".join(map(str, self.Theory['Fingering'][self.theory2][selected_scale]['Right'])))
                self.required_notes = self.extend_scale(intervals, 1, 60, descending=True)

    def handle_chords_case(self):
        selected_scale = self.Theory["Circle"][self.theory1][self.theory2][self.theory3][self.circledegree]

        match self.theory2:
            case "Triads":
                self.handle_triads_case(selected_scale)
            case "Sevenths":
                self.handle_sevenths_case(selected_scale)
            case "Shells":
                self.handle_shells_case(selected_scale)

    def handle_triads_case(self, selected_scale):
        try:
            intervals = self.Theory["Triads"][selected_scale][self.theory4]
            self.circledegree = (self.circledegree + 1) % 12
            self.required_notes = self.extend_scale(intervals, 1, 60, descending=False)
            self.label1.setText(f"{selected_scale} {self.theory4}")
        except KeyError:
            print(f"Error: {selected_scale} not found in Triads")

    def handle_sevenths_case(self, selected_scale):
        scaleletter = selected_scale.split()[0]
        selected_scale = f"{scaleletter} {self.theory3}"
        try:
            intervals = self.Theory["Sevenths"][selected_scale][self.theory4]
            self.circledegree = (self.circledegree + 1) % 6
            self.required_notes = self.extend_scale(intervals, 1, 60, descending=False)
            self.label1.setText(f"{selected_scale}")
            self.label2.setText(self.theory4)
        except KeyError:
            print(f"Error: {selected_scale} not found in Sevenths")

    def handle_shells_case(self, selected_scale):
        try:
            intervals = self.Theory["Shells"][self.theory3][selected_scale][self.theory4]
            self.required_notes = intervals
            self.circledegree = (self.circledegree + 1) % 12
            self.label1.setText(selected_scale)
        except KeyError:
            print(f"Error: {selected_scale} not found in Shells")

    def note_handler(self, message):
        if message.type == "note_off":

            self.note_off_signal.emit(message.note)
            self.pressed_notes.remove(message.note)
        if message.type == "note_on":
            match self.theory1:
                case 'Notes':
                    if message.note == self.required_notes:
                        self.play_sound_in_background('correct.mp3')

                        self.note_on_signal.emit(message.note, "green")
                        self.choose_mode()
                    else:
                        print ('testing123')
                       #self.play_sound_in_background('incorrect.mp3')
                        self.note_on_signal.emit(message.note, "red")
                case 'Scales':

                    if message.note == self.required_notes[self.scale_degree_number]:
                        self.note_on_signal.emit(message.note, "green")
                        self.scale_degree_number += 1
                        if self.scale_degree_number == len(self.required_notes):
                            self.scale_degree_number = 0
                            self.play_sound_in_background('correct.mp3')
                            self.choose_mode()
                    else:
                        if message.note == self.required_notes[0]:
                            self.scale_degree_number = 1
                            self.note_on_signal.emit(message.note, "green")
                        else:
                            self.play_sound_in_background('incorrect.mp3')
                            self.scale_degree_number = 0
                            self.note_on_signal.emit(message.note, "red")
                case 'Chords':
                    if message.note in self.required_notes:
                        self.note_on_signal.emit(message.note, "green")
                        self.pressed_notes.append(message.note)

                        if len(self.pressed_notes) >= len(self.required_notes):
                            self.play_sound_in_background('correct.mp3')
                            self.choose_mode()
                    else:
                        self.note_on_signal.emit(message.note, "red")
                case _:
                    self.note_on_signal.emit(message.note, "red")
    def extend_scale(self, intervals, num_octaves, root_note=60, descending=False):

        midi_notes = []
        intervals = [int(interval) for interval in intervals]
        for octave in range(num_octaves): midi_notes += [root_note + interval + 12 * octave for interval in intervals]
        if descending:
            descending_notes = []
            for octave in reversed(range(num_octaves)):descending_notes += [root_note + interval + 12 * octave for interval in reversed(intervals[:-1])]
            midi_notes += descending_notes
        return midi_notes
    def insert_note(self, note, color):
        self.xcord = self.Theory["NoteCoordinates"][note % 12] + ((note // 12) - 4) * 239
        self.pixmap_item[note] = QGraphicsPixmapItem(QPixmap("key_" + color + self.Theory["NoteFilenames"][note % 12]))
        self.pixmap_item[note].setPos(self.xcord, 0)
        current_scene = self.pixmap_item[note].scene()
        if current_scene: current_scene.removeItem(self.pixmap_item[note])
        self.Scene.addItem(self.pixmap_item[note])
    def delete_note(self, note):
        if note in self.pixmap_item:
            if self.pixmap_item[note].scene(): self.pixmap_item[note].scene().removeItem(self.pixmap_item[note])
            del self.pixmap_item[note]

    def play_sound_in_background(self,file_path):
        def play():
            try:
                playsound(file_path)
            except Exception as e:
                print(f"Error playing sound: {e}")
        # Start the thread
        thread = threading.Thread(target=play)
        thread.start()



app = QApplication(sys.argv)
main_app = MainApp()
main_app.show()

with mido.open_input(callback=main_app.note_handler) as inport: sys.exit(app.exec())