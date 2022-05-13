# from PyQt5 import Qt
# drawing elements
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsItem
from PyQt5.QtCore import QRectF, QPoint, QLineF, QVariantAnimation, Qt, QPointF
from PyQt5.QtGui import QPainterPath, QBrush, QPen
from controller import *
import random


class Circle(QGraphicsEllipseItem):
    RECT_X = 50
    RECT_Y = 50

    CTRL_LEFT_X = -15
    CTRL_LEFT_Y = 13

    CTRL_RIGHT_X = 45
    CTRL_RIGHT_Y = 13

    CTRL_LEFTTOP_X = 0
    CTRL_LEFTTOP_Y = -12

    CTRL_RIGHTTOP_X = 30
    CTRL_RIGHTTOP_Y = -12

    CTRL_LEFTDOWN_X = 30
    CTRL_LEFTDOWN_Y = 41

    CTRL_RIGHTDOWN_X = -2
    CTRL_RIGHTDOWN_Y = 40

    def __init__(self, state, dfa=False):
        QGraphicsEllipseItem.__init__(self)
        self.state = state
        self.anim = QVariantAnimation()
        self.setRect(QRectF(-10, -10, self.RECT_X, self.RECT_Y))
        self.make_not_final()
        self.setFlag(self.ItemIsMovable)
        self.control_points = []
        self.dfa = dfa
        self.final = False
        self.add_control_point(self.CTRL_LEFT_X, self.CTRL_LEFT_Y, self.state)
        self.add_control_point(self.CTRL_RIGHT_X, self.CTRL_RIGHT_Y, self.state)
        if dfa:
            self.add_control_point(self.CTRL_LEFTTOP_X, self.CTRL_LEFTTOP_Y, self.state)
            self.add_control_point(self.CTRL_RIGHTTOP_X, self.CTRL_RIGHTTOP_Y, self.state)
            self.add_control_point(self.CTRL_LEFTDOWN_X, self.CTRL_LEFTDOWN_Y, self.state)
            self.add_control_point(self.CTRL_RIGHTDOWN_X, self.CTRL_RIGHTDOWN_Y, self.state)
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
        self.final = True
        pass

    def make_not_final(self):
        pen = QPen(Qt.black)
        pen.setWidth(2)
        self.setPen(pen)
        self.final = False
        pass

    def get_control_points(self):
        return self.control_points

    def get_control_point(self):
        if self.dfa:
            if len(self.control_points[0].lines) <= 1:
                return self.control_points[0], self.control_points[0].pos()
            elif len(self.control_points[1].lines) <= 1:
                return self.control_points[1], self.control_points[1].pos()
            elif len(self.control_points[2].lines) <= 1:
                return self.control_points[2], self.control_points[2].pos()
            elif len(self.control_points[3].lines) <= 1:
                return self.control_points[3], self.control_points[3].pos()
            elif len(self.control_points[4].lines) <= 1:
                return self.control_points[4], self.control_points[4].pos()
            else:
                return self.control_points[5], self.control_points[5].pos()

    def get_diff_point(self, current_point):
        for point in self.control_points:
            if current_point == point:
                continue
            else:
                return point, point.pos()

    """
    def mousePressEvent(self, event):
        if self.dfa:
            self.setBrush(QBrush(Qt.lightGray))
            pen = QPen(Qt.green)
            if self.final:
                pen.setWidth(5)
            else:
                pen.setWidth(2)
            self.setPen(pen)
            #self.setPos(event.scenePos())

    def mouseReleaseEvent(self, event):
        if self.dfa:
            self.setBrush(QBrush(Qt.white))
            pen = QPen(Qt.black)
            if self.final:
                pen.setWidth(5)
            else:
                pen.setWidth(2)
            self.setPen(pen)
            #self.setPos(event.scenePos())

    def mouseMoveEvent(self, event):
        if event.button() == Qt.LeftButton and self.dfa:
            self.setPos(event.scenePos())
    """


class Connection(QGraphicsLineItem):
    LABEL_OFFSET = 0

    def __init__(self, start, p2, control_point=None):
        super().__init__()
        if type(control_point) is QPointF:
            self.start = start
            self.end = p2
            self._line = QLineF(start.pos(), p2.pos())
            self.p1 = start.pos()
            self.p2 = p2.pos()
        else:
            self.start = start
            self.end = None
            self._line = QLineF(start.scenePos(), p2)
            self.p1 = start.scenePos()
            self.p2 = p2
        self.label_item = None
        self.setLine(self._line)

    def get_p1(self):
        return self.p1

    def get_p2(self):
        return self.p2

    def get_mid_x(self):
        x = (self._line.x1() + self._line.x2()) / 2
        return x + self.LABEL_OFFSET
        pass

    def get_mid_y(self):
        y = (self._line.y1() + self._line.y2()) / 2
        return y + self.LABEL_OFFSET
        pass

    def control_points(self):
        return self.start, self.end

    def set_p2(self, p2):
        self._line.setP2(p2)
        self.p2 = p2
        self.setLine(self._line)

    def set_start(self, start):
        self.start = start
        self.update_line(start)

    def set_end(self, end):
        self.end = end
        self.update_line(end)

    def set_label_item(self, label):
        self.label_item = label

    def get_label_item(self):
        return self.label_item

    def update_line(self, source):
        if source == self.start:
            self._line.setP1(source.scenePos())
            self.p1 = source.scenePos()
        else:
            self._line.setP2(source.scenePos())
            self.p2 = source.scenePos()
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
                line.get_label_item().update_label_position()
            return super().itemChange(change, value)
        except Exception as e:
            print(e)
            return


class Label(QGraphicsTextItem):
    GRAPHICS_SCENE = None

    def __init__(self, alphabet, item):
        super().__init__()
        self.item = item
        self.setEnabled(True)
        self.setDefaultTextColor(Qt.black)
        self.setPlainText(alphabet)

        self.item.set_label_item(self)
        pass

    def set_graphics_scene(self, graphics_scene):
        self.GRAPHICS_SCENE = graphics_scene

    def show_label(self):
        self.GRAPHICS_SCENE.addItem(self)

    def hide_label(self):
        self.GRAPHICS_SCENE.removeItem(self)

    def destroy_label(self):
        self.hide_label()
        self.item.set_label_item(None)
        del self


class EdgeLabel(Label):
    def __init__(self, alphabet, item):
        super().__init__(alphabet, item)
        self.update_label_position()
        pass

    def update_label_position(self):
        self.setX(self.item.get_line_item().get_mid_x())
        self.setY(self.item.get_line_item().get_mid_y())


class StateLabel(Label):
    def __init__(self, alphabet, item):
        super().__init__(alphabet, item)
        self.update_label_position()
        pass

    def update_label_position(self):
        self.setX(self.item.get_circle().x())
        self.setY(self.item.get_circle().y())
