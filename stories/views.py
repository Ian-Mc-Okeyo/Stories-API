from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Editor
from .serializers import *
from rest_framework.views import APIView
from knox.models import AuthToken
from django.contrib.auth import authenticate
#from drf_yasg.utils import swagger_auto_schema

class UserView(APIView):
    def post(self, request, *args, **kwargs):
        print('we are here')
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(request.data['password'])
            user.save()
            return Response({
                'user': serializer.data,
                'token': AuthToken.objects.create(user)[1]
            }, status=201)
        return Response(serializer.errors, status=400)

class UserEditor(APIView):
    def post(self, request, username, *args, **kwargs):
        print(request.data)
        user = User.objects.filter(username=username).first()
        if user:
            serializer = EditorSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)
        return Response({'Msg': 'User not found'}, status=404)
    
class Login(APIView):
    def post(self, request, *args, **kwargs):
        print(request.data)
        user = authenticate(username= request.data['username'], password=request.data['password'])
        if user:
            return Response({
                'user': UserSerializer(user).data,
                'token': AuthToken.objects.create(user)[1]
            }, status=201)
        return Response({'Msg': 'Invalid credentials'}, status=400)

#@swagger_auto_schema(method='POST', request_body=EditorSerializer) 
@api_view(['GET', 'POST'])
def editor_list(request):
    if request.method == 'GET':
        editors = Editor.objects.all()
        serializer = EditorSerializer(editors, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = EditorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#@swagger_auto_schema(method='PUT', request_body=EditorSerializer) 
@api_view(['GET', 'PUT', 'DELETE'])
def editor_detail(request, pk):
    try:
        editor = Editor.objects.get(pk=pk)
    except Editor.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = EditorSerializer(editor)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = EditorSerializer(editor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        editor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#@swagger_auto_schema(method='POST', request_body=SubcategorySerializer) 
@api_view(['GET', 'POST'])
def subcategory_list(request):
    if request.method == 'GET':
        subcategories = Subcategory.objects.all()
        serializer = SubcategorySerializer(subcategories, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SubcategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#@swagger_auto_schema(method='PUT', request_body=SubcategorySerializer) 
@api_view(['GET', 'PUT', 'DELETE'])
def subcategory_detail(request, pk):
    try:
        subcategory = Subcategory.objects.get(pk=pk)
    except Subcategory.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SubcategorySerializer(subcategory)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SubcategorySerializer(subcategory, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        subcategory.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#@swagger_auto_schema(method='POST', request_body=StoriesSerializer) 
@api_view(['GET', 'POST'])
def stories_list(request):
    if request.method == 'GET':
        stories = Stories.objects.all()
        serializer = StoriesSerializer(stories, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = StoriesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CreateStory(APIView):
    def post(self, request, username, *args, **kwargs):
        editor = Editor.objects.filter(user__username = username).first()
        if not editor:
            return Response({'Msg': 'Editor not found'}, status=404)
        serializer = StoryCreateSerializer(data = request.data)
        if serializer.is_valid():
            story = serializer.save()
            story.editor = editor
            story.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

#@swagger_auto_schema(method='PUT', request_body=StoriesSerializer) 
@api_view(['GET', 'PUT', 'DELETE'])
def stories_detail(request, pk):
    try:
        story = Stories.objects.get(pk=pk)
    except Stories.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = StoriesSerializer(story)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = StoriesSerializer(story, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        story.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class FilterStories(APIView):
    def get(self, request, category='', subCategory=''):
        if category and subCategory:
            stories = Stories.objects.filter(category=category, subcategory__name=subCategory).all()
        elif category:
            stories = Stories.objects.filter(category=category).all()
        elif subCategory:
            stories = Stories.objects.filter(subcategory__name=subCategory).all()
        else:
            Stories.objects.all()
        serializer = StoriesSerializer(stories, many=True)
        return Response(serializer.data)

class AddToReadingList(APIView):
    def post(self, request, *args, **kwargs):
        serializer  = ReadingListCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class GetReadingList(APIView):
    def get(self, request, userid, *args, **kwargs):
        print('jdsfn')
        readingList = ReadingList.objects.filter(user__id=userid).all()
        print(readingList)
        serializer = ReadingListGetSerializer(readingList, many=True)
        return Response(serializer.data, status=200)


