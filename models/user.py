from database import add_user

class User:
    def __init__(self, name):
        self.name = name
        self.topics = []
        self.completed_tasks = 0

    def add_topic(self, topic):
        self.topics.append(topic)

    def complete_task(self):
        self.completed_tasks += 1

    def show_info(self):
        print('Имя:', self.name)
        print('Темы:', self.topics)
        print('Выполнено заданий:', self.completed_tasks)

    def save(self):
        add_user(self.name, self.completed_tasks)

    def add_topics(self, topics):
        for topic in topics:
            self.add_topic(topic)

    def get_progress(self):
        return self.completed_tasks





