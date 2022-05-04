from PyQt5 import Qt
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

    def __init__(self):
        QGraphicsEllipseItem.__init__(self)
        self.anim = QVariantAnimation()
        self.setRect(QRectF(-10, -10, self.RECT_X, self.RECT_Y))
        pen = QPen(Qt.black)
        pen.setWidth(2)
        self.setPen(pen)
        self.setFlag(self.ItemIsMovable)
        #self.control_points = []
        self.addControlPoint(self.CTRL_LEFT_X, self.CTRL_LEFT_Y, self)
        self.addControlPoint(self.CTRL_RIGHT_X, self.CTRL_RIGHT_Y, self)
        pass

    def addControlPoint(self, x, y, parentState):
        pen = QPen(Qt.red)
        pen.setWidth(2)
        control_left = ControlPoint(self, True, parentState)
        #self.control_points.append(control_left)
        control_left.setPen(pen)
        control_left.setX(x)
        control_left.setY(y)
        pass


class Connection(QGraphicsLineItem):
    def __init__(self, start, p2):
        super().__init__()
        self.start = start
        self.end = None
        self._line = QLineF(start.scenePos(), p2)
        self.setLine(self._line)

    def controlPoints(self):
        return self.start, self.end

    def setP2(self, p2):
        self._line.setP2(p2)
        self.setLine(self._line)

    def setStart(self, start):
        self.start = start
        self.updateLine()

    def setEnd(self, end):
        self.end = end
        self.updateLine(end)

    def updateLine(self, source):
        if source == self.start:
            self._line.setP1(source.scenePos())
        else:
            self._line.setP2(source.scenePos())
        self.setLine(self._line)



class ControlPoint(QGraphicsEllipseItem):
    COUNTER = 0
    def __init__(self, parent, onLeft, parentState):
        super().__init__(-5, -5, 10, 10, parent)
        self.onLeft = onLeft
        self.lines = []
        self.setFlags(self.ItemSendsScenePositionChanges)
        self.parentState = parentState

    def addLine(self, lineItem):
        self.lines.append(lineItem)
        return True

    def removeLine(self, lineItem):
        for existing in self.lines:
            if existing.controlPoints() == lineItem.controlPoints():
                self.scene().removeItem(existing)
                self.lines.remove(existing)
                return True
        return False

    def itemChange(self, change, value):
        for line in self.lines:
            line.updateLine(self)
        return super().itemChange(change, value)
