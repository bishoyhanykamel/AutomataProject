#from PyQt5 import Qt
# drawing elements
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsItem
from PyQt5.QtCore import QRectF, QPoint, QLineF, QVariantAnimation, Qt
from PyQt5.QtGui import QPainterPath
from controller import *


class Circle(QGraphicsEllipseItem):
    RECT_X = 50
    RECT_Y = 50

    CTRL_LEFT_X = -15
    CTRL_LEFT_Y = 13

    CTRL_RIGHT_X = 45
    CTRL_RIGHT_Y = 13

    def __init__(self, state):
        QGraphicsEllipseItem.__init__(self)
        self.state = state
        self.anim = QVariantAnimation()
        self.setRect(QRectF(-10, -10, self.RECT_X, self.RECT_Y))
        self.make_not_final()
        self.setFlag(self.ItemIsMovable)
        self.control_points = []
        self.add_control_point(self.CTRL_LEFT_X, self.CTRL_LEFT_Y, self.state)
        self.add_control_point(self.CTRL_RIGHT_X, self.CTRL_RIGHT_Y, self.state)
        pass

    def add_control_point(self, x, y, parent_state):
        pen = QPen(Qt.red)
        pen.setWidth(2)
        control_point = ControlPoint(self, True, parent_state)
        control_point.setPen(pen)
        control_point.setX(x)
        control_point.setY(y)
        self.control_points.append(control_point)
        pass

    def make_final(self):
        pen = QPen(Qt.black)
        pen.setWidth(5)
        self.setPen(pen)
        pass

    def make_not_final(self):
        pen = QPen(Qt.black)
        pen.setWidth(2)
        self.setPen(pen)
        pass


class Connection(QGraphicsLineItem):
    def __init__(self, start, p2):
        super().__init__()
        self.start = start
        self.end = None
        self._line = QLineF(start.scenePos(), p2)
        self.setLine(self._line)

    def control_points(self):
        return self.start, self.end

    def set_p2(self, p2):
        self._line.setP2(p2)
        self.setLine(self._line)

    def set_start(self, start):
        self.start = start
        self.update_line()

    def set_end(self, end):
        self.end = end
        self.update_line(end)

    def update_line(self, source):
        if source == self.start:
            self._line.setP1(source.scenePos())
        else:
            self._line.setP2(source.scenePos())
        self.setLine(self._line)


class ControlPoint(QGraphicsEllipseItem):
    COUNTER = 0

    def __init__(self, parent, on_left, parent_state):
        super().__init__(-5, -5, 10, 10, parent)
        self.onLeft = on_left
        self.lines = []
        self.setFlags(self.ItemSendsScenePositionChanges)
        self.parent_state = parent_state

    def add_line(self, line_item):
        self.lines.append(line_item)
        return True

    def remove_line(self, line_item):
        for existing in self.lines:
            if existing.control_points() == line_item.control_points():
                self.scene().removeItem(existing)
                self.lines.remove(existing)
                return True
        return False

    def itemChange(self, change, value):
        try:
            for line in self.lines:
                line.update_line(self)
            return super().itemChange(change, value)
        except Exception as e:
            print(e)
            return
