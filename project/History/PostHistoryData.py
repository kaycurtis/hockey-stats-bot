class PostHistoryData:
    def __init__(self, post):
        self.post = post
        self.comments = []
        self.users = []

    def increment_user_count(self, user_id):
        for index, user_count in enumerate(self.users):
            if user_count.user == user_id:
                user_count.increment()
                self.users[index] = user_count
                return
        self.users.append(UserCount(user_id))

class UserCount:
    def __init__(self, user_id):
        self.user = user_id
        self.count = 1

    def increment(self):
        self.count += 1
