from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView

def home(request):
    return render(request, 'events/home.html')

def event_list(request):
    # В будущем здесь будет вывод списка мероприятий
    return render(request, 'events/event_list.html')

def event_detail(request, event_id):
    # В будущем здесь будет вывод деталей мероприятия
    return render(request, 'events/event_detail.html', {'event_id': event_id})

def delete_event(request, event_id):
    if request.method == 'POST':
        # Пока не реализовано удаление, просто перенаправляем на список
        return redirect('events:event_list')
    return render(request, 'events/delete_event.html', {'event_id': event_id})

def services(request):
    return render(request, 'events/services.html')

def team(request):
    return render(request, 'events/team.html')

def contact_us(request):
    return render(request, 'events/contact_us.html')

class GalleryView(TemplateView):
    template_name = 'events/gallery.html'