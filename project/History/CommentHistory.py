import redis
import yaml

from project import config
from project.History import PostHistoryData


class CommentHistory:

    SUMMONS_THRESHOLD = 5   # How many times one user can summon the bot in a particular post; this is a guard against a bot loop

    def __init__(self):
        # Redis data is stored in format [post_id, blob] where blob is a yaml encoded instance of PostHistoryData
        self.redis_instance = redis.StrictRedis(host=config.redis_ip, password=config.redis_auth)

    def should_reply_to_comment(self, comment):
        return not (self.replied_to_comment(comment.submission.id, comment.id) or self.too_many_summons(comment.submission.id, comment.author.id) or self.replying_to_bot(comment))

    # Determine whether the bot has already replied to a given comment, so as to prevent an infinite loop
    def replied_to_comment(self, post_id, comment_id):
        yaml_blob = self.redis_instance.get(post_id)
        if yaml_blob is not None:
            post_history_data = yaml.load(yaml_blob)
            if comment_id in post_history_data.comments:
                return True
        return False

    # Some guards against bots (obviously should add more later)
    def replying_to_bot(self, comment):
        if "I'm a bot" in comment.body or "I am a bot" in comment.body:
            print("There is a good chance this comment was made by a bot. Skipping it.")
            return True
        if comment.author.name == "hockeystats_beepboop":
            return True
        return False

    # This is to prevent getting into a bot loop; a particular user can only summon the bot so many times in a given post
    def too_many_summons(self, post_id, user):
        yaml_blob = self.redis_instance.get(post_id)
        if yaml_blob is not None:
            post_history_data = yaml.load(yaml_blob)
            for value in post_history_data.users:
                if value.user == user and value.count > self.SUMMONS_THRESHOLD:
                    print("This user has summoned the bot too many times in this post!")
                    return True
        return False

    def add_comment(self, post_id, comment_id, user_id):
        yaml_blob = self.redis_instance.get(post_id)

        if yaml_blob is not None:
            post_history_data = yaml.load(yaml_blob)    # we have already replied to a comment on this post
        else:
            post_history_data = PostHistoryData.PostHistoryData(post_id)

        post_history_data.comments.append(comment_id)
        post_history_data.increment_user_count(user_id)

        self.redis_instance.set(post_id, yaml.dump(post_history_data))

