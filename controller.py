# widgets
from PyQt5 import sip
from PyQt5.QtGui import QPen
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsSceneMouseEvent
# project files
from DrawingClasses import *
from logic import *

# global variables
NUM_STATES = -1
NUM_EDGES = -1


def create_state(graphic_scene, state_combo_box):
    global NUM_STATES
    NUM_STATES = NUM_STATES + 1
    new_state = State(NUM_STATES)
    circle = Circle(new_state)
    graphic_scene.addItem(circle)
    new_state.connect_circle(circle)
    state_combo_box.addItem(f'{new_state}')


# add alphabet parameter
def create_edge(edge_combo_box, start_state, end_state, line_item, inp='a'):
    global NUM_EDGES
    NUM_EDGES = NUM_EDGES + 1
    edge = Edge(NUM_EDGES, start_state, end_state, line_item, inp)
    edge_combo_box.addItem(f'{edge}')


def get_selected_state(combo_box):
    for state in State.STATES:
        if f'{state.get_name()}' == f'{combo_box.currentText()}':
            return state
        print(f'No state found by name: {state.get_name()}')


def remove_state(graphic_scene, state, state_combo_box):
    graphic_scene.removeItem(state.circle)
    # sip.delete(state.circle)
    state_combo_box.removeItem(state.get_number())
    state.delete_state()
    state_combo_box.clear()
    for state in State.STATES:
        state_combo_box.addItem(state.get_name())


def get_selected_edge(combo_box):
    for ed in Edge.EDGES:
        if f'{ed.get_name()}' == f'{combo_box.currentText()}':
            return ed
        print(f'No edge found by name: {ed.get_name()}')


def remove_edge(graphic_scene, edge, edge_combo_box):
    graphic_scene.removeItem(edge.get_line_item())
    # sip.delete(edge.get_line_item())
    edge_combo_box.removeItem(edge.get_number())
    edge.delete_edge()
    edge_combo_box.clear()
    for edge in Edge.EDGES:
        edge_combo_box.addItem(edge.get_name())


def create_label_for_edge(alphabet, edge):
    pass


def make_final_state(state, final = True):
    if final:
        state.circle.make_final()
        state.set_final(True)
    else:
        state.circle.make_not_final()
        state.set_final(False)
    pass


def edit_state():
    pass


def edit_edge():
    pass
