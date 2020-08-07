from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render

from . models import Tweet

# Create your views here.
def home_view(request, *args, **kwargs):
    return HttpResponse("<h1>Hello world</h1>")
    
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
