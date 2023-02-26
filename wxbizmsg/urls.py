from django.urls import path
from wxbizmsg import views

urlpatterns = [
    path("wechat/", views.WechatView.as_view()),
    path("chatgpt/", views.chatgpt, name="chatgpt"),
]