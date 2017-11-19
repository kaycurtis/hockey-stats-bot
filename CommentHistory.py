import redis
import yaml
import PostHistoryData

class CommentHistory:

    SUMMONS_THRESHOLD = 5   # How many times one user can summon the bot in a particular post; this is a guard against a bot loop

    def __init__(self):
        self.redis_instance = redis.StrictRedis(host="138.197.175.216", password="!*z9DmY4XLXo*bJSagG!RamPTbc5K#")

    def should_reply_to_comment(self, post_id, comment_id, user):
        return not (self.replied_to_comment(post_id, comment_id) or self.too_many_summons(post_id, user))

    def replied_to_comment(self, post_id, comment_id):
        json_blob = self.redis_instance.get(post_id)
        if json_blob is not None:
            post_history_data = yaml.load(json_blob)
            if comment_id in post_history_data.comments:
                return True
        return False

    def too_many_summons(self, post_id, user):
        json_blob = self.redis_instance.get(post_id)
        if json_blob is not None:
            post_history_data = yaml.load(json_blob)
            for value in post_history_data.users:
                print(value.user)
                print(value.count)
                if value.user == user and value.count > self.SUMMONS_THRESHOLD:
                    print("This user has summoned the bot too many times in this post!")
                    return True
        return False

    def add_comment(self, post_id, comment_id, user_id):
        json_blob = self.redis_instance.get(post_id)
        if json_blob is not None:
            post_history_data = yaml.load(json_blob)
            post_history_data.comments.append(comment_id)
            for index, user_count in enumerate(post_history_data.users):
                if user_count.user == user_id:
                    user_count.increment()
                    post_history_data.users[index] = user_count
                    self.redis_instance.set(post_id, yaml.dump(post_history_data))
                    return
            user_count = PostHistoryData.UserCount(user_id)
            post_history_data.users.append(user_count)
            self.redis_instance.set(post_id, yaml.dump(post_history_data))
            return
        else:
            post_history_data = PostHistoryData.PostHistoryData(post_id)
            post_history_data.comments.append(comment_id)
            user_count = PostHistoryData.UserCount(user_id)
            post_history_data.users.append(user_count)
            self.redis_instance.set(post_id, yaml.dump(post_history_data))

