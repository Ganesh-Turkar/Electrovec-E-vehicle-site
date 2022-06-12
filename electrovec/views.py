from multiprocessing import context
from django.contrib.auth.models import *
from urllib import response
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse,  redirect, get_object_or_404, HttpResponseRedirect
import requests


from .models import *
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password, check_password
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm
from newsapi import NewsApiClient
from django.core.paginator import Paginator
from datetime import date, datetime, timedelta
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash

# from rest_framework import status
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from .serializers import tempserializer


def register_page(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)

                return redirect('login')

        context = {'form': form}
        return render(request, 'register.html', context)


def login_page(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('index')

            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'login.html', context)


@login_required(login_url='login')
def profile(request):
    current_user = request.user
    all_details_obj = UserDetails.objects.filter(user=current_user)
    print(all_details_obj)
    if len(all_details_obj) <= 0:
        new_user = UserDetails(user=request.user)
        new_user.save()

    userdetail = UserDetails.objects.get(user=current_user)
    print(userdetail)
    # current_user = (current_user, )
    # print(userdetail.name)

    # print(current_user, all_details_obj)

    # try:
    #     new_user = request.user.userdetails
    # except UserDetails.DoesNotExist:
    #     new_user = UserDetails(user=request.user)
    # if current_user not in all_details_obj[0]:
    #     new_user = UserDetails(user=request.user)
    #     new_user.save()

    # print(new_user)
    # if request.user.is_authenticated:
    #     return redirect('index')
    # else:
    #     form = CreateUserForm()
    #     if request.method == 'POST':
    #         form = CreateUserForm(request.POST)
    #         if form.is_valid():
    #             form.save()
    #             user = form.cleaned_data.get('username')
    #             messages.success(request, 'Account was created for ' + user)

    #             return redirect('login')

    context = {'user': current_user, "userdetail": userdetail}
    return render(request, 'profile.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def index(request):
    cats = Category.objects.all()
    all_bikes = Vehicle.objects.filter(category=cats[0])
    all_cars = Vehicle.objects.filter(category=cats[2])
    all_scooters = Vehicle.objects.filter(category=cats[1])
    return render(request, 'index.html', {"all_bikes": all_bikes, "all_cars": all_cars, "all_scooters": all_scooters})


# def generateOTP():
#     digits = "0123456789"
#     OTP = ""
#     for i in range(4):
#         OTP += digits[math.floor(random.random() * 10)]
#     return OTP


# def send_otp(request):
#     email = request.POST["email"]
#     # print(email)
#     o = generateOTP()
#     htmlgen = '<p><p>Welcome to Electrovec.. </p>&nbsp;<p> Your OTP is <strong>' + \
#         o+'</strong></p></p>'
#     send_mail('OTP request', o, 'electrovec.org@gmail.com', [
#               email], fail_silently=False, html_message=htmlgen)
#     return HttpResponse(o)


@login_required(login_url='login')
def aboutus(request):
    return render(request, 'aboutus.html')


@login_required(login_url='login')
def bikes(request):
   # cats = Category.objects.get(cat_id=id)
    cats = Category.objects.all()
    all_bikes = Vehicle.objects.filter(category=cats[0])
    return render(request, 'bikes.html', {"all_bikes": all_bikes})


@login_required(login_url='login')
def cars(request):
    # cats = Category.objects.get(cat_id=id)
    cats = Category.objects.all()
    all_cars = Vehicle.objects.filter(category=cats[2])
    # all_cars = Vehicle.objects.get(category=cats)
    all_cars = reversed(all_cars)
    return render(request, 'cars.html', {"all_cars": all_cars})


@login_required(login_url='login')
def scooters(request):
   # cats = Category.objects.get(cat_id=id)
    cats = Category.objects.all()
    all_scooters = Vehicle.objects.filter(category=cats[1])
    # all_scooters = Vehicle.objects.get(category=cats)
    return render(request, 'scooters.html', {"all_scooters": all_scooters})


@login_required(login_url='login')
def contact(request):
    return render(request, 'contact.html')


newsapi = NewsApiClient(api_key='8e902071d14e44879496eff33acc62e8')
# newsapikey = '8e902071d14e44879496eff33acc62e8'
# url = 'https://newsapi.org/v2/everything?'


@login_required(login_url='login')
def news(request):
    # response = requests.get(url, params=parameters)
    response_json = newsapi.get_everything(q='e-vehicles',
                                           from_param=datetime.today() - timedelta(days=20),
                                           to=datetime.today(),
                                           language='en',
                                           sort_by='publishedAt')

   # response_json = response.json()
    # print(response_json)
    for i in response_json['articles']:
        i['content'].replace("<ul><li>", "")
        i['content'].replace("</ll><li>", "")
    paginator = Paginator(response_json['articles'], 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'news.html', {"page_obj": page_obj, 'total_pages': range(1, page_obj.paginator.num_pages+1)})


@login_required(login_url='login')
def show_details(request, vehicle_id):
    current_user = request.user
    current_vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    cart_item, created = Cart.objects.get_or_create(
        user=current_user, vehicle=current_vehicle)
    vehicle_obj = Vehicle.objects.filter(id=vehicle_id)
    comments = V_Comment.objects.filter(vehicle=vehicle_id, parent=None)
    replies = V_Comment.objects.filter(
        vehicle=vehicle_id).exclude(parent=None)
    total_count = len(comments)+len(replies)
    # replydict = {}
    # for reply in replies:
    #     if reply.sno not in replydict.keys():
    #         replydict[reply.sno] = [reply]

    #     else:
    #         replydict[reply.sno].append(reply)
    return render(request, "details.html", {'vehicle': vehicle_obj[0], 'cart_item': cart_item, "comments": comments, "replies": replies, "total_count": total_count})


@login_required(login_url='login')
def postComments(request):
    if request.method == "POST":
        comment = request.POST.get("comment")
        user = request.user
        vehicle_id = request.POST.get("vehicle_id")
        vehicle = Vehicle.objects.get(id=vehicle_id)
        # comment = V_Comment(comment=comment, user=user, vehicle=vehicle)
        parentsno = request.POST.get("parentSno")
        replied_to = request.POST.get("replied_to")
        # print(V_Comment.objects.get(replied_to=parerentsno))
        if parentsno == "" or parentsno is None:
            comment = V_Comment(comment=comment, user=user, vehicle=vehicle)
            messages.success(
                request, "Your Comment has been posted successfully")
        else:
            parent = V_Comment.objects.get(sno=parentsno)
            comment = V_Comment(comment=comment, user=user,
                                vehicle=vehicle, parent=parent, replied_to=replied_to)
            messages.success(
                request, "Your Reply has been posted successfully")
        comment.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def update_details(request, attr2change):
    user = request.user
    detail_user = UserDetails.objects.get(user=user)
    if request.method == "POST":
        # for password change request
        if attr2change == "changepsw":
            user = request.user
            new_psw = request.POST.get("psw")
            print(f" new{new_psw}")
            user.set_password(new_psw)
            user.save()
            update_session_auth_hash(request, request.user)
            print("pswchange caal")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        # for profile pic change request
        elif attr2change == "changepic":
            print("change pic")
            if len(request.FILES) != 0:
                detail_user.profile_pic = request.FILES["img"]
                detail_user.save()
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
            elif len(request.FILES) == 0:
                messages.error(
                    request, "Please enter image")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        # for details change request
        elif attr2change == "changedetails":
            isData = False
            name = request.POST.get("name").strip()
            uname = request.POST.get("uname").strip()
            phone = request.POST.get("phone").strip()
            email = request.POST.get("email").strip()
            old_name = detail_user.name
            old_uname = user.username
            old_phone = detail_user.phone
            old_email = user.email
            # user = User.objects.get(id=request.user.id)
            # print(name, uname, phone, email)

            if name != old_name:
                if name != "" and len(name) >= 5:
                    isData = True
                    detail_user.name = name
                    detail_user.save()
                else:
                    messages.error(
                        request, "Enter valid name")
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

            if uname != old_uname:
                if uname != "" and len(uname) >= 5:
                    isData = True
                    user.username = uname
                    user.save()
                else:
                    messages.error(
                        request, "Enter valid username")
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

            if phone != old_phone:
                if phone != "" and len(phone) >= 10:
                    isData = True
                    detail_user.phone = phone
                    detail_user.save()
                else:
                    messages.error(
                        request, "Enter valid phone number")
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

            if email != old_email:
                if email != "" and len(email) >= 10:
                    isData = True
                    user.email = email
                    user.save()
                else:
                    messages.error(
                        request, "Enter valid email")
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

            if isData == True:
                messages.success(
                    request, "Your Changes are saved successfully")

            else:
                messages.error(
                    request, "You have not given any changes")

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    # elif attr == "psw":
    #     user.set_password(value)
    #     user.save()

    # print(V_Comment.objects.get(replied_to=parerentsno))
    # if parentsno == "" or parentsno is None:
    #     comment = V_Comment(comment=comment, user=user, vehicle=vehicle)
    #     messages.success(
    #         request, "Your Comment has been posted successfully")
    # else:
    #     parent = V_Comment.objects.get(sno=parentsno)
    #     comment = V_Comment(comment=comment, user=user,
    #                         vehicle=vehicle, parent=parent, replied_to=replied_to)
    #     print("reply")
    #     messages.success(
    #         request, "Your Reply has been posted successfully")
    # UserDetails.save()


# @login_required(login_url='login')
# def addfav(request, vehicle_id, action):

#     current_user = request.user
#     current_vehicle = get_object_or_404(Vehicle, id=vehicle_id)
#     cart_item, created = Cart.objects.get_or_create(
#         user=current_user, vehicle=current_vehicle)
#     if action == "add":
#         if cart_item.quantity < 1:
#             # here i hve created this for cart but i am using it as a wishlist
#             cart_item.quantity = (cart_item.quantity + 1)
#             cart_item.save()
#             print("add")
#     else:
#         if cart_item.quantity >= 0:
#             cart_item.quantity = 0
#             cart_item.delete()
#             print("del")
#     # cart_item.save()
#     #print("clicked", current_vehicle)

#     return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
# checking for ajax
@login_required(login_url='login')
def like(request):
    if request.method == 'GET':
        current_user = request.user
        vehicle_id = request.GET['vehicle_id']
        current_vehicle = get_object_or_404(Vehicle, id=vehicle_id)
        cart_item, created = Cart.objects.get_or_create(
            user=current_user, vehicle=current_vehicle)
        if cart_item.quantity < 1:
            # here i hve created this for cart but i am using it as a wishlist
            cart_item.quantity = (cart_item.quantity + 1)
            print("1", cart_item.quantity)
            cart_item.save()
            return HttpResponse('add')
        else:
            cart_item.quantity = 0
            print("<0", cart_item.quantity)
            cart_item.delete()
            return HttpResponse("unsuccesful")


@login_required(login_url='login')
def wishlist(request):
    current_user = request.user
    cart_item = Cart.objects.filter(
        user=current_user)
    cartlen = len(cart_item)
    print(cartlen)
    for j in cart_item:
        if j.quantity < 1:
            # here i hve created this for cart but i am using it as a wishlist
            j.delete()
    # items = list(cart_items.objects.all())
    # print(cart_item)
    # print(cart_item[0])
    #     current_vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    #     # code for add or minus the cart item
    #     # current_user = request.user
    #     # cart_item, created = Cart.objects.get_or_create(
    #     #     user=current_user, vehicle=current_vehicle)

    #     # if action == "del":
    #     #     if cart_item.quantity >= 1:
    #     #         cart_item.quantity = (cart_item.quantity - 1)
    #     #     else:
    #     #         cart_item.quantity = 0
    #     # else:
    #     #     cart_item.quantity = (cart_item.quantity + 1)
    #     # cart_item.save()

    # return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    return render(request, "wishlist.html", {'cart_item': cart_item, "cartlen": cartlen})


@login_required(login_url='login')
def contact(request):
    return render(request, 'contact.html')

# testing rest framework

# @api_view(['GET'])
# def templist(request):
#     tempobjs = tempclass.objects.all()
#     serializer = tempserializer(tempobjs, many=True)
#     return Response(serializer.data)


# @api_view(['GET'])
# def tempdetail(request, pk):
#     tempobj = tempclass.objects.get(id=pk)
#     serializer = tempserializer(tempobj, many=False)
#     return Response(serializer.data)


# @api_view(['POST'])
# def tempadd(request):
#     serializer = tempserializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#     return Response(serializer.data)


# @api_view(['POST'])
# def tempupdate(request, pk):
#     tempobj = tempclass.objects.get(id=pk)
#     serializer = tempserializer(instance=tempobj, data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#     return Response(serializer.data)


# @api_view(['DELETE'])
# def tempdelete(request, pk):
#     tempobj = tempclass.objects.get(id=pk)
#     tempobj.delete()
#     return Response("Deleted successfully")
