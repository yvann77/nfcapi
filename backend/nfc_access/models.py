from django.db import models

class User(models.Model):
    UserID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=100)
    Email = models.EmailField(unique=True)
    iat = models.DateTimeField()  # issued at
    exp = models.DateTimeField()  # expiration
    Role = models.CharField(max_length=50)

    def __str__(self):
        return self.Name

class NFCCard(models.Model):
    CardID = models.AutoField(primary_key=True)
    CardNumber = models.CharField(max_length=100, unique=True)
    UserID = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.CardNumber

class Transaction(models.Model):
    TransactionID = models.AutoField(primary_key=True)
    CardID = models.ForeignKey(NFCCard, on_delete=models.CASCADE)
    Amount = models.DecimalField(max_digits=10, decimal_places=2)
    Date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Transaction {self.TransactionID} on {self.Date}'