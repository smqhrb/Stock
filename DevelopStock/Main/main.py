
import math
from PyQt5 import QtWidgets, QtCore

PI =3.14
def main():
    a =math.sin(2*PI)
    print("PI:",a)
    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QWidget()
    widget.resize(360, 360)
    widget.setWindowTitle("Hello, PyQt5!")
    widget.show()
    sys.exit(app.exec_())

if __name__=="__main__":
    main()

