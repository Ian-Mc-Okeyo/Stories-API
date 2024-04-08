from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'email']

class EditorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Editor
        fields = '__all__'

class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ['id', 'name']


class StoriesSerializer(serializers.ModelSerializer):
    editor = EditorSerializer()  # Use EditorSerializer for nested representation
    subcategory = SubcategorySerializer()  # Use SubcategorySerializer for nested representation

    class Meta:
        model = Stories
        fields = ['id', 'title', 'content', 'category', 'editor', 'image', 'subcategory', 'excerpt']

    def create(self, validated_data):
        editor_data = validated_data.pop('editor')
        subcategory_data = validated_data.pop('subcategory')

        editor = Editor.objects.create(**editor_data)  # Create Editor instance
        subcategory = Subcategory.objects.create(**subcategory_data)  # Create Subcategory instance

        story = Stories.objects.create(editor=editor, subcategory=subcategory, **validated_data)
        return story

    def update(self, instance, validated_data):
        editor_data = validated_data.pop('editor')
        subcategory_data = validated_data.pop('subcategory')

        editor = instance.editor
        editor.name = editor_data.get('name', editor.name)
        editor.bio = editor_data.get('bio', editor.bio)
        editor.save()

        subcategory = instance.subcategory
        subcategory.name = subcategory_data.get('name', subcategory.name)
        subcategory.save()

        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.category = validated_data.get('category', instance.category)
        instance.editor = editor
        instance.subcategory = subcategory

        instance.save()
        return instance

class StoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stories
        fields = ['title', 'content', 'image', 'category', 'subcategory', 'excerpt']

class ReadingListCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model= ReadingList
        fields = ['user', 'story']

class ReadingListGetSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    story = StoriesSerializer()
    class Meta:
        model= ReadingList
        fields = ['user', 'story']