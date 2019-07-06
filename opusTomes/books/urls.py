from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='books_index'),
    path('create/', views.book_create, name='book_create'),
    path('<int:book_id>/', views.book_detail, name='book_detail'),
    path('edit/<int:book_id>/', views.book_edit, name='book_edit'),
    path('generate/pdf/<int:book_id>/', views.generate_pdf, name='book_generate_pdf'),
    path('<int:book_id>/dndPage/create/', views.dnd_page_create, name='dnd_page_create'),
    path('<int:page_id>/dndPage/edit/', views.dnd_page_edit, name='dnd_page_edit'),
    path('<int:page_id>/dndPage/order/up/', views.dnd_page_order_up, name='dnd_page_order_up'),
    path('<int:page_id>/dndPage/order/down/', views.dnd_page_order_down, name='dnd_page_order_down'),
    path('<int:book_id>/srdPage/select/', views.srd_page_select, name='srd_page_select'),
]