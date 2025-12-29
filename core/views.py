from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect

from .forms import ContactForm, ProductModelForm
from .models import Product


def index(request):
    """View para a página inicial."""

    context = {
        'products': Product.objects.all()
    }
    return render(request, 'index.html', context)


def contact(request):
    """View para o formulário de contato."""
    form = ContactForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.send_email()
            """Processa os dados do formulário."""
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            messages.success(request, 'Mensagem enviada com sucesso!')
            form = ContactForm()  # Limpa o formulário após o envio bem-sucedido
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')

    context = {
        'form': form
    }
    return render(request, 'contact.html', context)


def product(request):
    """View para a página de produto."""
    if str(request.user) != 'AnonymousUser':
        if str(request.method) == 'POST':
            form = ProductModelForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, 'Produto salvo com sucesso!')
                form = ProductModelForm()
            else:
                messages.error(request, 'Por favor, corrija os erros abaixo.')
        else:
            form = ProductModelForm()
        context = {
            'form': form
        }
        return render(request, 'product.html', context)
    else:
        return redirect('index')
