import sys

from InteractiveWaves import InteractiveWaves
import waveSelectionUI as ws

#from PyQt5.QtGui import QDrag, QColor
#from PyQt5.QtCore import Qt, QMimeData, pyqtSignal 
from PyQt5.QtWidgets import QApplication
                             

if __name__ == "__main__":
    app = QApplication(sys.argv)

    a = InteractiveWaves()
    print("moep")
    wave_select = ws.WaveSelect(a)
    #wave_select.show()
    #a.reset()
    #test_action = np.array([[2, 1], [3, 5]])
    #a.step(test_action)

    #ex = Window()
    #ex.show()

    sys.exit(app.exec_())
    
