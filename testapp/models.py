from django.db import models

# Create your models here.

class User(models.Model):
    first_name = models.TextField()
    last_name = models.TextField()
    username = models.TextField()
    password = models.TextField()
    credit_card = models.TextField()
    admin = models.BooleanField(default=False)


# new_user = User.objects.create(
#     first_name=first_name,
#     last_name=last_name,
#     username=username,
#     password=password,
#     credit_card=credit_card
# )
# new_user.save()
