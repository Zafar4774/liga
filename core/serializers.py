from rest_framework import serializers
from .models import Tour, Club, TournamentTable, Game


class ClubForTourListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = '__all__'


class GameListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        exclude = ('tour', )


class TourListSerializer(serializers.ModelSerializer):
    home = ClubForTourListSerializer(read_only=True)
    guest = ClubForTourListSerializer(read_only=True)
    details = serializers.SerializerMethodField()

    class Meta:
        model = Tour
        fields = '__all__'

    def get_details(self, detail):
        if Game.objects.filter(tour=detail.id).exists():
            game = Game.objects.get(tour=detail.id)
            return {
                'home_point': game.home_point,
                'guest_point': game.guest_point,
                'link': game.link,
                'home_red_card': game.home_red_card,
                'guest_red_card': game.guest_red_card,
                'home_yellow_card': game.home_yellow_card,
                'guest_yellow_card': game.guest_yellow_card,
            }
        return {}


class TournamentTableSerializer(serializers.ModelSerializer):
    club = ClubForTourListSerializer(read_only=True)

    class Meta:
        model = TournamentTable
        fields = "__all__"
