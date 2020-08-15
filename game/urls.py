from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from .views import (
    LogoutAndBlacklistRefreshTokenForUserView,
    ObtainTokenPairWithColorView, countries_visited, 
    inventory_specifics,
    User_flight_history,
    CustomUserCreate,
    inventory_delete,
    no_back_tracking,
    inventory_edit,
    BuildAirportDB,
    HelloWorldView,
    inventory_list,
    item_specifics,
    airports_list,
    book_a_flight,
    BuildFlightDB,
    inventory_new,
    item_delete,
    item_edit,
    item_list,
    item_new,

)
urlpatterns = [
    path('api/admin/seedAirports/',
         BuildAirportDB),

    path('api/admin/seedFlights/',
         BuildFlightDB),

    path('api/blacklist/',
         LogoutAndBlacklistRefreshTokenForUserView.as_view()),

    path('api/hello/',
         HelloWorldView.as_view()),

    path('api/token/obtain/',
         ObtainTokenPairWithColorView.as_view()),

    path('api/token/refresh/',
         jwt_views.TokenRefreshView.as_view()),

    path('api/user/create/',
         CustomUserCreate.as_view()),

    path('airports/',
         airports_list),

    path('flights/<int:IATA_code>/DestinationsNotVisited/<str:username>',
         no_back_tracking),

    path('flightHistory/<str:username>/',
         User_flight_history),

    path('items', include([
        path('', item_list),
        path('new/', item_new),
        path('<int:item_id/', include([
            path('', item_specifics),
            path('edit/', item_edit),
            path('delete/', item_delete)
        ]))
    ])),

    path('<str:username>/inventory', include([
        path('', inventory_list),
        path('new/', inventory_new),
        path('<int:inventory_id>/', include([
            path('', inventory_specifics),
            path('edit/', inventory_edit),
            path('delete/', inventory_delete)
        ]))

    ])),

    path('boookFlight/<str:username>/', book_a_flight),
    path('countriesVisited/<str:username>/', countries_visited)

]

'''

/counrties list all countries
/countries/new create a new country
/countries/countrycode create read update delete a specific country possibly countries/new for create
/countries/countrycode/airports list all airports that are in a specific country

/airports               list all airports
/airports/iatacode      create read update delete a specific airport possibly airports/new for create
/airports/iatacode/arrivals list all flights with current airport as destination
/airports/iatacode/departures list all flights with current airport as origin
/airports/iatacode/destinations list all airports with flights originating from a specific airport
/airports/iatacode/origins list all airports with flights that have a specific airport as a destination
/airports/iatacode/newflight create a new flight with a specific airport as origin
/airports/iatacode/flights list all flights to and from a specific airport
/flights
'''
