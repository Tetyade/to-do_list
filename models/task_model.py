class Task:
    def __init__(self, title, is_done=False):
        self.title = title
        self.is_done = is_done

    # def toggle(self):
    #     self.is_done = not self.is_done

    # def to_dict(self):
    #     return {"title": self.title, "is_done": self.is_done}

    # @staticmethod
    # def from_dict(data):
    #     return Task(data["title"], data["is_done"])
