from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ['rating', 'title', 'content', 'advantages', 'disadvantages']
        widgets = {
            'rating': forms.RadioSelect(attrs={
                'class': 'flex space-x-4'
            }),
            'title': forms.TextInput(attrs={
                'class': 'w-full p-2 border rounded',
                'placeholder': 'Заголовок відгуку'
            }),
            'content': forms.Textarea(attrs={
                'class': 'w-full p-2 border rounded',
                'placeholder': 'Напишіть ваш відгук...',
                'rows': 4
            }),
            'advantages': forms.Textarea(attrs={
                'class': 'w-full p-2 border rounded',
                'placeholder': 'Переваги (необов’язково)',
                'rows': 3
            }),
            'disadvantages': forms.Textarea(attrs={
                'class': 'w-full p-2 border rounded',
                'placeholder': 'Недоліки (необов’язково)',
                'rows': 3
            }),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title.strip()) < 5:
            raise forms.ValidationError("Заголовок має містити мінімум 5 символів.")
        return title.strip()

    def clean_content(self):
        content = self.cleaned_data['content']
        if len(content.strip()) < 20:
            raise forms.ValidationError("Текст відгуку має містити мінімум 20 символів.")
        return content.strip()

    def clean_advantages(self):
        return self.cleaned_data['advantages'].strip()

    def clean_disadvantages(self):
        return self.cleaned_data['disadvantages'].strip()