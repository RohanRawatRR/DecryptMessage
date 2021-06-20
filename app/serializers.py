import re
import gnupg
from django.conf import settings
from django.core.files.storage import default_storage
from rest_framework import serializers

''' Serializer to decrypt the message '''
class DecryptMessageSerializer(serializers.Serializer):

    passphrase = serializers.CharField(required=True)
    message = serializers.CharField()


    ''' Initializing the gnupg package here '''
    def __init__(self, *args, **kwargs):
        super(DecryptMessageSerializer, self).__init__(*args, **kwargs)
        context = kwargs.get('context', None)
        self.gpg = gnupg.GPG("gpg", verbose=True)
        if context:
            self.request = kwargs['context']['request']


    '''Handling the decryption of the message here '''
    def create(self, validated_data):
        passphrase = validated_data['passphrase']
        message = validated_data['message']

        if 'Version' in message:
            message = re.sub("Version.*?\)", '', message)
        try:
            length_begin_msg = len("-----BEGIN PGP MESSAGE-----")
            length_end_msg = len("-----END PGP MESSAGE-----")
            message = message[:length_begin_msg] + '\r\n\r' + message[length_begin_msg:]
            message = message[:-length_end_msg] + '\r\n' + "-----END PGP MESSAGE-----"
        except:
            pass

        # with open('F:\\External Projects\\text.txt', 'rb') as f:
        #     status = self.gpg.decrypt_file(f, passphrase='parrot@123')
        try:
            data = self.gpg.decrypt(message, passphrase=passphrase)
        except Exception as e:
            raise serializers.ValidationError(
                {'message': e}
            )
        return data

    '''Sending the required data in JSON format '''
    def to_representation(self, instance):
        data = {}
        data['DecryptedMessage'] = instance.data
        return data
