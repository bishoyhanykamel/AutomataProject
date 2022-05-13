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
SEMAPHORE = False


def create_state(graphic_scene, state_combo_box, name=None):
    global NUM_STATES
    NUM_STATES = NUM_STATES + 1
    new_state = State(NUM_STATES, name)
    circle = Circle(new_state)
    graphic_scene.addItem(circle)
    new_state.connect_circle(circle)
    state_combo_box.addItem(f'{new_state.get_name()}')
    create_label_for_state(new_state, graphic_scene)
    return new_state


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


def get_selected_edge(combo_box):
    for ed in Edge.EDGES:
        if f'{ed.get_name()}' == f'{combo_box.currentText()}':
            return ed


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



def create_label_for_state(state, graphic_scene):
    state_name = f'{state.get_name()}'
    label = StateLabel(state_name, state)
    label.set_graphics_scene(graphic_scene)
    label.show_label()
    state.set_label_item(label)


def delete_label_for_edge(edge):
    edge.get_label_item().destroy_label()



def delete_label_for_state(state):
    state.get_label_item().destroy_label()


def update_label_for_edge(edge, graphic_scene):
    delete_label_for_edge(edge)
    create_label_for_edge(edge.get_alphabet(), edge, graphic_scene)



def update_label_for_state(graphic_scene, state):
    if state:
        delete_label_for_state(state)
        create_label_for_state(state, graphic_scene)


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



# ====================================== [ NFA DATA STRUCTURE ] =====================================================
def nfa_data_generator(drawing_scene, selectState_comboBox, selectEdge_comboBox):
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

    print(f'NFA DATA STRUCTURE: \n\t {nfa_states}')
    print(f'NFA FINAL STATES: \n\t {nfa_final_states}')
    get_dfa_states(nfa_states, nfa_final_states, drawing_scene, selectState_comboBox, selectEdge_comboBox)


def dfa_child_states(state, states_dict):
    new_state_dict = dict(list())

    # alphabet is a key, states is a list (value)
    for alphabet, states in states_dict[state]:
        # only 1 state
        new_state_name = ''
        if len(states) == 1:
            new_state_name = states[0]
        elif len(states) >= 2:
            new_state_name = ''.join(states)
        else:
            new_state_name = 'XX'

        new_state_dict[alphabet] = new_state_name

    return new_state_dict



# ============================ [ MAIN FUNCTION OF DFA GENERATION ] =====================================================
def get_dfa_states(nfa_states, nfa_final_states, drawing_scene, selectState_comboBox, selectEdge_comboBox):
    start_state = 'A'
    dfa_state_dict = dict(list())
    dfa_state_queue = ['A']
    current_state = dfa_state_queue[0]
    done_states = []
    get_dfa_child_states(current_state, nfa_states, dfa_state_dict, dfa_state_queue, done_states)

    while len(dfa_state_queue) >= 1:
        current_state = dfa_state_queue[0]
        if current_state == 'XX':
            state_dict = dict(list())
            for alphabet in Edge.ALPHABETS:
                state_dict[alphabet] = 'XX'
            dfa_state_queue.remove(current_state)
            done_states.append(current_state)
            dfa_state_dict[current_state] = state_dict

        elif len(current_state) == 1:
            get_dfa_child_states(current_state, nfa_states, dfa_state_dict, dfa_state_queue, done_states)

        else:
            dfa_state_dict[current_state] = dict()
            single_get_dfa_child_states(current_state, nfa_states, dfa_state_dict, dfa_state_queue, done_states)
    print(f'DFA DATA STRUCTURE: \n\t {dfa_state_dict}')
    return dfa_state_dict


# ====================================== [ DFA STATE GENERATORS ] =====================================================
# ======================================== [ HELPER FUNCTIONS ] =======================================================
def get_dfa_child_states(state, states_dict, dfa_states_dict, dfa_state_queue, done_states):
    state_dict = dict(list())
    for alphabet, states in states_dict[state].items():
        # only 1 state
        new_state_name = ''
        if len(states) == 1:
            new_state_name = states[0]
        elif len(states) >= 2:
            new_state_name = ''.join(states)
            new_state_name = ''.join(sorted(new_state_name))
        else:
            new_state_name = 'XX'

        if ''.join(sorted(new_state_name)) not in dfa_state_queue:
            if ''.join(sorted(new_state_name)) not in done_states:
                dfa_state_queue.append(''.join(sorted(new_state_name)))

        state_dict[alphabet] = new_state_name

    dfa_state_queue.remove(state)
    done_states.append(state)
    dfa_states_dict[state] = state_dict


