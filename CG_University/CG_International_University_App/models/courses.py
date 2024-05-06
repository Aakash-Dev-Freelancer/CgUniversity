from django.db import models

class Courses(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    courses = models.TextField()

