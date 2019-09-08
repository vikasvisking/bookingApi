from django.shortcuts import render
from .models import Match,Selection, Sports, Market
from .serailizers import MatchDetailSerializer, MatchListSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

 # Create your views here.

class MatchViewSet(viewsets.ModelViewSet):
	"""
	Retrieve:
	Return The Given Match.

	List:
	Return a list of existing Matches.

	Create:
	Create a new match instance.
	"""
	queryset = Match.objects.all()
	serializer_class = MatchListSerializer  #for list view
	Detail_serializer_class = MatchDetailSerializer #for detail view
	filter_backends = (DjangoFilterBackend, OrderingFilter,)
	ordering_field = '__all__'

	def get_serializer_class(self):
		'''
		determine which serializer to use: 'list' or 'details'
		'''

		if self.action =='retrieve':
			if hasattr(self, 'Detail_serializer_class'):
				return self.Detail_serializer_class
		return super().get_serializer_class()


	def get_queryset(self):
		'''optionally restricts the returned queires by filtering against a "sport" and "name" query parameter in the url'''

		queryset = Match.objects.all()
		sport = self.request.query_params.get('sport', None)
		name = self.request.query_params.get('name', None)
		if sport is not None:
			sport = sport.title
			queryset = queryset.filter(sport__name = sport)

		if name is not None:
			queryset = queryset.filter(name = name)

		return queryset

	def create(self, request):
		'''
		TO parse the incoming request and create the new match or update existing match odds. 
		'''

		message = request.data.pop('message_type')

		#check if incoming api request is for new event creation

		if message == 'NewEvent':
			event = request.data.pop('event')
			sport = event.pop('sport')
			market = event.pop('markets')[0] #for now we need only one market place
			selection = markets.pop('selections')
			sportObj = Sport.objects.create(**sport)
			marketObj = Market.objects.create(**event, sport = sportObj)
			for selection in selections:
				market.selections.create(**selection)
			match = Match.objects.create(**event , sport = sportObj, market = marketObj)
			return Response(status = status.HTTP_201_CREATED)

		#check if incoming api request is for updation of odds

		elif message == 'UpdateOdds':
			event = request.data.pop('event')
			market = event.pop('market')[0]
			selection = event.pop('selection')
			for select in selection:
				sel = Selection.objects.get(id = select['id'])
				sel.odds = select['odds']
				sel.save()
			match = Match.objects.get(id = event['id'])
			return Response(status = status.HTTP_201_CREATED)

		else:
			return Response(status = status.HTTP_400_BAD_REQUEST)


