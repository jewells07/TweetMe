import random
from django.conf import settings
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url

from .forms import TweetForm
from .models import Tweet

# Create your views here.
ALLOWED_HOSTS = settings.ALLOWED_HOSTS

def home_view(request, *args, **kwargs):
    # return HttpResponse("<h1>Hello world</h1>")
    return render(request, 'pages/home.html', context={}, status=200)

def tweet_create_view(request, *args, **kwargs):
    form = TweetForm(request.POST or None)
    next_url = request.POST.get("next") or None
    if form.is_valid():
        obj = form.save(commit=False)
        # Do other form related logic
        obj.save()
        if request.is_ajax():
            return JsonResponse({}, status=201) # 201 == Created a Items

        if next_url != None and is_safe_url(next_url, ALLOWED_HOSTS):
            return redirect(next_url)
        form = TweetForm()
    return render(request, 'components/form.html', context={"form" : form})

def tweet_list_view(request, *args, **kwargs):
    """
    REST API VIEW
    Consume by Javascript or Swift or Java/iOS/Android etc..
    return json data
    """

    qs = Tweet.objects.all()
    tweets_list = [ {"id":x.id, "content":x.content, "likes": random.randint(0, 122) } for x in qs]
    data = {
        "isUser" : False,
        "response": tweets_list
    }
    return JsonResponse(data)
    
def tweets_detail_view(request, tweet_id, *args, **kwargs):
    """
    REST API VIEW
    Consume by Javascript or Swift or Java/iOS/Android etc..
    return json data
    """
    data ={
        "id": tweet_id
    }
    status=200
    try:
        obj = Tweet.objects.get(id=tweet_id)
        data['content'] = obj.content
    except:
        data['message']= "Not found"
        status = 404
        
    

    return JsonResponse(data, status=status) # json.dumps content_type='application/json'
