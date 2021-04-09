import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core import paginator
from django.db.models.query_utils import Q
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from .models import Post, Follow, PostForm, User, Likes
from django.core import serializers
from django.core.paginator import Paginator


def index(request):

    return render(request, "network/index.html", {
        'form': PostForm(),
    })


@login_required
@csrf_exempt
def liked_posts(request):
    user = request.user
    print(user)
    post_numbers = []
    if Likes.objects.filter(user=user).exists():
        try:
            like_obj = Likes.objects.get(user=user)
            liked_posts = like_obj.liked_posts.all()
            for post in liked_posts:
                print(post.id)
                post_numbers.append(post.id)
            print(post_numbers)
            return JsonResponse(post_numbers, safe=False)
        except:
            return JsonResponse({"error": "Something went wrong!"}, status=400)


@login_required
@csrf_exempt
def like(request, postid):
    if request.method == "PUT":
        user = User.objects.get(id=request.user.id)
        print(user)
        data = json.loads(request.body)
        post = Post.objects.get(id=postid)
        # Why is this giving me trouble?
        obj, create = Likes.objects.get_or_create(user=user)

        like_boolean = data.get("like", "")

        if (like_boolean == "true"):
            post.likes += 1
            obj.liked_posts.add(post)
        else:
            post.likes -= 1
            obj.liked_posts.remove(post)
            if (post.likes < 0):
                post.likes = 0
        post.save()
        obj.save()
        return JsonResponse({"success": "Likes adjusted successfully"}, status=200)
    else:
        return JsonResponse({"error": "Not a put request"}, status=400)


@login_required
@csrf_exempt
def like_count(request, postid):
    if request.method == "GET":
        try:
            post = Post.objects.get(id=postid)
            likes = post.likes
            return JsonResponse(likes, safe=False, status=200)
        except:
            return JsonResponse({"error": "Can't access post"}, status=400)


@login_required
@csrf_exempt
def follow(request, username):
    if request.method == "PUT":
        data = json.loads(request.body)
        follow = data.get("follow", "")

        # get current user
        user = User.objects.get(id=request.user.id)
        profile = User.objects.get(username=username)
        if follow == True:
            try:
                obj, create = Follow.objects.get_or_create(user=user)
                obj.following.add(profile)
                obj.save()

                obj, create = Follow.objects.get_or_create(user=profile)
                obj.followers.add(user)
                obj.save()
                return JsonResponse({"success": "user followed successfully"}, status=200)
            except:
                return JsonResponse({"error": "user followed unsuccessfully"}, status=400)
        else:
            try:
                obj = Follow.objects.get(user=user)
                obj.following.remove(profile)
                obj.save()

                obj = Follow.objects.get(user=profile)
                obj.followers.remove(user)
                obj.save()
                return JsonResponse({"success": "user unfollowed successfully"}, status=200)
            except:
                return JsonResponse({"error": "user unfollowed unsuccessfully"}, status=400)


@login_required
def count(request, username):
    if request.method == "GET":
        try:
            # get the username of the profile to update
            user = User.objects.get(username=username)
            print(user)
            obj = Follow.objects.get(user=user)
            print(obj)

            # get the current follower count length
            count = obj.followers.count()
            print(count)

            # return that length
            return JsonResponse(count, safe=False, status=200)
        except:
            return JsonResponse({"error": "Can't access profile or follower list"}, status=400)


@login_required
@csrf_exempt
def post(request):
    user = User.objects.get(pk=request.user.id)
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    data = json.loads(request.body)
    body = data.get("body", "")
    if body == "":
        return JsonResponse({"error": "Field cannot be blank."}, status=400)
    post = Post(
        user=user,
        body=body,
        posted_by=user,
    )
    post.save()
    return JsonResponse({"message": "Posted successfully."}, status=201)


@login_required
@csrf_exempt
def get_profile(request, username):

    following_this_user = False

    # get the current user
    req_user = User.objects.get(id=request.user.id)

    # get the like array

    if Likes.objects.filter(user=req_user).exists():
        like_array = Likes.objects.get(user=req_user)
        liked_posts = like_array.liked_posts

    # get the username of the profile you are looking at
    user_profile = User.objects.get(username=username)
    user_profile_name = user_profile.username

    # get the number_of_followers and following
    if Follow.objects.filter(user=user_profile).exists():
        user_follow_object = Follow.objects.get(user=user_profile.id)

        number_of_followers = user_follow_object.followers.count()
        number_of_following = user_follow_object.following.count()

        # check to see if request_user is already following this profile
        list_of_followers = user_follow_object.followers.all()
        for follower in list_of_followers:
            if follower == req_user:
                following_this_user = True
    else:
        number_of_followers = 0
        number_of_following = 0

    # get all posts for user_profile
    if Post.objects.filter(user=user_profile).exists():
        profile_posts = Post.objects.filter(user=user_profile)
        profile_posts = profile_posts.order_by('-timestamp').all()
    else:
        profile_posts = []

    # check to see if user == username
    if req_user == user_profile:
        same_user = True
    else:
        same_user = False

    return render(request, "network/profile.html", {
        "same_user": same_user,
        "req_user": req_user,
        "user_profile": user_profile,
        "posts": profile_posts,
        "number_of_followers": number_of_followers,
        "number_of_following": number_of_following,
        "following_this_user": following_this_user,
        "user_profile_name": user_profile_name,
        "like_array": liked_posts

    })


def load_posts(request, group):
    posts = Post.objects.none()
    try:
        # get all posts
        if group == "all":
            posts = Post.objects.all()

        # get posts from people you're following only
        elif group == "following":
            user = User.objects.get(id=request.user.id)
            if Follow.objects.filter(user=user).exists():
                obj = Follow.objects.get(user=user)
                following = obj.following.all()

                # for each follower, get their posts and add it to a list

                for person in following:
                    posts = posts | Post.objects.filter(user=person)
        else:
            user = User.objects.get(username=group)
            posts = Post.objects.filter(user=user)

        # Return posts in reverse chronologial order
        posts = posts.order_by("-timestamp").all()

        return JsonResponse([post.serialize() for post in posts], safe=False)
    except:
        return JsonResponse({"error": "Invalid request for newsfeed posts."}, status=400)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
