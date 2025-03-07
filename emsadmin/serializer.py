from rest_framework import serializers

from account.serializer import ArtistLoginProfileFull_Serializer, UserDetail_Serializer

from .models import Artist, Event, Sponser


# Sponser
# creating serializer for the sponser.
class Sponser_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Sponser
        fields = "__all__"


# Event
# creating serializer for the event.
class Event_Serializer(serializers.ModelSerializer):
    # this done for accepting the multiple value in the model relation field form the front end user.
    artist = serializers.PrimaryKeyRelatedField(
        queryset=Artist.objects.all(), many=True
    )
    sponser = serializers.PrimaryKeyRelatedField(
        queryset=Sponser.objects.all(), many=True
    )

    class Meta:
        model = Event
        fields = "__all__"


# this is for the ticket booking.
class EventListT_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"


# creating the sponser serializer for the event list.
class SponserList_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Sponser
        fields = ("photo", "name", "sponser_type")


# creating serializer for the event list view.
class EventList_Serializer(serializers.ModelSerializer):
    artist = serializers.StringRelatedField(many=True)
    sponser = SponserList_Serializer(many=True)

    class Meta:
        model = Event
        fields = "__all__"


# creating the artist serializer for the event list.
class ArtistList_Serializer(serializers.ModelSerializer):
    user = UserDetail_Serializer()

    class Meta:
        model = Artist
        fields = ("user", "photo")
        # depth = 1


# creating serializer for the event list/detail view...
class EventList1_Serializer(serializers.ModelSerializer):
    # this done for converting the pimary key into string.
    # artist = serializers.StringRelatedField(many=True)
    artist = ArtistList_Serializer(many=True)
    # sponser = serializers.StringRelatedField(many=True)
    sponser = SponserList_Serializer(many=True)

    class Meta:
        model = Event
        fields = "__all__"


# making the serializer for the recommended events.
class RecommendedEvent_Serializer(serializers.ModelSerializer):
    # artist=Artist_Serializer_Full_Details(many=True)
    artist = serializers.StringRelatedField(many=True)
    sponser = SponserList_Serializer(many=True)

    class Meta:
        model = Event
        fields = "__all__"


# serializer for the request event.
class EventRequest_Serializer(serializers.ModelSerializer):
    artist = ArtistLoginProfileFull_Serializer(many=True)
    sponser = SponserList_Serializer(many=True)

    class Meta:
        model = Event
        fields = "__all__"
