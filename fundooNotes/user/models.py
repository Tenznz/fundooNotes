from django.db import models


# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=200)
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    password = models.CharField(max_length=50)
    age = models.IntegerField()
    email = models.EmailField(max_length=40)
    phone = models.CharField(max_length=10)

    def __str__(self):
        return self.username + "," + self.firstname + "," + self.lastname + "," + self.password + "," \
               + str(self.age) + "," + self.email + "," + self.phone
