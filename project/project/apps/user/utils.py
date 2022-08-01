from .models import User

#unfollow function
def _unfollow(user : User, requester : User):
    user.followers.remove(requester)
    requester.following.remove(user)
    return user