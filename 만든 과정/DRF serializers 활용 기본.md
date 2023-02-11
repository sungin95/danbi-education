REST_FRAMEWORK를 이용해 views만들기

1. 우선 모델을 만들어 준다. 

2. serializers를 만든다. 
   ```python
   from rest_framework import serializers
   from .models import Quiz
   
   class QuizSerializer(serializers.ModelSerializer):
       class Meta:
           model = Quiz
           fields = ('title','body','answer')
   ```

3. views.py
   ```python
   from rest_framework.response import Response
   from rest_framework.decorators import api_view
   from .models import Quiz
   from .serializers import QuizSerializer
   import random
   
   
   @api_view(["GET"])
   def helloAPI(request):
       return Response("hello world!")
   
   
   @api_view(["GET"])
   def randomQuiz(reuest, id):
       totalQuizs = Quiz.objects.all()
       randomQuizs = random.sample(list(totalQuizs), id)
       serializer = QuizSerializer(randomQuizs, many=True)
       return Response(serializer.data)
   
   
   ```

 4. urls
    ```python
    from django.urls import path, include
    from .views import helloAPI, randomQuiz
    
    urlpatterns = [
        path("hello/", helloAPI),
        path("<int:id>/", randomQuiz),
    ]
    ```

    

    





