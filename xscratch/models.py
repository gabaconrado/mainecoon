from django.db import models
from django.contrib.auth.models import User


class XSUser(User):
    """
    xScratch user model, extending from django generic user
    """

    age = models.IntegerField()
    school = models.CharField(max_length=20)

    def __str__(self):
        """
        Human readable representation for the model
        """
        return "{0} {1}".format(self.first_name, self.last_name)
