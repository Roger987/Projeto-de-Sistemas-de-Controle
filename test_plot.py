from plot_pyqtgraph import DynamicPlotter

m = DynamicPlotter(sampleinterval=0.05, timewindow=10.0, frequency=0.5, amplitude=5.0, offset=0, waveform='pseudoRandomSignal', min_amplitude=-2, t_min=20, t_max=50)
m.run()