class PostHistoryData:
    def __init__(self, post):
        self.post = post
        self.comments = []
        self.users = []

class UserCount:
    def __init__(self, user_id):
        self.user = user_id
        self.count = 1

    def increment(self):
        self.count += 1