# ======================================== [ HELPER FUNCTIONS ] =======================================================
def single_get_dfa_child_states(state, states_dict, dfa_states_dict, dfa_state_q, done_states):
    for alphabet in Edge.ALPHABETS:
        set_of_states = str()
        for single_state in state:
            set_of_states += ''.join(states_dict[single_state][alphabet])

        temp_str = ''
        for chr in set_of_states:
            if chr in temp_str:
                continue
            temp_str += chr

        dfa_states_dict[state][alphabet] = ''.join(sorted(temp_str))
        if dfa_states_dict[state][alphabet] not in dfa_state_q:
            if dfa_states_dict[state][alphabet] not in done_states:
                dfa_state_q.append(dfa_states_dict[state][alphabet])

    dfa_state_q.remove(state)
    done_states.append(state)



# ====================================== [ DRAWING DFA ] =====================================================
def draw_dfa(dfa_states, dfa_final_states, graphic_scene, state_combo, edge_combo):
    POSITIONS = {'A': [39.0, -12.0], 'B': [90.0, 388.0], 'C': [305.0, 72.0], 'D': [343.0, 532.0],
                 'E': [637.0, 32.0], 'F': [661.0, 428.0], 'G': [891.0, -22.0], 'H': [876.0, 308.0],
                 'I': [462.0, 171.0], 'J': [469.0, 362.0], 'K': None}

    created_states = []
    current_pos = 'A'

    for dfa_state in State.STATES:
        dfa_state.delete_state()
    State.STATES.clear()

    for edge in Edge.EDGES:
        edge.delete_edge()
    Edge.EDGES.clear()

    state_combo.clear()
    edge_combo.clear()
    graphic_scene.clear()

    # creating DFA states
    for dfa_state in dfa_states.keys():
        new_state = create_state(graphic_scene, state_combo, name=f'{dfa_state}')

        # final states
        for x in dfa_final_states:
            if dfa_state == x:
                make_final_state(new_state)
                dfa_final_states.remove(x)
                break

        # pre-defined positions
        if current_pos != 'K':
            new_state.get_circle().setX(POSITIONS[current_pos][0])
            new_state.get_circle().setY(POSITIONS[current_pos][1])
            update_label_for_state(graphic_scene, new_state)
            current_pos = chr(ord(current_pos) + 1)

        # what if more than the pre-defined positions?

    for dfa_state in dfa_states.keys():
        # creating edges
        # {'A': {'a': 'BA', 'b': 'A'}, 'BA': {'a': 'CBA', 'b': 'CA'}, 'CBA': {'a': 'DCBA', 'b': 'DCA'},
        state_alphabet_dict = dfa_states[dfa_state]
        for alphabet in state_alphabet_dict.keys():
            for child_state in State.STATES:
                if f'{state_alphabet_dict[alphabet]}' == child_state.get_name():
                    child = child_state
                    ctrl_p1, ctrl_p1_pos = new_state.get_circle().get_control_point()
                    ctrl_p2, ctrl_p2_pos = child.get_circle().get_control_point()
                    connection = Connection(ctrl_p1, ctrl_p2_pos)
                    ctrl_p1.add_line(connection)
                    connection.set_start(ctrl_p1)
                    connection.set_end(ctrl_p2)
                    ctrl_p2.add_line(connection)
                    create_edge(edge_combo, new_state, state_alphabet_dict[alphabet], connection, alphabet,
                                graphic_scene)
                    graphic_scene.addItem(connection)
                    break

    global SEMAPHORE
    SEMAPHORE = False


# ====================================== [ OLD CODE ] =====================================================
"""
def dfa_nfa_converter(graphics_scene, state_combo, edge_combo):
    global SEMAPHORE
    SEMAPHORE = True
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

    convert_nfa_to_dfa(nfa_states, nfa_final_states, graphics_scene, state_combo, edge_combo)


def convert_nfa_to_dfa(nfa, nfa_final_state, graphic_scene, state_combo, edge_combo):
    new_states_list = []
    dfa = {}
    keys_list = list(x.get_name() for x in State.STATES)
    path_list = list(Edge.ALPHABETS)

    dfa[keys_list[0]] = {}
    for y in range(len(Edge.ALPHABETS)):
        var = "".join(nfa[keys_list[0]][path_list[
            y]])
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

    print('NFA: ')
    print(nfa)
    print('NFA Final States: ')
    print(nfa_final_state, '\n')

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
    draw_dfa(dfa, dfa_final_states, graphic_scene, state_combo, edge_combo)

"""
