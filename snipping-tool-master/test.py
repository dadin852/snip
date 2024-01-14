import sys
from PyQt5 import QtWidgets
import SnippingTool2, utils

class Test:
    def __init__(self):
        self.image = None
        self.tool = SnippingTool2.SnippingWidget()
        self.tool.returnToMainWindowSignal.connect(self.handleReturnToMainWindow)
    def handleReturnToMainWindow(self):
        # print("Returning to MainWindow")
        utils.scaledShow(self.tool.img)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    obj = Test()
    while True:
        cmd = input('Cmd: ')
        if cmd=='e': break
        elif cmd=='s':
            obj.tool.start()
        # elif cmd=='s':
        #     try:
        #     #     pass
        #     # except: pass
        #     # if True:
        #         pass
        #     except: pass
                
    # sys.exit(app.exec_())
