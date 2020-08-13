from django.urls import path

from wall import views

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('walls/list/', views.WallsList.as_view(), name='walls_list'),
    path('walls/details/<int:pk>/', views.WallDetails.as_view(), name='wall_details'),
    path('comment/list/', views.CommentsList.as_view(), name='comments_list'),
    path('comment/details/<int:pk>/', views.CommentDetails.as_view(), name='comment_details'),
]
