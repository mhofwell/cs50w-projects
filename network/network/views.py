import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from .models import Post, User, PostForm, UserFollowers
from django.core import serializers


def index(request):
    return render(request, "network/index.html", {
        'form': PostForm(),
        'posts': Post.objects.all(),
    })


@login_required
@csrf_exempt
def follow(request, username):
    # Query for requested User, User_to_follow and UserFollower list
    user = request.user
    print(user)
    user_to_follow = User.objects.get(username=username)
    try:
        follower_list = UserFollowers.objects.get_or_create(user=request.user)
    except UserFollowers.DoesNotExist:
        return JsonResponse({"error": "Follower list not found."}, status=404)

    # handle PUT request
    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("follow") is not None:
            count = user.following
            user.following = (count + 1)
            user.save()
            print("added +1")
            follower_list.append(user_to_follow)
            print("appended")
            follower_list.save()
        return JsonResponse({"success": "Follower list updated."}, tatus=204)

    # Follow must be via PUT
    else:
        return JsonResponse({
            "error": "PUT request required."
        }, status=400)


@ login_required
@ csrf_exempt
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


@ login_required
def get_profile(request, username):

    posts = []
    follower_obj = []
    follower_count = 0
    user = User.objects.get(id=request.user.id)
    following_this_user = False
    print(user)

    # get specific user and followers
    userprofile = User.objects.get(username=username)
    username = userprofile.username
    followers = userprofile.number_of_followers

    obj = UserFollowers.objects.get_or_create(user=userprofile.id)
    following_obj = obj.following
    follower_count = len(following_obj)
    for follower in follower_obj:
        if follower.username == username:
            following_this_user == True

    # get posts and order in reverse chronological order
    if Post.objects.filter(user=userprofile.id).exists():
        posts = Post.objects.filter(user=userprofile.id)
        posts = posts.order_by('-timestamp').all()

    return render(request, "network/profile.html", {
        'followers': follower_obj,
        'follower_count': follower_count,
        'following': following,
        'username': username,
        'posts': posts,
        'user': user,
        'userprofile': userprofile,
        'following_this_user': following_this_user
    })


def load_posts(request, group):
    # get all posts
    if group == "all":
        posts = Post.objects.all()
        print(posts)
        if posts == None:
            return JsonResponse({"error": "No posts to show!"}, status=400)

    # get followers posts only
    elif group == "following":
        followers = []
        if UserFollowers.objects.filter(user=request.user.id).exists():
            user = UserFollowers.objects.filter(
                user=request.user.id
            )

            # get all of a users followers
            followers = user.followers.all()

            # for each follower, get their posts and add it to a list
            for follower in followers:
                posts = []
                posts.append(Post.objects.get(user=follower))

    else:
        return JsonResponse({"error": "Invalid request for newsfeed posts."}, status=400)

    # Return posts in reverse chronologial order
    posts = posts.order_by("-timestamp").all()
    print(type(posts))
    # s_posts = serializers.serialize("json", posts)
    return JsonResponse([post.serialize() for post in posts], safe=False)


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
