from api.models import Match, Sports, Market, Selection
from rest_framework import serializers

class SportSerializer(serializers.ModelSerializer):
	class Meta:
		model =Sports
		fields = ('id', 'name')

class SelectionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Selection
		fields = ('id', 'name', 'odds')

class MarketSerializer(serializers.ModelSerializer):
	selections = SelectionSerializer(read_only= True)
	class Meta:
		model = Market
		fields = ('id', 'name', 'selections')

class MatchListSerializer(serializers.ModelSerializer):
	class Meta:
		model = Match
		fields = ('id', 'url', 'name', 'startTime')

class MatchDetailSerializer(serializers.ModelSerializer):
	sport = SportSerializer()
	market = MarketSerializer()

	class Meta:
		model = Match
		fields = ('id', 'url', 'name', 'startTime', 'sport', 'market' )