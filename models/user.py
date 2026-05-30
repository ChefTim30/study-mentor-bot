class User:
    def __init__(self, name):
        self.name = name
        self.topics = []
        self.completed_tasks = 0

    def add_topic(self, topic):
        self.topics.append(topic)

    def complete_task(self):
        self.completed_tasks += 1



