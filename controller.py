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




def create_state(graphicScene, stateComboBox):
    global NUM_STATES
    NUM_STATES = NUM_STATES + 1
    circle = Circle()
    graphicScene.addItem(circle)
    new_state = State(NUM_STATES, circle)
    stateComboBox.addItem(f'{new_state}')


# add alphabet parameter
def add_edge(edgeComboBox, startState, endState, lineItem, inp = 'a'):
    global NUM_EDGES
    NUM_EDGES = NUM_EDGES + 1
    edge = Edge(NUM_EDGES, startState, endState, lineItem, inp)
    edgeComboBox.addItem(f'{edge}')
    pass


# TODO
def make_final_state(state, graphicScene):
    pass



def remove_state():
    pass

def remove_edge():
    pass

def edit_state():
    pass

def edit_edge():
    pass
