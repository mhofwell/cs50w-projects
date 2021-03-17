from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from .models import Post, User, PostForm, UserFollowers


def index(request):
    return render(request, "network/index.html", {
        'form': PostForm(),
        'posts': Post.objects.all(),
    })


@login_required
@csrf_exempt
def post(request):
    user = User.objects.get(pk=request.user.id)
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    data = json.loads(request.body)
    body = data.get("body", "")
    if post_data == [""]:
        return JsonResponse({"error": "Field cannot be blank."}, status=400)
    post = Post(
        user=user,
        body=body,
    )
    post.save()
    return JsonResponse({"message": "Posted successfully."}, status=201)


def loadPosts(request, group):
    # get all posts
    if group == "all":
        posts = Post.objects.all()
        return JsonResponse([post.serialize() for post in posts], safe=False)

    # get followers posts only
    elif group == "following":
        followers = UserFollowers.objects.filter(
            user=request.user
        )

        # create empty list for follower objects
        posts_from_followers = []
        user = UserFollowers.objects.get(user=request.user.id)

        # get all of a users followers
        followers = user.followers.all()

        # for each follower, get their posts and add it to a list
        for follower in followers:
            posts = Post.objects.get(user=follower)
            posts_from_followers.append(posts)

        # Return posts in reverse chronologial order
        posts_from_followers.order_by("-timestamp").all()
        return JsonResponse([post.serialize() for post in posts_from_followers], safe=False)

    else:
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
