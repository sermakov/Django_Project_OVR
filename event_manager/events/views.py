from django.shortcuts import render

def home(request):
    return render(request, 'events/home.html')

def event_list(request):
    # В будущем здесь будет вывод списка мероприятий
    return render(request, 'events/event_list.html')

def event_detail(request, event_id):
    # В будущем здесь будет вывод деталей мероприятия
    return render(request, 'events/event_detail.html', {'event_id': event_id})