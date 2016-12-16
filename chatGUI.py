import sys
from PyQt4 import QtGui, QtCore
import threading
import socket
import time
import Queue

class initWindow(QtGui.QDialog):

   def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setGeometry(50,50,500,200)
        self.setWindowTitle('PyChat Setup')
        self.setWindowIcon(QtGui.QIcon('favicon.png'))

        myLayout = QtGui.QGridLayout()
        myLayout.columnCount = 4
        myLayout.rowCount = 4

        # determine if listening or connecting
        self.state = "Listen"  # default, only modified if we click a radio button
        
        self.b1 = QtGui.QRadioButton("Listen")
        self.b1.setChecked(True)
        self.b1.toggled.connect(lambda:self.setState(self.b1))
        myLayout.addWidget(self.b1)

        self.b2 = QtGui.QRadioButton("Connect")
        self.b2.setChecked(False)
        self.b2.toggled.connect(lambda:self.setState(self.b2))
        myLayout.addWidget(self.b2)

        self.b3 = QtGui.QPushButton('Ok', self)   # first argument is the text
        self.b3.clicked.connect(self.accept)  
        myLayout.addWidget(self.b3, 2, 2)

        # get the IP address 
        self.IPInput = QtGui.QLineEdit()
        self.IPInput.setPlaceholderText('IP address')
        myLayout.addWidget(self.IPInput, 0, 1)

        # get the socket
        self.SocketInput = QtGui.QLineEdit()
        self.SocketInput.setPlaceholderText('Socket')
        myLayout.addWidget(self.SocketInput, 1, 1)

        self.setLayout(myLayout)

   def setState(self,b):
	
       if b.text() == "Listen":
           if b.isChecked() == True:
               self.state = "Listen"
           else:
               self.state = "Connect"
       else:
           if b.isChecked() == True:
               self.state = "Connect"
           else:
               self.state = "Listen"

   def accept(self):
       self.IP = self.IPInput.text()
       self.Socket = self.SocketInput.text()
       self.close()

class Window(QtGui.QMainWindow):

    def __init__(self):
        super(Window,self).__init__()
        self.setGeometry(50,50,500,300)
        self.setWindowTitle('PyChat')
        self.setWindowIcon(QtGui.QIcon('favicon.png'))

        self.dialog = initWindow()
        self.dialog.exec_()
        # or do self.dialog.show() for non-blocking

        # add an exit feature
        exitAction = QtGui.QAction('&Quit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Leave the App')
        exitAction.triggered.connect(self.close_application)

        # menu part of exit feature
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(exitAction)
        
        self.home()
        time.sleep(1)
        self.launch_threads()

    def home(self):

        # text display box
        self.textDisp = QtGui.QTextEdit()
        self.textDisp.setReadOnly(True)
        self.setCentralWidget(self.textDisp)

        # text input box
        self.textInputWidget = QtGui.QLineEdit()
        self.textInputWidget.returnPressed.connect(self.addInput)
        self.textInputWidget.setPlaceholderText('input here')
        self.input = QtGui.QDockWidget('', self)
        self.input.setFeatures(QtGui.QDockWidget.DockWidgetMovable)
        self.input.setWidget( self.textInputWidget)
        self.input.setFloating(False)
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self.input)

        # this should always be last
        self.show()
        print('GUI done')
        
    def launch_threads(self):

       print('just entered launch_threads')
        
       my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
       my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
       self.send_queue = Queue.Queue()
       self.recv_queue = Queue.Queue()
        
       if self.dialog.state == 'Listen':

          print('just entered launcher')
          self.textDisp.append('Listening for a connection')
          accept_from  = (self.dialog.IP, int(self.dialog.Socket))
          my_socket.bind(accept_from)
          my_socket.listen(1)
          conn, addr = my_socket.accept()
          self.textDisp.append('Client connected from ' + addr[0] +':'+str(addr[1]))
          self.listen_thread  = ListenThread(conn, addr[0], self.textDisp)
          self.listen_thread.start()
          self.send_thread = SendThread(conn, self.send_queue)
          self.send_thread.start()
          print('got to the bottom of the listen launcher')
                                             
       else:
          my_socket.connect((self.dialog.IP, int(self.dialog.Socket)))
          self.textDisp.append('Connected to ' + self.dialog.IP +':'+ str(self.dialog.Socket))
          self.listen_thread = ListenThread(my_socket, self.dialog.IP, self.textDisp)
          self.listen_thread.start()
          self.send_thread = SendThread(my_socket, self.send_queue)
          self.send_thread.start()
          print('got to the bottom of the sending launcher')

    def addInput(self):
        # skip empty text
        if self.textInputWidget.text():
            self.myText = self.textInputWidget.text()
            self.send_queue.put(str(self.myText))
            self.textDisp.append('You: '+ self.myText)
            # clear the QLineEdit for new input
            self.textInputWidget.clear()
            print('registering input')
        
    def close_application(self):
        # add functionality to see if we want to exit
        choice = QtGui.QMessageBox.question(self,'Exit','Are you sure you want to exit?',
                                            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)

        if choice == QtGui.QMessageBox.Yes:
            sys.exit()
        else:
            pass
        
class ListenThread(QtCore.QThread):

    def __init__(self, conn, addr, textDisp):
        QtCore.QThread.__init__(self)
        self.conn = conn
        self.addr = addr
        self.textDisp = textDisp

    def __del__(self):
        self.wait()

    def run(self):
        while True:
            data = self.conn.recv(4096)
            if data:
               print data
               self.textDisp.append(self.addr + ': ' + data)

class SendThread(QtCore.QThread):

    def __init__(self, conn, send_queue):
        QtCore.QThread.__init__(self)
        self.conn = conn
        self.send_queue = send_queue

    def __del__(self):
        self.wait()

    def run(self):
       while True:
          myText = self.send_queue.get()
          self.conn.sendall(myText)   

def run(): 
    app = QtGui.QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())

if __name__ == '__main__':
    run()
