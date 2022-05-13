from datetime import date

from django.shortcuts import redirect

from django.shortcuts import render
from django.views import View

from .models import RoomForm, Room, RoomReservation


def index(request):
    return render(request, 'base.html')


def thanks(request):
    return render(request, 'thanks.html')


class AddRoomView(View):
    def get(self, request):
        form = RoomForm()
        return render(request, 'add_room.html', {'form': form})

    def post(self, request):
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('room-list')
        return render(request, 'add_room.html', {'form': form})


class RoomListView(View):
    def get(self, request):
        room = Room.objects.all().order_by('id')
        return render(request, 'room_list.html', {'rooms': room})


class DeleteRoomView(View):
    def get(self, request, room_id):
        room = Room.objects.get(id=room_id)
        room.delete()
        return redirect('room-list')


class ModifyRoomView(View):
    def get(self, request, room_id):
        r = Room.objects.get(id=room_id)
        form = RoomForm(instance=r)
        return render(request, 'modify_room.html', {'form': form})

    def post(self, request, room_id):
        r = Room.objects.get(id=room_id)
        form = RoomForm(request.POST, instance=r)
        if form.is_valid():
            form.save()
            return redirect('room-list')
        return render(request, 'room_list.html', {'form': form})


class RoomReservationView(View):
    def get(self, request, room_id):
        room = Room.objects.get(pk=room_id)
        reservations = room.roomreservation_set.filter(date__gte=str(date.today())).order_by('date')
        ctx = {'room': room, 'reservations': reservations}
        return render(request, 'room_reservation.html', ctx)

    def post(self, request, room_id):
        room = Room.objects.get(pk=room_id)
        date_r = request.POST.get('reservation-date')
        comment = request.POST.get('comment')
        if RoomReservation.objects.filter(room_id=room_id, date=date_r):
            return render(request, 'room_reservation.html',
                          context={'room': room, 'error': 'Sala jest już zarezerwowana! Proszę wybrać inną datę'})
        if date_r < str(date.today()):
            return render(request, 'room_reservation.html', context={'room': room, "error": 'Data jest z przeszłości!'})

        RoomReservation.objects.create(room_id=room, date=date_r, comment=comment)
        return redirect('room-list')
