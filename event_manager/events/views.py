from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView
from .forms import EventForm
from .models import Event
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import DeleteView
from django.urls import reverse_lazy

events = Event.objects.all().order_by('date')

def home(request):
    return render(request, 'events/home.html', {'events': events})

def event_list(request):
    events = Event.objects.all().order_by('date')
    print(f"Количество мероприятий: {events.count()}")
    return render(request, 'events/event_list.html', {'events': events})

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    comments = event.comments.all().order_by('-created_at')
    return render(request, 'events/event_detail.html', {
        'event': event,
        'comments': comments
    })

def delete_event(request, event_id):
    if request.method == 'POST':
        # Пока не реализовано удаление, просто перенаправляем на список
        return redirect('events:event_list')
    return render(request, 'events/delete_event.html', {'event_id': event_id})

def services(request):
    services_list = [
        'Организация мероприятий',
        'Аренда оборудования',
        'Кейтеринг',
        'Развлекательные программы',
    ]
    return render(request, 'events/services.html', {'services': services_list})

team_members = [
        {'name': 'Иван Иванов', 'position': 'Директор'},
        {'name': 'Петр Петров', 'position': 'Менеджер проектов'},
        {'name': 'Светлана Смирнова', 'position': 'Координатор мероприятий'},
    ]

def team(request):
    return render(request, 'events/team.html', {'team': team_members})

def about(request):
    return render(request, 'events/about.html', {'team': team_members})

def gallery(request):
    return render(request, 'events/gallery.html', {'events': events})

def contact_us(request):
    return render(request, 'events/contact_us.html')

class GalleryView(TemplateView):
    template_name = 'events/gallery.html'

#@login_required
def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save()
            messages.success(request, 'Мероприятие успешно добавлено.')
            return redirect('events:event_detail', event_id=event.id)
    else:
        form = EventForm()
    return render(request, 'events/add_event.html', {'form': form})

#@login_required
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Мероприятие успешно обновлено.')
            return redirect('events:event_detail', event_id=event.id)
    else:
        form = EventForm(instance=event)
    return render(request, 'events/edit_event.html', {'form': form, 'event': event})

class EventDeleteView(DeleteView):
    model = Event
    template_name = 'events/delete_event.html'
    success_url = reverse_lazy('events:event_list')

    def dispatch(self, request, *args, **kwargs):
        #if not request.user.is_authenticated:
        #    return redirect('login')
        return super().dispatch(request, *args, **kwargs)