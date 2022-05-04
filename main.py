# main window imports
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog
from PyQt5 import uic
import sys
# model file for UI drawing/control
from controller import *


class GraphicScene(QGraphicsScene):
    WIDTH = 956 - 15
    HEIGHT = 566 - 15
    START_X = 10
    START_Y = 10

    startItem = newConnection = None

    def __init__(self, graphicsView):
        QGraphicsScene.__init__(self)
        self.parent = graphicsView
        self.item = None
        self.setSceneRect(0, 0, self.WIDTH, self.HEIGHT)
        pass

    def controlPointAt(self, pos):
        mask = QPainterPath()
        mask.setFillRule(Qt.WindingFill)
        for item in self.items(pos):
            if mask.contains(pos):
                return
            if isinstance(item, ControlPoint):
                return item
            if not isinstance(item, Connection):
                mask.addPath(item.shape().translated(item.scenePos()))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            item = self.controlPointAt(event.scenePos())
            if item:
                self.startItem = item
                self.newConnection = Connection(item, event.scenePos())
                self.addItem(self.newConnection)
                return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.newConnection:
            item = self.controlPointAt(event.scenePos())
            if (item and item != self.startItem and
                    self.startItem.onLeft != item.onLeft):
                p2 = item.scenePos()
            else:
                p2 = event.scenePos()
            self.newConnection.setP2(p2)
            return
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.newConnection:
            item = self.controlPointAt(event.scenePos())
            if item and item != self.startItem:
                self.newConnection.setEnd(item)
                if self.startItem.addLine(self.newConnection):
                    item.addLine(self.newConnection)
                    window.createEdgeCreationWindow(self.startItem, item, self.newConnection)
                else:
                    self.startItem.removeLine(self.newConnection)
                    self.removeItem(self.newConnection)
            else:
                self.removeItem(self.newConnection)
        self.startItem = self.newConnection = None
        super().mouseReleaseEvent(event)


# window classes shown to users

class EdgeCreationUI(QMainWindow):
    WINDOW_WIDTH = 360
    WINDOW_HEIGHT = 296

    def __init__(self, startItem, endItem, line):
        super(EdgeCreationUI, self).__init__()
        uic.loadUi('ui/create_edge.ui', self)
        self.title = 'Edge creation'
        self.startItem = startItem
        self.endItem = endItem
        self.line = line
        self.setFixedSize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        self.edge_dialog.setGeometry(0, 0, self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.cancelEdge_pushButton.clicked.connect(lambda: self.cancelEdge())
        self.saveEdge_pushButton.clicked.connect(lambda: self.saveEdge())
        self.show()

    def saveEdge(self):
        print(f'starting control point -> {self.startItem} - parent: {self.startItem.parentState}')
        print(f'ending control point -> {self.endItem} - parent: {self.endItem.parentState}')
        edge_alphabet = self.inputEdge_lineEdit.text()
        # check if user enters no text
        add_edge(window.selectEdge_comboBox, self.startItem.parentState, self.endItem.parentState, self.line,
                 edge_alphabet)

        self.close()
        pass

    def cancelEdge(self):
        self.startItem.removeLine(self.line)
        self.close()

    def closeEvent(self, event):
        window.setEnabled(True)


class StateEditUI(QMainWindow):
    WINDOW_WIDTH = 360
    WINDOW_HEIGHT = 319
    UI_FILENAME = 'select_state_box'
    TITLE = 'Edit state'

    def __init__(self, state):
        super(StateEditUI, self).__init__()
        uic.loadUi(f'ui/{self.UI_FILENAME}.ui', self)
        self.title = self.TITLE
        self.state_to_edit = state
        self.setFixedSize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        self.stateEdit_dialog.setGeometry(0, 0, self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.cancel_btn.clicked.connect(lambda: self.closeWindow())
        self.save_btn.clicked.connect(lambda: self.saveState())
        self.show()

    def deleteState(self):
        self.close()

    def closeWindow(self):
        self.close()

    def saveState(self):
        self.close()

    def closeEvent(self, event):
        window.setEnabled(True)


class MainWindowUI(QMainWindow):
    WINDOW_WIDTH = 1025
    WINDOW_HEIGHT = 750

    def __init__(self):
        super(MainWindowUI, self).__init__()
        uic.loadUi('ui/final2.ui', self)
        self.setFixedSize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        self.title = "NFA to DFA Converter"
        self.centralwidget.setGeometry(0, 0, self.WINDOW_WIDTH, self.WINDOW_HEIGHT)

        drawing_scene = GraphicScene(self.drawing_graphicsView)
        self.drawing_scene = drawing_scene
        self.drawing_graphicsView.setScene(drawing_scene)
        self.addState_btn.clicked.connect(lambda: create_state(drawing_scene, self.selectState_comboBox))
        self.editState_btn.clicked.connect(self.editStateWindow)
        self.editEdge_btn.clicked.connect(self.editEdgeWindow)
        self.createEdgeUI = None
        self.editStateUI = None
        self.editEdgeUI = None
        self.show()

    def createEdgeCreationWindow(self, startItem, endItem, line):
        self.createEdgeUI = EdgeCreationUI(startItem, endItem, line)
        self.setEnabled(False)

    def editStateWindow(self):
        # if condition to check selection of combobox
        # state = self.selectState_comboBox.
        self.editStateUI = StateEditUI('test state')
        self.setEnabled(False)
        pass

    def editEdgeWindow(self):
        pass


app = QApplication(sys.argv)
window = MainWindowUI()
app.exec_()
