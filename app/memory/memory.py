class Memory:

    def __init__(self):
        self.history = []

    def remember(self, event):
        self.history.append(event)

    def get_history(self):
        return self.history

    def clear(self):
        self.history.clear()