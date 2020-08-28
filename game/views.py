import json
from game.utils.db_builder import build_airports, build_flights
from game.models import CustomUser
from django.http import JsonResponse, HttpResponseNotAllowed
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import permissions, status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from .forms import InventoryForm, ItemForm, UserFlightsForm
from .models import Airport, Country, Inventory, UserFlights, Flight, Item, CustomUser
from .serializers import (
    CountrySerializer, GameStatsSerializer, MyTokenObtainPairSerializer,
    CustomUserSerializer,
    AirportSerializer,
    FlightSerializer,
    UserFlightSerializer,
    ItemSerializer,
    InventorySerializer
)


class ObtainTokenPairWithColorView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class LogoutAndBlacklistRefreshTokenForUserView(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def post(self, request):
        try:
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class CustomUserCreate(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def post(self, request, format='json'):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HelloWorldView(APIView):

    def get(self, request):
        return Response(data={"Hello": "World"}, status=status.HTTP_200_OK)


def airports_list(request):
    airports = Airport.objects.all()
    serialized_airports = AirportSerializer(airports).all_airports
    return JsonResponse(data=serialized_airports, status=status.HTTP_200_OK)


def no_back_tracking(request, IATA_code, username):
    current_airport = get_object_or_404(Airport, IATA_code=IATA_code)
    current_user = get_object_or_404(CustomUser, username=username)
    filterd_destinations = list(Flight.objects.filter(
        origin=current_airport).exclude(manifest__user=current_user))
    serialized_flights = FlightSerializer(filterd_destinations).all_flights
    return JsonResponse(data=serialized_flights, status=status.HTTP_200_OK)

@csrf_exempt
def book_a_flight(request, username):
    user = get_object_or_404(CustomUser, username=username)
    if request.method == 'POST':
        data = json.loads(request.POST)
        flight = get_object_or_404(Flight, pk=data.flight_id)
        new_flight = UserFlights
        new_flight.user = user
        new_flight.flight = flight
        new_flight.turn_count = data.turn_count
        form = UserFlightsForm(new_flight)
        if form.is_valid():
            user.currency_on_hand -= flight.price
            user.save()
            item = form.save()
            serialized_item =ItemSerializer(item).item_detail
            return JsonResponse(data=serialized_item, status=201)
        return JsonResponse(data=form.errors.as_data, status=400)
    return HttpResponseNotAllowed(['POST'])

def countries_visited(request, username):
    ctry = Country
    departing = set(ctry.objects.filter(airports__departing__manifest__user__username=username))
    arriving = set(ctry.objects.filter(airports__arriving__manifest__user__username=username))
    all_countries = departing.union(arriving)
    serialized_data = CountrySerializer(list(all_countries)).all_countries
    return JsonResponse(data=serialized_data, status=200)


def User_flight_history(request, username):
    current_user = get_object_or_404(CustomUser, username=username)
    flight_history = get_list_or_404(UserFlights, user=current_user)
    serialized_flight_history = UserFlightSerializer(flight_history).all_flights
    return JsonResponse(data=serialized_flight_history, status=status.HTTP_200_OK)


def index(self, request):
    return render(request, "index.html", context=None)


def BuildAirportDB(request):
    print("Adding seed airports to DB...")
    airports = build_airports()
    print("Airports added.")
    data = AirportSerializer(airports).all_airports
    return JsonResponse(data=data, status=status.HTTP_201_CREATED)


def BuildFlightDB(request):
    print("Adding seed flights to DB...")
    flights = build_flights()
    print("Flights added.")
    data = {'msg': "Flights added successfully"}
    return JsonResponse(data=data, status=status.HTTP_201_CREATED)


@csrf_exempt
def item_new(request):  #item_create
    if request.method == 'POST':
        data = json.loads(request.POST)
        form = ItemForm(data)
        if form.is_valid():
            item = form.save()
            serialized_item =ItemSerializer(item).item_detail
            return JsonResponse(data=serialized_item, status=201)
        return JsonResponse(data=form.errors.as_data, status=400)
    return HttpResponseNotAllowed(['POST'])

def item_list(request):  #item_read_all
    items = Item.objects.all()
    serialized_items = ItemSerializer(items).all_items
    return JsonResponse(data=serialized_items, status=200)

def item_specifics(request, item_id):  #item_read
    item = get_object_or_404(Item, pk=item_id)
    serialized_item =ItemSerializer(item).item_detail
    return JsonResponse(data=serialized_item, status=200)

@csrf_exempt
def item_edit(request, item_id):  #item_update
    item = get_object_or_404(Item, pk=item_id)
    if request.method == 'POST':
        data = json.loads(request.POST)
        form = ItemForm(data, instance=item)
        if form.is_valid():
            item = form.save()
            serialized_item = ItemSerializer(item).item_detail
            return JsonResponse(data=serialized_item, status=200)
        return JsonResponse(data=form.errors.as_data, status=400)
    return HttpResponseNotAllowed(['POST'])

@csrf_exempt
def item_delete(request, item_id):  #item_delete
    if request.method == 'POST':
        item = get_object_or_404(Item, pk=item_id)
        item.delete()
        return JsonResponse(data={'status':'success'}, status=200)
    return HttpResponseNotAllowed(['POST'])


@csrf_exempt
def inventory_new(request, username):  #inventory_create
    user = get_object_or_404(CustomUser, username=username)
    if request.method == 'POST':
        lookup = json.loads(request.POST)
        item = get_object_or_404(Item, pk=lookup.item_id)
        data = Inventory
        data.user = user
        data.item = item
        data.turn_purchased = lookup.turn_purchased
        data.turns_remaining = item.duration
        data.status = 'av'
        form = InventoryForm(data)
        if form.is_valid():
            inventory = form.save()
            serialized_inventory = InventorySerializer(inventory).inventory_detail
            return JsonResponse(data=serialized_inventory, status=201)
        return JsonResponse(data=form.errors.as_data, status=400)
    return HttpResponseNotAllowed(['POST'])

def inventory_list(request, username):  #inventory_read_all
    user = get_object_or_404(CustomUser, username=username)
    inventory = get_list_or_404(Inventory, user=user)
    serialized_inventory = InventorySerializer(inventory).all_inventories
    return JsonResponse(data=serialized_inventory, status=200)

def inventory_specifics(request, username, inventory_id):  #inventory_read
    inventory = get_object_or_404(Inventory, pk=inventory_id)
    serialized_inventory = InventorySerializer(inventory).inventory_detail
    return JsonResponse(data=serialized_inventory, status=200)

@csrf_exempt
def inventory_edit(request, username, inventory_id):  #inventory_update
    inventory = get_object_or_404(Inventory, pk=inventory_id)
    if request.method == 'POST':
        data = json.loads(request.POST)
        form = InventoryForm(data, instance=inventory)
        if form.is_valid():
            inventory = form.save()
            serialized_inventory = InventorySerializer(inventory).inventory_detail
            return JsonResponse(data=serialized_inventory, status=200)
        return JsonResponse(data=form.errors.as_data, status=400)
    return HttpResponseNotAllowed(['POST'])

@csrf_exempt
def inventory_delete(request, username, inventory_id):  #inventory_delete
    if request.method == 'POST':
        inventory = get_object_or_404(Inventory, pk=inventory_id)
        inventory.delete()
        return JsonResponse(data={'status':'success'}, status=200)
    return HttpResponseNotAllowed(['POST'])

@api_view(('GET',))
@renderer_classes((JSONRenderer, TemplateHTMLRenderer))
def retrieve_game_stats(request):
    user = get_object_or_404(CustomUser, pk=request.user.pk)
    ctry = Country
    departing = set(ctry.objects.filter(airports__departing__manifest__user=user))
    arriving = set(ctry.objects.filter(airports__arriving__manifest__user=user))
    all_countries = departing.union(arriving)
    countries_visited_count=len(all_countries)
    stats_obj = {}
    stats_obj['user'] = user
    stats_obj['countries_visited_count'] = countries_visited_count
    stats_obj['countries_visited'] = all_countries
    serialized_result = GameStatsSerializer(stats_obj, many=False).data
    return Response(serialized_result)
    


