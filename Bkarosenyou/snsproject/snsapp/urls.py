from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.TopPageView.as_view(),name='index'),
    
    path('coment/', views.ComentView.as_view(),name='coment'),
    path('reply/<int:pk>', views.ReplyView.as_view(),name='reply'),
    
    path('profile/<int:ids>',views.profileView,name='profile'),
    path('profilesetting/<int:pk>',views.ProfileSettingView.as_view(),name='profile-setting'),
    
    path('search/',views.SearchView.as_view(),name='search'),
    path('test/',views.Test.as_view(),name='test'),
    path('setting/',views.SettingView.as_view(),name='setting'),
    path('delete/<int:pk>',views.deletecomment,name='delete'),
    path('detail/<int:pk>',views.DetailView.as_view(),name='detail'),
    path('evaluation/<int:pk>',views.evaluationview, name='evaluation'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)