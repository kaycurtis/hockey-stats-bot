class CommentHistory:

    comments_replied_to = None
    history_per_post = None

    def __init__(self):
        global comments_replied_to
        with open("comments_replied.txt", "r") as file:
            comments_replied_to = file.read()
            comments_replied_to = comments_replied_to.split("\n")
            file.close()

    def contains_id(self,id):
        return id in comments_replied_to

    def add_id(self,id):
        comments_replied_to.append(id)
        with open("comments_replied.txt", "a+") as file:
            file.write(id + "\n")
            file.close()
