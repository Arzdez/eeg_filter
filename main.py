import numpy as np
import matplotlib.pyplot as plt 

from filter import EegFilter
from stream_processing import stream_filter

from pgc import txt_edit




X = np.loadtxt(r"C:\Users\insec\Desktop\eeg_filter\281-10.07.18\baseline.txt")
path = r"C:\Users\insec\Desktop\eeg_filter\281-10.07.18"
parh_arch = r"C:\Users\insec\Desktop\eeg_filter\arch"
#stream_filter(path, ploting=True)

txt_edit.txt_to_zip(path, parh_arch)


