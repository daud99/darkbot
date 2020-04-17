from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view
from accounts.models import User


@api_view(['POST'])
def createToken(request):
    user = User.objects.filter(email=request.email, password= request.password)
    token = Token.objects.create(user=user)
    print(token.key)
    return Response({
        "Success": "token is successfully created",
        "Token": token
    })