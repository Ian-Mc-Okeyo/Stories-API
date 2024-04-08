from django.urls import path
from .views import *

urlpatterns = [
    path('api/editors/', editor_list, name='editor-list'),
    path('api/editors/<int:pk>/', editor_detail, name='editor-detail'),
    path('api/stories/', stories_list, name='stories-list'),
    path('api/stories/<int:pk>/', stories_detail, name='stories-detail'),
    path('api/create-story/<str:username>/', CreateStory.as_view(), name='create-story'),
    path('api/stories/<str:category>/<str:subCategory>/', FilterStories.as_view(), name='filter_stories-all'),
    path('api/stories/<str:category>/', FilterStories.as_view(), name='filter_stories-cat'),
    path('api/stories/<str:subCategory>/', FilterStories.as_view(), name='filter_stories-sub'),
    path('api/subcategories/', subcategory_list, name='subcategory-list'),
    path('api/subcategories/<int:pk>/', subcategory_detail, name='subcategory-detail'),
    path('api/user/', UserView.as_view(), name='user'),
    path('api/user-editor/<str:username>/', UserEditor.as_view(), name='user-editor'),
    path('api/login/', Login.as_view(), name='login'),
    path('api/reading-list-create/', AddToReadingList.as_view(), name='add-to-reading-list'),
    path('api/reading-list-get/<int:userid>/', GetReadingList.as_view(), name='get-reading-list'),
]