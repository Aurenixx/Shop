from django import forms
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError


TAILWIND_CLASSES = (
    "w-full px-4 py-2 border border-gray-300 rounded-lg "
    "focus:ring-2 focus:ring-blue-500 focus:border-transparent"
)


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label="Ім'я",
        widget=forms.TextInput(
            attrs={
                "class": TAILWIND_CLASSES,
                "placeholder": "Введіть ваше ім'я",
            }
        ),
        error_messages={
            "required": "Будь ласка, введіть ваше ім'я.",
            "max_length": "Ім'я не може перевищувати 100 символів.",
        },
    )

    email = forms.EmailField(
        label="Email",
        validators=[EmailValidator(message="Введіть коректну email адресу.")],
        widget=forms.EmailInput(
            attrs={
                "class": TAILWIND_CLASSES,
                "placeholder": "your.email@example.com",
            }
        ),
        error_messages={
            "required": "Будь ласка, введіть email адресу.",
            "invalid": "Введіть коректну email адресу.",
        },
    )

    subject = forms.CharField(
        max_length=200,
        label="Тема",
        widget=forms.TextInput(
            attrs={
                "class": TAILWIND_CLASSES,
                "placeholder": "Тема повідомлення",
            }
        ),
        error_messages={
            "required": "Будь ласка, введіть тему повідомлення.",
            "max_length": "Тема не може перевищувати 200 символів.",
        },
    )

    message = forms.CharField(
        label="Повідомлення",
        widget=forms.Textarea(
            attrs={
                "class": f"{TAILWIND_CLASSES} resize-none",
                "rows": 6,
                "placeholder": "Ваше повідомлення...",
            }
        ),
        error_messages={
            "required": "Будь ласка, введіть повідомлення.",
        },
    )

    def clean_name(self):
        name = self.cleaned_data.get("name", "").strip()

        if len(name) < 2:
            raise ValidationError("Ім'я повинно містити мінімум 2 символи.")

        if name.isdigit():
            raise ValidationError("Ім'я не може складатися лише з цифр.")

        return name

    def clean_message(self):
        message = self.cleaned_data.get("message", "").strip()

        if len(message) < 10:
            raise ValidationError("Повідомлення повинно містити мінімум 10 символів.")

        if message.count("http") > 3:
            raise ValidationError("Повідомлення не може містити більше 3 посилань.")

        return message

    def clean_subject(self):
        subject = self.cleaned_data.get("subject", "").strip()
        return subject