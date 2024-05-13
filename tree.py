class Node(object):
    def __init__(self, alfa=float("-inf"), beta=float("inf"), parent=None, value=None):
        self.value = value
        self.alfa = alfa
        self.beta = beta
        self.parent = parent
        self.children = []
    
    def add_child(self, child):
        self.children.append(child)

    def get_children(self):
        return self.children

    def update_alpha(self, value):
        self.alfa = max(self.alfa, value)    
    
    def update_beta(self, value):
        self.beta = min(self.beta, value)
    
    def get_alpha(self):
        return self.alfa
    
    def get_beta(self):
        return self.beta
    
    def is_purned(self):
        return self.alfa >= self.beta