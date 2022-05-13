class State:
    STATES = []
    STATE_NAME = 'A'

    def __init__(self, number, name=None):
        self.number = number
        self.edges = list()
        self.circle = None
        self.combobox_id = number
        self.final = False
        self.label_item = False
        if name:
            self.name = name
        else:
            self.name = self.STATE_NAME
        State.STATE_NAME = chr(ord(self.STATE_NAME) + 1)
        State.STATES.append(self)
        pass

    def get_name(self):
        return self.name

    def get_number(self):
        return self.number

    def get_edges(self):
        return self.edges

    def get_label_item(self):
        return self.label_item

    def get_circle(self):
        return self.circle

    def add_edge(self, edge):
        self.edges.append(edge)

    def connect_circle(self, circle):
        self.circle = circle

    def set_final(self, val):
        self.final = val

    def set_label_item(self, label):
        self.label_item = label

    def is_final(self):
        return self.final

    def delete_state(self):
        self.number = None
        self.edges = None
        self.circle = None
        self.combobox_id = None
        self.name = None
        self.final = False
        self.label_item = None
        State.STATES.remove(self)
        pass

    def __str__(self):
        return f'State {self.name}'


class Edge:
    EDGES = []
    ALPHABETS = []

    def __init__(self, number, from_parent, to_parent, line_item, inp):
        self.number = number
        self.from_parent = from_parent
        self.to_parent = to_parent
        self.line_item = line_item
        self.alphabet = inp
        self.combobox_id = number
        self.label_item = None
        self.add_to_alphabets(inp)
        Edge.EDGES.append(self)

    def delete_edge(self):
        self.number = None
        self.from_parent = None
        self.to_parent = None
        self.line_item = None
        self.alphabet = None
        self.combobox_id = None
        self.label_item = None
        Edge.EDGES.remove(self)
        pass

    def get_number(self):
        return self.number

    def get_name(self):
        return f'{self}'

    def get_parent_name(self):
        return self.from_parent.get_name()

    def get_child_name(self):
        return self.to_parent.get_name()

    def get_alphabet(self):
        return self.alphabet

    def get_line_item(self):
        return self.line_item

    def get_label_item(self):
        return self.label_item

    def set_label_item(self, label):
        self.label_item = label

    def add_to_alphabets(self, alphabet):
        if alphabet not in self.ALPHABETS:
            self.ALPHABETS.append(alphabet)
        """
        try:
            self.ALPHABETS = self.ALPHABETS.sort()
        except:
            print("Sorting alphabets failure")
        """

    def get_alphabets(self):
        return self.ALPHABETS

    def __str__(self):
        # return f'Edge status: connected from {self.from_parent} to {self.to_parent} by {self.alphabet}'
        return f'Edge #{self.number}'
