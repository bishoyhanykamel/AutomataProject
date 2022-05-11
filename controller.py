# widgets
from PyQt5 import sip
from PyQt5.QtGui import QPen
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsSceneMouseEvent, QGraphicsTextItem
# project files
from DrawingClasses import *
from DrawingClasses import EdgeLabel
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
    create_label_for_state(new_state, graphic_scene)


# add alphabet parameter
def create_edge(edge_combo_box, start_state, end_state, line_item, alphabet, graphic_scene):
    global NUM_EDGES
    NUM_EDGES = NUM_EDGES + 1
    edge = Edge(NUM_EDGES, start_state, end_state, line_item, alphabet)
    edge_combo_box.addItem(f'{edge}')
    create_label_for_edge(alphabet, line_item, edge, graphic_scene)


def get_selected_state(combo_box):
    for state in State.STATES:
        if f'{state.get_name()}' == f'{combo_box.currentText()}':
            return state
        print(f'No state found by name: {state.get_name()}')


def get_selected_edge(combo_box):
    for ed in Edge.EDGES:
        if f'{ed.get_name()}' == f'{combo_box.currentText()}':
            return ed
        print(f'No edge found by name: {ed.get_name()}')


def remove_state(graphic_scene, state, state_combo_box):
    graphic_scene.removeItem(state.circle)
    graphic_scene.removeItem(state.get_label_item())
    # sip.delete(state.circle)
    state_combo_box.removeItem(state.get_number())
    state.delete_state()
    state_combo_box.clear()
    for state in State.STATES:
        state_combo_box.addItem(state.get_name())


def remove_edge(graphic_scene, edge, edge_combo_box):
    graphic_scene.removeItem(edge.get_line_item())
    delete_label_for_edge(edge)
    # sip.delete(item.get_line_item())
    edge_combo_box.removeItem(edge.get_number())
    edge.delete_edge()
    edge_combo_box.clear()
    for edge in Edge.EDGES:
        edge_combo_box.addItem(edge.get_name())


def create_label_for_edge(alphabet, line, edge, graphic_scene):
    label = EdgeLabel(alphabet, edge)
    label.set_graphics_scene(graphic_scene)
    label.show_label()
    line.set_label_item(label)
    pass


def create_label_for_state(state, graphic_scene):
    state_name = f'Q #{state.get_number()}'
    label = StateLabel(state_name, state)
    label.set_graphics_scene(graphic_scene)
    label.show_label()
    state.set_label_item(label)


def delete_label_for_edge(edge):
    edge.get_label_item().destroy_label()
    pass


def delete_label_for_state(state):
    state.get_label_item().destroy_label()


def update_label_for_edge(edge, graphic_scene):
    delete_label_for_edge(edge)
    create_label_for_edge(edge.get_alphabet(), edge, graphic_scene)
    pass


def update_label_for_states(graphic_scene):
    for state in State.STATES:
        if state:
            delete_label_for_state(state)
            create_label_for_state(state, graphic_scene)


def make_final_state(state, final=True):
    if final:
        state.circle.make_final()
        state.set_final(True)
    else:
        state.circle.make_not_final()
        state.set_final(False)
    pass


def test():
    nfa_states = dict()
    nfa_final_states = list()
    for state in State.STATES:

        if state.is_final():
            nfa_final_states.append(state.get_name())

        nfa_states[state.get_name()] = dict()
        for alphabet in Edge.ALPHABETS:
            nfa_states[state.get_name()][alphabet] = list()

    for edge in Edge.EDGES:
        parent = edge.get_parent_name()
        child = edge.get_child_name()
        alphabet = edge.get_alphabet()

        if parent not in nfa_states.keys():
            nfa_states[parent] = dict()

        if alphabet not in nfa_states[parent].keys():
            nfa_states[parent][alphabet] = list()

        nfa_states[parent][alphabet].append(child)

    # print(nfa_states)
    # print(nfa_final_states)

    convert_nfa_to_dfa(nfa_states, nfa_final_states)


def convert_nfa_to_dfa(nfa, nfa_final_state):
    new_states_list = []
    dfa = {}
    keys_list = list(x.get_name() for x in State.STATES)
    path_list = list(Edge.ALPHABETS)

    dfa[keys_list[0]] = {}
    for y in range(len(Edge.ALPHABETS) - 1):
        var = "".join(nfa[keys_list[0]][path_list[y]])
        dfa[keys_list[0]][path_list[y]] = var
        if var not in keys_list:
            new_states_list.append(var)
            keys_list.append(var)

    while len(new_states_list) != 0:
        dfa[new_states_list[0]] = {}
        for _ in range(len(new_states_list[0])):
            for i in range(len(path_list)):
                temp = []
                for j in range(len(new_states_list[0])):
                    temp += nfa[new_states_list[0][j]][path_list[i]]
                s = ""
                s = s.join(temp)
                if s not in keys_list:
                    new_states_list.append(s)
                    keys_list.append(s)
                dfa[new_states_list[0]][path_list[i]] = s

        new_states_list.remove(new_states_list[0])

    print("\nDFA :- \n")
    print(dfa)

    dfa_states_list = list(dfa.keys())
    dfa_final_states = []
    for x in dfa_states_list:
        for i in x:
            if i in nfa_final_state:
                dfa_final_states.append(x)
                break

    print("\nFinal states of the DFA are : ", dfa_final_states)
    pass
