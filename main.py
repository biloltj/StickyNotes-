import sys
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction,QPalette, QColor,QIcon

from PySide6.QtWidgets import (
    QApplication,
    QMenu,
    QHBoxLayout,
    QPushButton,
    QSystemTrayIcon,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)
app = QApplication(sys.argv)
active_notewindows = {}



class NoteWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sticky Notes")
         
     
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("blue"))  
        self.setAutoFillBackground(True)
        self.setPalette(palette)

        
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("Write your notes here...")

     
        layout = QVBoxLayout()
        buttons = QHBoxLayout()
        self.close_btn = QPushButton("×")
        self.close_btn.setStyleSheet(
            "font-weight: bold; font-size: 25px; width: 25px; height: 25px;"
        )
        self.close_btn.clicked.connect(self.close)
        self.close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        buttons.addStretch()  # Add stretch on left to push button right.
        buttons.addWidget(self.close_btn)
        layout.addLayout(buttons)

        layout.addWidget(self.text_edit)
        self.setLayout(layout)
        active_notewindows[id(self)] = self
    def mousePressEvent(self, e):
        self.previous_pos = e.globalPosition()

    def mouseMoveEvent(self, e):
        delta = e.globalPosition() - self.previous_pos
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.previous_pos = e.globalPosition()


def create_notewindow():
    note = NoteWindow()
    note.show()


create_notewindow()

# Create the icon
icon = QIcon("note.png")

# Create the tray
tray = QSystemTrayIcon()
tray.setIcon(icon)
tray.setVisible(True)


def handle_tray_click(reason):
    # If the tray is left-clicked, create a new note.
    if (
        QSystemTrayIcon.ActivationReason(reason)
        == QSystemTrayIcon.ActivationReason.Trigger
    ):
        create_notewindow()


tray.activated.connect(handle_tray_click)

app.setQuitOnLastWindowClosed(False)

# Create the menu
menu = QMenu()
add_note_action = QAction("Add note")
add_note_action.triggered.connect(create_notewindow)
menu.addAction(add_note_action)

# Add a Quit option to the menu.
quit_action = QAction("Quit")
quit_action.triggered.connect(app.quit)
menu.addAction(quit_action)

# Add the menu to the tray
tray.setContextMenu(menu)



window = NoteWindow()
window.show()
app.exec()
