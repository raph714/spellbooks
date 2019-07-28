from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from django.contrib.auth.models import User

from .models import Book, DNDPage, SRDPage
from .forms import BookCreateForm, DNDPageCreateForm, SRDSelectForm
# from fpdf import FPDF
import os

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        books = request.user.books.all()
        return render(request, 'books/index.html', {'books': books})
    return render(request, 'books/index.html')

def book_create(request):
    if request.method == 'POST' and request.user.is_authenticated:
        form = BookCreateForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.owner = request.user
            book.save()
            return redirect('books_index')
    else:
        form = BookCreateForm()
    return render(request, 'books/create.html', {'form': form})

def book_edit(request, book_id):
    # get the related book
    try:
        book = Book.objects.get(pk=book_id)
    except Book.DoesNotExist:
        raise Http404("Book does not exist")

    # make sure we own the book
    if book.owner != request.user:
        raise Http404("Book does not exist")

    if request.method == 'POST' and request.user.is_authenticated:
        form = BookCreateForm(request.POST, instance=book)
        if form.is_valid():
            book = form.save(commit=False)
            book.owner = request.user
            book.save()
            return redirect('books_index')
    else:
        form = BookCreateForm(instance=book)
    return render(request, 'books/create.html', {'form': form})

def book_detail(request, book_id):
    try:
        book = Book.objects.get(pk=book_id)
        pages = DNDPage.objects.filter(book_id=book_id).order_by('order')
    except Book.DoesNotExist:
        raise Http404("Book does not exist")
    return render(request, 'books/detail.html', {'book': book, 'pages': pages})

def dnd_page_create(request, book_id):
    # get the related book
    try:
        book = Book.objects.get(pk=book_id)
    except Book.DoesNotExist:
        raise Http404("Book does not exist")

    # make sure we own the book
    if book.owner != request.user:
        raise Http404("Book does not exist")

    if request.method == 'POST' and request.user.is_authenticated:
        form = DNDPageCreateForm(request.POST)
        if form.is_valid():
            page = form.save(commit=False)
            page.book = book
            page.order = book.pages.count() + 1
            page.save()
            return HttpResponseRedirect(reverse('book_detail', args=[book_id]))
    else:
        form = DNDPageCreateForm()
    return render(request, 'pages/dnd_page_create.html', {'form': form, 'book': book})

def dnd_page_edit(request, page_id):
    # get the related book
    try:
        page = DNDPage.objects.get(pk=page_id)
    except DNDPage.DoesNotExist:
        raise Http404("DNDPage does not exist")

    # make sure we own the book
    if page.book.owner != request.user:
        raise Http404("DNDPage does not exist")

    if request.method == 'POST' and request.user.is_authenticated:
        form = DNDPageCreateForm(request.POST, instance=page)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('book_detail', args=[page.book.id]))
    else:
        form = DNDPageCreateForm(instance=page)
    return render(request, 'pages/dnd_page_create.html', {'form': form, 'book': page.book})

def dnd_page_order_up(request, page_id):
    # get the related book
    try:
        page = DNDPage.objects.get(pk=page_id)
    except DNDPage.DoesNotExist:
        raise Http404("DNDPage does not exist")

    # make sure we own the book
    if page.book.owner != request.user:
        raise Http404("DNDPage does not exist")

    allPages = list(DNDPage.objects.filter(book_id=page.book.pk).order_by('order'))

    # get the current index of the page we want to move up
    current_index = allPages.index(page)

    if current_index == 0:
        #short circuit if it's already at the top.
        return HttpResponseRedirect(reverse('book_detail', args=[page.book.id]))

    #roll over the pages and set the index
    for index, aPage in enumerate(allPages):
        print(index)
        print(aPage.title)
        if index == current_index -1:
            # this is the one above the page, we want to move it down one
            aPage.order = index + 1
        elif index == current_index:
            #this is the page we want to move up
            aPage.order = index - 1
        else:
            aPage.order = index
        aPage.save()

    return HttpResponseRedirect(reverse('book_detail', args=[page.book.id]))

def dnd_page_order_down(request, page_id):
    # get the related book
    try:
        page = DNDPage.objects.get(pk=page_id)
    except DNDPage.DoesNotExist:
        raise Http404("DNDPage does not exist")

    # make sure we own the book
    if page.book.owner != request.user:
        raise Http404("DNDPage does not exist")

    allPages = list(DNDPage.objects.filter(book_id=page.book.pk).order_by('order'))

    # get the current index of the page we want to move up
    current_index = allPages.index(page)

    if current_index == len(allPages) - 1:
        #short circuit if it's already at the bottom.
        return HttpResponseRedirect(reverse('book_detail', args=[page.book.id]))

    #roll over the pages and set the index
    for index, aPage in enumerate(allPages):
        if index == current_index +1:
            # this is the one below the page, we want to move it up one
            aPage.order = index - 1
        elif index == current_index:
            #this is the page we want to move up
            aPage.order = index + 1
        else:
            aPage.order = index
        aPage.save()

    return HttpResponseRedirect(reverse('book_detail', args=[page.book.id]))

def srd_page_select(request, book_id):
    # get the related book
    try:
        book = Book.objects.get(pk=book_id)
    except Book.DoesNotExist:
        raise Http404("Book does not exist")

    # make sure we own the book
    if book.owner != request.user:
        raise Http404("Book does not exist")

    if request.method == 'POST' and request.user.is_authenticated:
        form = SRDSelectForm(request.POST)
        if form.is_valid():
            for spell_pk in request.POST.getlist('srd_spells'):
                try:
                    page = SRDPage.objects.get(pk=spell_pk)
                    page.save_as_dnd(book)
                except SRDPage.DoesNotExist:
                    raise Http404("SRD Page does not exist")
            return HttpResponseRedirect(reverse('book_detail', args=[book_id]))
    else:
        form = SRDSelectForm()
    return render(request, 'pages/srd_page_select.html', {'form': form, 'book': book})

def generate_pdf(request, book_id):
    # get the related book
    try:
        book = Book.objects.get(pk=book_id)
    except Book.DoesNotExist:
        raise Http404("Book does not exist")

    # make sure we own the book
    if book.owner != request.user:
        raise Http404("Book does not exist")

    # BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # fallingSkyPath = os.path.join(BASE_DIR, 'fonts/theano/TheanoDidot-Regular.ttf')

    # pdf = FPDF(orientation = 'P', unit = 'mm', format='Letter')
    # pdf.add_font('theano', '', fallingSkyPath, uni=True)

    # for page in book.pages.all().order_by('order'):
    #     page.add_page_to_pdf(pdf)

    # pdf.output('tuto1.pdf', 'F')

    return HttpResponseRedirect(reverse('book_detail', args=[book_id]))
