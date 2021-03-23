from .views import FileCompressionAPIView
from django.urls import include, path

urlpatterns = [
    path("compress", FileCompressionAPIView.as_view()),
]