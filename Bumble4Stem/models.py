from django.db import models

# Create your models here.
class Users(models.Model):
    id = models.BigAutoField(primary_key=True)
    avatar_index = models.IntegerField(default=0)
    email =  models.CharField(max_length=255, unique=True, default="")
    display_name = models.CharField(max_length=255)
    major = models.CharField(max_length=255, default="Computer Science")
    batch = models.CharField(max_length=255)
    pronouns = models.CharField(max_length=255)
    research_interests = models.TextField()
    bio = models.TextField()


class Matches(models.Model):
    m1id = models.ForeignKey(Users, related_name="matches_current_user", on_delete=models.CASCADE, default=1)
    m2id = models.ForeignKey(Users, related_name="matched_user", on_delete=models.CASCADE, default=1)

class Rejected(models.Model):
    r1id = models.ForeignKey(Users, related_name="rejected_current_user", on_delete=models.CASCADE, default=1)
    r2id = models.ForeignKey(Users, related_name="rejected_user", on_delete=models.CASCADE, default=1)
    