from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QComboBox, QDialogButtonBox
from pyqtgraph import PlotWidget, plot
from plot_pyqtgraph import DynamicPlotter
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import os

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        #Load the UI Page
        uic.loadUi('mainwindow1.ui', self)

        self.combo = self.findChild(QComboBox, "waveform")
        self.combo.addItem('Senóide')
        self.combo.addItem('Degrau')
        self.combo.addItem('Quadrada')
        self.combo.addItem('Dente de serra')
        self.combo.addItem('Sinal aleatório')

        self.waveform1 = 'sinusoidal'
        self.frequency1 = 0.5
        self.offset1 = 0
        self.amplitude1 = 5
        self.min_amplitude1 = 1
        self.t_min1 = 2
        self.t_max1 = 10

        self.apply.clicked.connect(self.apply_was_clicked)
        self.reset.clicked.connect(self.reset_was_clicked)    

        self.dp = DynamicPlotter(widget=self.widget, sampleinterval=0.05, timewindow=10.0, frequency=0.5, amplitude=self.amplitude1, offset=0, waveform='Senóide', min_amplitude=-2, t_min=20, t_max=50)
        # self.dp.showMaximized()


    def apply_was_clicked(self):
        print(self.waveform1, self.frequency1, self.offset1, self.amplitude1, self.min_amplitude1, self.t_min1, self.t_max1)
        if self.waveform.currentText():
            self.waveform1 = self.waveform.currentText()
        if self.frequency.text():
            self.frequency1 = float(self.frequency.text())
        if self.offset.text():
            self.offset1 = float(self.offset.text())
        if self.max_amp.text():
            self.amplitude1 = float(self.max_amp.text())
        if self.min_amp.text():
            self.min_amplitude1 = float(self.min_amp.text())
        if self.ti.text():
            self.t_min1 = float(self.ti.text())
        if self.tf.text():
            self.t_max1 = float(self.tf.text())
        print(self.waveform1, self.frequency1, self.offset1, self.amplitude1, self.min_amplitude1, self.t_min1, self.t_max1)
        self.dp.updateParameters(self.frequency1, self.amplitude1, self.offset1, 
                                self.waveform1, self.min_amplitude1, self.t_min1, self.t_max1)
        

    def reset_was_clicked(self):
        print("Clicked!")

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()