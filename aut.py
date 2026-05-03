import sys, time, random
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Signal, QObject
from pynput import mouse, keyboard

On_Off = ["Turn on", "Turn off"]
randsp = ["Random Mode: Off", "Random Mode: On"]

class MainWindow(QtWidgets.QWidget):
    
    num_sent = Signal(int)
    
    def __init__(self):
        super().__init__()
    
        self.mouse_controller = mouse.Controller()
        self.listener = keyboard.Listener(on_press=self.keyboard_actoins)
        self.num_sent.connect(self.changeOnOff) 
        self.listener.start()
        
        self.status = 0
        self.randstat = 0
        
        self.setStyleSheet("""
                    QWidget {
                        background-color: #0a192f;
                    }
                    QLabel {
                        color: white;
                        font-size: 14px;
                        font-weight: bold;
                    }
                    QFrame {
                        background-color: #2c3e50;
                    }
                    QPushButton {
                        color: white;
                        background-color: pastel;
                    }
                """)
    
        layout = QtWidgets.QVBoxLayout(self)
        self.setLayout(layout)
        
        grtlabel = QtWidgets.QLabel("Auto Clicker v1.0",
                                         alignment=QtCore.Qt.AlignCenter)
        layout.addWidget(grtlabel)
        
        
        self.btn1 = QtWidgets.QPushButton(On_Off[self.status])
        layout.addWidget(self.btn1, alignment=QtCore.Qt.AlignCenter)
        self.btn1.clicked.connect(self.changeOnOff)
        
        self.randlabel = QtWidgets.QLabel(randsp[self.randstat],
                                         alignment=QtCore.Qt.AlignCenter)
        layout.addWidget(self.randlabel)
        
        btn2 = QtWidgets.QPushButton("randmode")
        btn2.clicked.connect(self.random_status_change)
        layout.addWidget(btn2, alignment=QtCore.Qt.AlignCenter)
        
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.do_click)
        
        
        
    @QtCore.Slot(int)
    def changeOnOff(self, n=0):
        if n == 0:
            self.status = (self.status + 1) % 2
        elif n == 1:
            self.status = 1
        elif n == 2:
            self.status = 0
        
        self.btn1.setText(On_Off[self.status])
    
        if self.status == 1:
            self.do_click()

        
    def do_click(self):
        if self.status == 0:
            return
            
        self.mouse_controller.click(mouse.Button.left)
        
        interval = random.randint(50, 190) if self.randstat == 1 else 100
        
        self.timer.setSingleShot(True)
        self.timer.start(interval)

        
    def random_status_change(self):
        self.randstat = (self.randstat + 1) % 2
        self.randlabel.setText(randsp[self.randstat])


    def keyboard_actoins(self, key):
        if key == keyboard.Key.f7:
            self.num_sent.emit(2)
        elif key == keyboard.Key.f5:
            self.num_sent.emit(1)
        

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.resize(400, 300)
    window.show()

    sys.exit(app.exec())