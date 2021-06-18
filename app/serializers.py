import pdb
import gnupg
from rest_framework import serializers


class DecryptMessageSerializer(serializers.Serializer):

    passphrase = serializers.CharField(required=True)
    message = serializers.CharField(required=True)


    def __init__(self, *args, **kwargs):
        super(DecryptMessageSerializer, self).__init__(*args, **kwargs)
        context = kwargs.get('context', None)
        self.gpg = gnupg.GPG("gpg", verbose=True)
        if context:
            self.request = kwargs['context']['request']

    def create(self, validated_data):
        passphrase = validated_data['passphrase']
        message = validated_data['message']
        try:
            data = self.gpg.decrypt(message, passphrase=passphrase)
        except Exception as e:
            raise serializers.ValidationError(
                {'message': e}
            )
        return data

    def to_representation(self, instance):
        data = {}
        data['DecryptedMessage'] = instance.data
        return data
