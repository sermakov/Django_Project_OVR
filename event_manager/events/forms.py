from django import forms
from .models import Event
from .models import Review

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'location', 'category']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class ReviewForm(forms.ModelForm):
    honeypot = forms.CharField(required=False, widget=forms.HiddenInput, label="Leave empty")

    class Meta:
        model = Review
        fields = ['name', 'email', 'rating', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(i, i) for i in range(1, 6)]),
        }

    def __init__(self, *args, **kwargs):
        self.event = kwargs.pop('event', None)
        super().__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Review.objects.filter(event=self.event, email=email).exists():
            raise forms.ValidationError('Вы уже оставляли отзыв для этого мероприятия.')
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        honeypot = cleaned_data.get('honeypot')
        if honeypot:
            raise forms.ValidationError('Пожалуйста, оставьте это поле пустым.')
        return cleaned_data