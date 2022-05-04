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


    def getName(self):
        return self

    def __str__(self):
        return f'State #{self.number}'



class Edge:
    EDGES = []
    def __init__(self, number, fromParent, toParent, lineItem, inp):
        self.number = number
        self.from_parent = fromParent
        self.to_parent = toParent
        self.line_item = lineItem
        self.alphabet = inp
        self.combobox_id = number
        Edge.EDGES.append(self)

    def __str__(self):
        #return f'Edge status: connected from {self.from_parent} to {self.to_parent} by {self.alphabet}'
        return f'Edge #{self.number}'
