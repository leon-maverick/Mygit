from rest_framework import serializers
from .models import Game, Song

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'






