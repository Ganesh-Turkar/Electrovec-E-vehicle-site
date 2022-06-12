from django.urls import path
from electrovec import views
urlpatterns = [

    path('', views.index, name="index"),
    path("bikes", views.bikes, name='bikes'),
    path('contact', views.contact, name='contact'),
    path('cars', views.cars, name='cars'),
    path('news', views.news, name='news'),
    path('aboutus', views.aboutus, name='aboutus'),
    path('scooters', views.scooters, name='scooters'),
    path('register', views.register_page, name='register'),
    path('login', views.login_page, name='login'),
    path('logout', views.logoutUser, name='logout'),
    path('profile', views.profile, name='profile'),
    path('wishlist', views.wishlist, name='wishlist'),
    path('show_details/<int:vehicle_id>',
         views.show_details, name='show_details'),
    #     path('show_scooter_details/<int:scooter_id>',
    #          views.show_scooter_details, name='show_scooter_details'),
    #     path('show_bike_details/<int:bike_id>',
    #          views.show_bike_details, name='show_bike_details'),
    #path("send_otp", views.send_otp, name="send otp")
    # path('addfav/<int:vehicle_id>/<str:action>', views.addfav, name='addfav'),
    path('like/', views.like, name='like'),  # checking ajax
    path('postComments', views.postComments, name='postComments'),
    path('update_details/<str:attr2change>',
         views.update_details, name='update_details'),
    # temp for rest framework
    #     path('tlist', views.templist, name='templist'),
    #     path('tdetail/<int:pk>', views.tempdetail, name='tempdetail'),
    #     path('tadd', views.tempadd, name='tempadd'),
    #     path('tupdate/<int:pk>', views.tempupdate, name='tempupdate'),
    #     path('tdelete/<int:pk>', views.tempdelete, name='tempdelete'),
]
