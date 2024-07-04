from rest_framework import serializers
from .models import User, NFCCard, Transaction

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['UserID', 'Name', 'Email', 'iat', 'exp', 'Role']

class NFCCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = NFCCard
        fields = ['CardID', 'CardNumber', 'UserID']

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['TransactionID', 'CardID', 'Amount', 'Date']