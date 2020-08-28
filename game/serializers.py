from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import Country, CustomUser, Airport, Flight, Inventory, Item, UserFlights


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


class GameUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['pk', 'username', 'currency_on_hand', 'turns_taken']


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['pk', 'name', 'code', 'latitude', 'longitude', 'flag_url']


class AirportSerializer(serializers.ModelSerializer):
    country = CountrySerializer()

    class Meta:
        model = Airport
        fields = ['pk', 'country', 'name', 'city', 'IATA_code', 'latitude', 'longitude', 'timezone_offset']


class FlightSerializer(serializers.ModelSerializer):
    origin = AirportSerializer()
    destination = AirportSerializer()

    class Meta:
        model = Flight
        fields = ['pk', 'origin', 'destination', 'duration', 'carrier_code', 'carrier_name', 'flight_number', 'aircraft_code', 'price']


class UserFlightSerializer(serializers.ModelSerializer):
    user = GameUserSerializer()
    flight = FlightSerializer()

    class Meta:
        model = UserFlights
        fields = ['pk', 'user', 'flight', 'booked_at', 'turn_count']


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['pk', 'name', 'price', 'currency_modifier', 'duration']


class InventorySerializer(serializers.ModelSerializer):
    user = GameUserSerializer()
    item = ItemSerializer()

    class Meta:
        model = Inventory
        fields = ['pk', 'user', 'item', 'turn_purchased', 
        'turns_remaining', 'status']

class GameStatsSerializer(serializers.ModelSerializer):
    userInfo = serializers.SerializerMethodField()
    countries_visited = serializers.SerializerMethodField()
    country_count = serializers.SerializerMethodField()

    def get_userInfo(self,instance):
        return GameUserSerializer(instance.user, many=False).data

    def get_countries_visited(self,instance):
        return CountrySerializer(instance.countries_visited, many=True).data

    def get_country_count(self,instance):
        return instance.countries_visited_count


    class Meta:
        model = CustomUser
        fields = ['user_info', 'countries_visited', 'country_count']