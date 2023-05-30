from django.db import models

from User.models import User


class Policy(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return self.name + '_' + self.user.name


class Claim(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.TextField()
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE)

    def __str__(self):
        return self.name + '_' + self.policy.name + '_' + self.policy.user.name


class Payment(models.Model):
    id = models.IntegerField(primary_key=True)
    amount = models.IntegerField()
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE)

    def __str__(self):
        return self.policy.user.name+'_'+self.policy.name+'_'+str(self.amount)
