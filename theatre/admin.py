from django.contrib import admin
from theatre.models import (
    Genre,
    Actor,
    TheatreHall,
    Play,
    Performance,
    Reservation,
    Ticket
)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name")
    search_fields = ("first_name", "last_name")


@admin.register(TheatreHall)
class TheatreHallAdmin(admin.ModelAdmin):
    list_display = ("name", "rows", "seats_in_row", "capacity")


@admin.register(Play)
class PlayAdmin(admin.ModelAdmin):
    list_display = ("title", "duration")
    search_fields = ("title",)
    list_filter = ("genres",)


@admin.register(Performance)
class PerformanceAdmin(admin.ModelAdmin):
    list_display = ("play", "theatre_hall", "show_time", "price")
    list_filter = ("show_time", "theatre_hall")


class TicketInline(admin.TabularInline):
    model = Ticket
    extra = 1


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("created_at", "user")
    list_filter = ("created_at",)
    search_fields = ("user__email",)
    inlines = [TicketInline]
