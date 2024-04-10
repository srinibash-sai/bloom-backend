from django.urls import path
from .views import RegisterView ,LoginView, UserView, PythonView, LogoutView, PythonQuestionView, PythonSubmitView

urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('user', UserView.as_view()),
    path('python', PythonView.as_view()),
    path('logout', LogoutView.as_view()),
    path('python-question', PythonQuestionView.as_view()),
    path('python-submit', PythonSubmitView.as_view()),
]