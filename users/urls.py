from django.urls import include, path
from rest_framework_simplejwt import views as jwt_views

from users import views

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/verify/', jwt_views.token_verify, name='token_verify'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/users/change-password/', views.ChangePasswordView.as_view(), name="change_pass"),
    path('api/users/list/', views.UsersList.as_view(), name='users_list'),
    path('api/users/details/<int:pk>/', views.UserDetails.as_view(), name='user_details'),
]
