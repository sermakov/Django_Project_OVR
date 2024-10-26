from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView
from .forms import EventForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

events = [
        {'id': 1, 'title': 'Концерт классической музыки', 'date': '12.01.2025 19:00', 'description': 'Концерт с участием известных исполнителей.', 'location': 'Концертный зал', 'organizer': 'Иван Иванов', 'category': 'Музыка', 'comments': [
            {'user': 'Пользователь1', 'comment': 'Потрясающее мероприятие!', 'created_at': '13.01.2025 10:00'},
            {'user': 'Пользователь2', 'comment': 'Очень понравилось!', 'created_at': '14.01.2025 12:00'},
        ]},
        # Добавьте другие мероприятия, если необходимо
    ]

def home(request):
    return render(request, 'events/home.html', {'events': events})

def event_list(request):
    # В будущем здесь будет вывод списка мероприятий
    return render(request, 'events/event_list.html')

def event_detail(request, event_id):
    # Статические данные, так как модели не используются
    event = next((item for item in events if item['id'] == event_id), None)
    if event:
        comments = event.get('comments', [])
        return render(request, 'events/event_detail.html', {
            'event': event,
            'comments': comments
        })
    else:
        return render(request, 'events/event_not_found.html')

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
    return render(request, 'events/gallery.html')

def contact_us(request):
    return render(request, 'events/contact_us.html')

class GalleryView(TemplateView):
    template_name = 'events/gallery.html'

@login_required
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