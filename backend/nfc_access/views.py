import jwt
from django.conf import settings
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime
from .models import User, NFCCard, Transaction
from .serializers import UserSerializer, NFCCardSerializer, TransactionSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class NFCCardViewSet(viewsets.ModelViewSet):
    queryset = NFCCard.objects.all()
    serializer_class = NFCCardSerializer

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

@api_view(['POST'])
def nfc_login(request):
    jwt_token = request.data.get('jwt')
    if not jwt_token:
        return Response({'error': 'No JWT provided'}, status=400)

    try:
        # Imprimez le token reçu pour le débogage
        print("Received token:", jwt_token)
        
        # Imprimez la clé secrète utilisée pour le débogage
        print("Secret key:", settings.SECRET_KEY)

        # Essayez de décoder le token sans vérifier la signature pour voir son contenu
        decoded_no_verify = jwt.decode(jwt_token, options={"verify_signature": False})
        print("Decoded token without verification:", decoded_no_verify)

        # Récupérer ou créer l'utilisateur basé sur les informations du token
        user, created = User.objects.get_or_create(
            Email=decoded_no_verify['email'],
            defaults={
                'Name': decoded_no_verify['name'],
                'Role': decoded_no_verify['role'],
                'iat': datetime.fromtimestamp(decoded_no_verify['iat']),
                'exp': datetime.fromtimestamp(decoded_no_verify['exp'])
            }
        )

        # Retourner les informations de l'utilisateur
        return Response({
            'message': 'Login successful',
            'user': UserSerializer(user).data
        }, status=200)

    except jwt.ExpiredSignatureError:
        return Response({'error': 'Token has expired'}, status=401)
    except jwt.InvalidTokenError as e:
        print("Decoding error:", str(e))  # Ajoutez un log pour l'erreur de décodage
        return Response({'error': f'Invalid token: {str(e)}'}, status=401)
    except Exception as e:
        print("Unexpected error:", str(e))  # Ajoutez un log pour toute autre erreur
        return Response({'error': f'Unexpected error: {str(e)}'}, status=500)