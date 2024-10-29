from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView
from .forms import EventForm
from .models import Event
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from .forms import ReviewForm
from django.core.exceptions import ValidationError
from django.contrib.auth import login
from .forms import SignUpForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.utils.decorators import method_decorator
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import EventSerializer
from rest_framework import generics
from rest_framework import viewsets
from .models import Review
from .serializers import ReviewSerializer, ReviewCreateSerializer

events = Event.objects.all().order_by('date')

def is_admin(user):
    return user.is_authenticated and user.is_staff

def home(request):
    return render(request, 'events/home.html', {'events': events})

def event_list(request):
    events = Event.objects.all().order_by('date')
    print(f"Количество мероприятий: {events.count()}")
    return render(request, 'events/event_list.html', {'events': events})

@login_required(login_url='events:login')
def post_review(request, event):
    review_form = ReviewForm(request.POST, event=event)
    try:
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.event = event
            review.user = request.user  # Если вы хотите связать отзыв с пользователем
            review.save()
            messages.success(request, 'Ваш отзыв успешно добавлен.')
            return redirect('events:event_detail', event_id=event.id)
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    except ValidationError as e:
        review_form.add_error(None, e)
    return review_form  # Возвращаем форму с ошибками

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    reviews = event.reviews.all().order_by('-created_at')
    if request.method == 'POST':
        # Если пользователь не аутентифицирован, перенаправляем на страницу входа
        if not request.user.is_authenticated:
            return redirect('events:login')
        # Обрабатываем отзыв
        review_form = post_review(request, event)
    else:
        review_form = ReviewForm(event=event)
    return render(request, 'events/event_detail.html', {
        'event': event,
        'reviews': reviews,
        'review_form': review_form,
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

@user_passes_test(is_admin)
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

@user_passes_test(is_admin)
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

class EventDeleteView(UserPassesTestMixin, DeleteView):
    model = Event
    template_name = 'events/delete_event.html'
    success_url = reverse_lazy('events:event_list')
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff
    def handle_no_permission(self):
        return redirect('events:login')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('events:home')  # Замените на вашу главную страницу
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки ниже.')
    else:
        form = SignUpForm()
    return render(request, 'events/signup.html', {'form': form})

@api_view(['GET', 'POST'])
def api_event_list(request):
    if request.method == 'GET':
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def api_event_detail(request, pk):
    try:
        event = Event.objects.get(pk=pk)
    except Event.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = EventSerializer(event)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = EventSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class EventListAPIView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class EventDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class EventViewSet(viewsets.ModelViewSet):
       queryset = Event.objects.all()
       serializer_class = EventSerializer

class ReviewViewSet(viewsets.ModelViewSet):
       queryset = Review.objects.all()
       serializer_class = ReviewSerializer

       def get_serializer_class(self):
           if self.action in ['create', 'update', 'partial_update']:
               return ReviewCreateSerializer
           return ReviewSerializer