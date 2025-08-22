from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import UserProfileView, LoginUserView, LogoutUserView, CreateUserView, EditProfileView



urlpatterns = [
    # path('profile-@<username>/', UserProfileView.as_view(), name='profile'),

    path('profile-@<username>/', UserProfileView.as_view(), name='profile'),

    path('signup/', CreateUserView.as_view(), name='signup'),
    path('edit-profile-@<username>', EditProfileView.as_view(), name='edit-profile'),

    path('signin/', LoginUserView.as_view(), name='signin'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
