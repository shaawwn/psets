from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """User information, including Username, email, and password
    included as part of AbstractUser
    """
    # pass


class Post(models.Model):
    """Create a user post including information about who made the post,
    and how many likes it has
    Should be very similar to Mail Email() class
    """
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts")
    body = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True) # This and liked should be added automatically
    liked = models.BooleanField(default=False) # Liked should also have some information regarding who liked it, default is false, can be changed with PUT

    def serialize(self):
        """Convert post to JSON object"""
        return{
            "id": self.id,
            "user": self.user.username,
            "body": self.body,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "liked": self.liked
        }

class Following(models.Model):
    """A user may add another user to their Following list. Followed users will
    have their posts displayed in a different section than the 'All Posts' section
    included as the 'Following' link on the navbar"""

    # Aside from allowing a user to 'Follow' other users, users that are Followed
    # should have the number of Followers be visible on their profile page.
        # ManyToMany and relational_name, 'follower', 'followed'
    pass


'''
Related names, this is how attributs are referenced later, with the flights example, "departures" was referencing what airports flights where originating from
and "arrivals" was what airport flights were going to.

'''
# class Email(models.Model):
#     user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="emails")
#     sender = models.ForeignKey("User", on_delete=models.PROTECT, related_name="emails_sent")
#     recipients = models.ManyToManyField("User", related_name="emails_received")
#     subject = models.CharField(max_length=255)
#     body = models.TextField(blank=True)
#     timestamp = models.DateTimeField(auto_now_add=True)
#     read = models.BooleanField(default=False)
#     archived = models.BooleanField(default=False)

#     def serialize(self):
#         return {
#             "id": self.id,
#             "sender": self.sender.email,
#             "recipients": [user.email for user in self.recipients.all()],
#             "subject": self.subject,
#             "body": self.body,
#             "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
#             "read": self.read,
#             "archived": self.archived
#         }