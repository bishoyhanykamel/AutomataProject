class State:
    STATES = []

    def __init__(self, number, circle):
        self.number = number
        self.edge = None
        self.circle = circle
        self.combobox_id = number
        self.name = f'State #{self.number}'
        State.STATES.append(self)
        pass

    def get_name(self):
        return self

    def __str__(self):
        return f'State #{self.number}'


class Edge:
    EDGES = []

    def __init__(self, number, from_parent, to_parent, line_item, input):
        self.number = number
        self.from_parent = from_parent
        self.to_parent = to_parent
        self.line_item = line_item
        self.alphabet = input
        self.combobox_id = number
        Edge.EDGES.append(self)

    def __str__(self):
        # return f'Edge status: connected from {self.from_parent} to {self.to_parent} by {self.alphabet}'
        return f'Edge #{self.number}'
