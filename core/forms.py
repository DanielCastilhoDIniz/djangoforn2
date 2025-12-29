from django import forms
from django.core.mail.message import EmailMessage

from .models import Product


class ContactForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100)
    email = forms.EmailField(label='Email')
    subject = forms.CharField(label='Subject', max_length=120)
    message = forms.CharField(label='Message', widget=forms.Textarea)

    def send_email(self):
        """Envia um email com os dados do formulário de contato."""
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        subject = self.cleaned_data['subject']
        message = self.cleaned_data['message']

        email_message = EmailMessage(
            subject=f'Contato: {subject}',
            body=f'Nome: {name}\nEmail: {email}\n\nMensagem:\n{message}',
            from_email=email,
            to=['contato@seudominio.com'],
            headers={'Reply-To': email}
        )

        email_message.send()


class ProductModelForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['name', 'price', 'stock', 'image', 'description']
