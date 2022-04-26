import wave
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg

import collections
import random
import time
import math
import numpy as np
from scipy import signal
from ControlLib import *

import asyncio
import websockets

class DynamicPlotter():

    def __init__(self, widget, sampleinterval=0.1, timewindow=100., size=(1130,541), frequency=0.5, amplitude=10.0, offset=0, waveform='sinusoidal', min_amplitude=0, t_min = 2.0, t_max = 10.0):
        # Data stuff
        self._interval = int(sampleinterval*1000)
        self._bufsize = int(timewindow/sampleinterval)
        self.databuffer = collections.deque([0.0]*self._bufsize, self._bufsize)
        self.x = np.linspace(0.0, timewindow, self._bufsize)
        self.y = np.zeros(self._bufsize, dtype=np.float)

        # self._bufsize = int(timewindow/sampleinterval)
        self.databuffer1 = collections.deque([0.0]*self._bufsize, self._bufsize)
        self.y1 = np.zeros(self._bufsize, dtype=np.float)

        # asyncio.run(self.get_output())
        
        # PyQtGraph stuff
        self.plt = pg.PlotWidget(widget)
        self.plt.resize(*size)
        self.plt.showGrid(x=True, y=True)
        self.plt.setLabel('left', 'amplitude', 'V')
        self.plt.setLabel('bottom', 'time', 's')
        self.curve = self.plt.plot(self.x, self.y, pen=(255,0,0))

        self.curve1 = self.plt.plot(self.x, self.y1, pen=(0,255,0))
        
        # QTimer
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updateplot)
        self.timer.start(self._interval)

        self.frequency = frequency 
        self.amplitude = amplitude
        self.offset = offset
        self.waveform = waveform
        self.min_amplitude = min_amplitude

        self.t_min = t_min
        self.t_max = t_max
        self.timewindow = timewindow
        self.time_flag = time.time()
        self.t_prs = random.uniform(self.time_flag + t_min, self.time_flag + t_max)
        self.amplitude1 = random.uniform(self.min_amplitude, self.amplitude)

    def getdata(self):
        if self.waveform == 'Senóide':
            new = self.amplitude*math.sin(time.time()*self.frequency*2*math.pi) + self.offset 
        elif self.waveform == 'Degrau':
            new = self.amplitude 
        elif self.waveform == 'Quadrada':
            new = self.amplitude*signal.square(2*math.pi*self.frequency*time.time()) + self.offset 
        elif self.waveform == 'Dente de serra':
            new = self.amplitude*signal.sawtooth(2*np.pi*self.frequency*time.time()) + self.offset 
        elif self.waveform == 'Sinal aleatório':
            # print(self.time_flag, self.t_prs)
            if self.time_flag >= self.t_prs:
                self.time_flag = time.time()
                self.t_prs = random.uniform(self.time_flag + self.t_min, self.time_flag + self.t_max)
                self.amplitude1 = random.uniform(self.min_amplitude, self.amplitude)
            else:
                self.time_flag = self.time_flag + 1
            new = self.amplitude1*signal.square(2*math.pi*self.frequency*time.time()) + self.offset
        return new

    def getdata1(self):
        return self.amplitude*math.cos(time.time()*self.frequency*2*math.pi) + self.offset
    
    def updateParameters(self, frequency, amplitude, offset, waveform, min_amplitude, t_min, t_max):
        self.frequency = frequency 
        self.amplitude = amplitude
        self.offset = offset
        self.waveform = waveform
        self.min_amplitude = min_amplitude

        self.t_min = t_min
        self.t_max = t_max

    def updateplot(self):
        self.databuffer.append( self.getdata() )
        self.y[:] = self.databuffer
        # self.x[:] = self.x + 0.05
        self.curve.setData(self.x, self.y)

        self.databuffer1.append( self.getdata1() )
        self.y1[:] = self.databuffer1
        self.curve1.setData(self.x, self.y1)

    async def echo(self, websocket):
        async for message in websocket:
            await websocket.send(message)

    async def get_output(self):
        async with websockets.serve(self.echo, "localhost", 8765):
            await asyncio.Future()  # run forever

    def run(self):
        self.app.exec()

if __name__ == '__main__':

    m = DynamicPlotter(sampleinterval=0.05, timewindow=10.0, frequency=0.5, amplitude=10.0, offset=0, min_amplitude=-5, t_min=2, t_max=10)
    m.run()