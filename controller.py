# widgets
from PyQt5.QtGui import QPen
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsSceneMouseEvent
# project files
from ModelClasses import *
from logic import *

# global variables
NUM_STATES = -1
NUM_EDGES = -1


def create_state(graphic_scene, state_combo_box):
    global NUM_STATES
    NUM_STATES = NUM_STATES + 1
    circle = Circle()
    graphic_scene.addItem(circle)
    new_state = State(NUM_STATES, circle)
    state_combo_box.addItem(f'{new_state}')


# add alphabet parameter
def add_edge(edge_combo_box, start_state, end_state, line_item, inp='a'):
    global NUM_EDGES
    NUM_EDGES = NUM_EDGES + 1
    edge = Edge(NUM_EDGES, start_state, end_state, line_item, inp)
    edge_combo_box.addItem(f'{edge}')
    pass


# TODO
def make_final_state(state, graphic_scene):
    pass


def remove_state():
    pass


def remove_edge():
    pass


def edit_state():
    pass


def edit_edge():
    pass
