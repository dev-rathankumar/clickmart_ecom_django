from django.urls import path
from users import views as UserViews
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from products import views as ProductViews



urlpatterns = [
    path('register/', UserViews.RegisterView.as_view()),
    
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # access tokens
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # refresh tokens

    path('profile/', UserViews.ProfileView.as_view()),

    # Categories API
    path('categories/', ProductViews.CategoryListView.as_view()),

    # Product List API
    path('products/', ProductViews.ProductListView.as_view()),

    # Product Detail API
    path('products/<int:pk>/', ProductViews.ProductDetailView.as_view())
]
