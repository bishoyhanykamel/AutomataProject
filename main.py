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

    start_item = new_connection = None

    def __init__(self, graphicsView):
        QGraphicsScene.__init__(self)
        self.parent = graphicsView
        self.item = None
        self.setSceneRect(0, 0, self.WIDTH, self.HEIGHT)
        pass

    def control_point_at(self, pos):
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
            item = self.control_point_at(event.scenePos())
            if item:
                self.start_item = item
                self.new_connection = Connection(item, event.scenePos())
                self.addItem(self.new_connection)
                return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.new_connection:
            item = self.control_point_at(event.scenePos())
            if (item and item != self.start_item and
                    self.start_item.onLeft != item.onLeft):
                p2 = item.scenePos()
            else:
                p2 = event.scenePos()
            self.new_connection.set_p2(p2)
            return
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.new_connection:
            item = self.control_point_at(event.scenePos())
            if item and item != self.start_item:
                self.new_connection.set_end(item)
                if self.start_item.add_line(self.new_connection):
                    item.add_line(self.new_connection)
                    window.create_edge_creation_window(self.start_item, item, self.new_connection)
                else:
                    self.start_item.remove_line(self.new_connection)
                    self.removeItem(self.new_connection)
            else:
                self.removeItem(self.new_connection)
        self.start_item = self.new_connection = None
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
        self.cancelEdge_pushButton.clicked.connect(lambda: self.cancel_edge())
        self.saveEdge_pushButton.clicked.connect(lambda: self.save_edge())
        self.show()

    def save_edge(self):
        edge_alphabet = self.inputEdge_lineEdit.text()
        try:
            if len(edge_alphabet) <= 0:
                self.cancel_edge()
                return
        except:
            self.cancel_edge()
            return

        print(f'starting control point -> {self.startItem} - parent: {self.startItem.parent_state}')
        print(f'ending control point -> {self.endItem} - parent: {self.endItem.parent_state}')
        create_edge(window.selectEdge_comboBox, self.startItem.parent_state, self.endItem.parent_state, self.line,
                    edge_alphabet)

        self.close()
        pass

    def cancel_edge(self):
        self.startItem.remove_line(self.line)
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
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.stateEdit_dialog.setGeometry(0, 0, self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        # buttons
        self.cancel_btn.clicked.connect(lambda: self.close_window())
        self.save_btn.clicked.connect(lambda: self.save_state())
        self.delete_btn.clicked.connect(lambda: self.delete_state())
        self.show()

    def delete_state(self):
        remove_state(window.drawing_scene, self.state_to_edit, window.selectState_comboBox)
        self.close()

    def close_window(self):
        self.close()

    def save_state(self):
        self.close()

    def closeEvent(self, event):
        window.setEnabled(True)


class EdgeEditUI(QMainWindow):
    WINDOW_WIDTH = 360
    WINDOW_HEIGHT = 295
    UI_FILENAME = 'select_edge_box'
    TITLE = 'Edit edge'

    def __init__(self, edge):
        super(EdgeEditUI, self).__init__()
        uic.loadUi(f'ui/{self.UI_FILENAME}.ui', self)
        self.title = self.TITLE
        self.edge_to_edit = edge
        self.setFixedSize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.edgeEdit_dialog.setGeometry(0, 0, self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        # buttons
        self.cancel_btn.clicked.connect(lambda: self.close_window())
        self.delete_btn.clicked.connect(lambda: self.delete_edge())
        self.show()

    def delete_edge(self):
        remove_edge(window.drawing_scene, self.edge_to_edit, window.selectEdge_comboBox)
        self.close()

    def close_window(self):
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
        self.title = 'NFA to DFA Converter'
        self.centralwidget.setGeometry(0, 0, self.WINDOW_WIDTH, self.WINDOW_HEIGHT)

        drawing_scene = GraphicScene(self.drawing_graphicsView)
        self.drawing_scene = drawing_scene
        self.drawing_graphicsView.setScene(drawing_scene)
        self.addState_btn.clicked.connect(lambda: create_state(drawing_scene, self.selectState_comboBox))
        self.editState_btn.clicked.connect(self.edit_state_window)
        self.editEdge_btn.clicked.connect(self.edit_edge_window)
        self.create_edge_ui = None
        self.edit_state_ui = None
        self.edit_edge_ui = None
        self.show()

    def create_edge_creation_window(self, start_item, end_item, line):
        self.create_edge_ui = EdgeCreationUI(start_item, end_item, line)
        self.setEnabled(False)

    def edit_state_window(self):
        # if condition to check selection of combobox
        # state = self.selectState_comboBox.
        selected_state = get_selected_state(self.selectState_comboBox)
        self.edit_state_ui = StateEditUI(selected_state)
        self.setEnabled(False)
        pass

    def edit_edge_window(self):
        selected_edge = get_selected_edge(self.selectEdge_comboBox)
        self.edit_edge_ui = EdgeEditUI(selected_edge)
        self.setEnabled(False)
        pass


app = QApplication(sys.argv)
window = MainWindowUI()
app.exec_()
