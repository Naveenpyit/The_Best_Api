from . import views
from django.urls import path

urlpatterns=[
    path('fetchph-buss/<str:table_name>/',views.get_ph_business,name='ph_business'),
    #post
    path('postph-buss/',views.post_ph_business,name='post-ph_business'),
]