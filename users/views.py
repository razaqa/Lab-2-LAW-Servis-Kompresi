from .serializers import CreateUserSerializer
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

import requests


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    '''
    Registers user to the server. Input should be in the format:
    {"username": "username", "password": "1234abcd"}
    '''
    serializer = CreateUserSerializer(data=request.data) 
    if serializer.is_valid():
        serializer.save() 
        r = requests.post(settings.TOKEN_API, 
            data={
                'grant_type': 'password',
                'username': request.data['username'],
                'password': request.data['password'],
                'client_id': settings.CLIENT_ID,
                'client_secret': settings.CLIENT_SECRET,
            },
        )
        return Response(r.json())
    return Response(serializer.errors)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    '''
    Gets tokens with username and password. Input should be in the format:
    {"username": "username", "password": "1234abcd"}
    '''
    r = requests.post(settings.TOKEN_API, 
        data={
            'grant_type': 'password',
            'username': request.data['username'],
            'password': request.data['password'],
            'client_id': settings.CLIENT_ID,
            'client_secret': settings.CLIENT_SECRET,
        },
    )
    return Response(r.json())