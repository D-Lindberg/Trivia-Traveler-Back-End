from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import CustomUser, Airport


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        return token


class CustomUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField()
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class GameUserSerializer():
    def __init__(self, body):
        self.body = body

    def convert(self, userObj):
        return {
            'id': userObj.id,
            'username': userObj.username,
            'currency_on_hand': userObj.currency_on_hand,
            'Turns_taken': userObj.Turns_taken
        }

    @property
    def all_users(self):
        output = {'users': []}
        for user in self.body:
            user_details = self.convert(user)
            output['users'].append(user_details)
        return output

    @property
    def user_detail(self):
        return self.convert(self.body)


class AirportSerializer():
    def __init__(self, body):
        self.body = body

    def convert(self, airport_obj):
        return {
            'country': CountrySerializer(airport_obj.country).country_detail,
            'name': airport_obj.name,
            'city': airport_obj.city,
            'IATA_code': airport_obj.IATA_code,
            'latitude': airport_obj.latitude,
            'longitude': airport_obj.longitude,
            'timezone_offset': airport_obj.timezone_offset,
        }

    @property
    def all_airports(self):
        output = {'airports': []}
        for airport in self.body:
            airport_details = self.convert(airport)
            output['airports'].append(airport_details)
        return output

    @property
    def airport_detail(self):
        return self.convert(self.body)


class CountrySerializer():
    def __init__(self, body):
        self.body = body

    def convert(self, country_obj):
        return {
            'name': country_obj.name,
            'code': country_obj.code,
            'latitude': country_obj.latitude,
            'longitude': country_obj.longitude,
            'flag_url': country_obj.flag_url,
        }

    @property
    def all_countries(self):
        output = {'countries': []}
        for country in self.body:
            country_details = self.convert(country)
            output['countries'].append(country_details)
        return output

    @property
    def country_detail(self):
        return self.convert(self.body)


class FlightSerializer():
    def __init__(self, body):
        self.body = body

    def convert(self, flight_obj):
        return {
            'id': flight_obj.id,
            'origin': AirportSerializer(flight_obj.origin).airport_detail,
            'destination': AirportSerializer(flight_obj.destination).airport_detail,
            'duration': flight_obj.duration,
            'carrier_code': flight_obj.carrier_code,
            'carrier_name': flight_obj.carrier_name,
            'flight_number': flight_obj.flight_number,
            'aircraft_code': flight_obj.aircraft_code,
            'price': flight_obj.price
        }

    @property
    def all_flights(self):
        output = {'flights': []}
        for flight in self.body:
            flight_details = self.convert(flight)
            output['flights'].append(flight_details)
        return output

    @property
    def flight_detail(self):
        return self.convert(self.body)


class UserFlightSerializer():
    def __init__(self, body):
        self.body = body

    def convert(self, user_flight_obj):
        return {
            'user': GameUserSerializer(user_flight_obj.user).user_detail,
            'flight': FlightSerializer(user_flight_obj.flight).flight_detail,
            'booked_at': user_flight_obj.booked_at,
            'turn_count': user_flight_obj.turn_count,
        }

    @property
    def all_flights(self):
        output = {'flights': []}
        for flight in self.body:
            flight_details = self.convert(flight)
            output['flights'].append(flight_details)
        return output

    @property
    def flight_detail(self):
        return self.convert(self.body)


class ItemSerializer:
    def __init__(self, body):
        self.body = body

    def convert(self, item_obj):
        return {
            'id': item_obj.id,
            'name': item_obj.name,
            'price': item_obj.price,
            'currency_modifier': item_obj.currency_modifier,
            'duration': item_obj.duration
        }

    @property
    def all_items(self):
        output = {'items': []}
        for item in self.body:
            item_details = self.convert(item)
            output['items'].append(item_details)
        return output

    @property
    def item_detail(self):
        return self.convert(self.body)


class InventorySerializer:
    def __init__(self, body):
        self.body = body

    def convert(self, inv_obj):
        return {
            'id': inv_obj.id,
            'user': CustomUserSerializer(inv_obj.user),
            'item': ItemSerializer(inv_obj.item),
            'turn_purchased': inv_obj.turn_purchased,
            'turns_remaining': inv_obj.turns_remaining,
            'status': inv_obj.status,
        }

    @property
    def all_inventories(self):
        output = {'inventories': []}
        for inventory in self.body:
            inventory_details = self.convert(inventory)
            output['inventories'].append(inventory_details)
        return output

    @property
    def item_detail(self):
        return self.convert(self.body)
