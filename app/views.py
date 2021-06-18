import gnupg
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import generics
from app.serializers import DecryptMessageSerializer 
# Create your views here.

class DecryptMessage(generics.CreateAPIView):

    serializer_class = DecryptMessageSerializer

    # def post(self, request, *args, **kwargs):
    #     passphrase = request.data['passphrase']
    #     message = request.data['message']
    #     self.gpg = gnupg.GPG("gpg", verbose=True)
    #     decrypted_data = self.gpg.decrypt(message, passphrase=passphrase)
    #     import json
    #     data = {'DecryptedMessage': (decrypted_data.data).decode()}
    #     return JsonResponse(data)        
