"""
URL configuration for chainvote project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views


urlpatterns = [
    path('set-account/', views.SetAccountByPrivateKey.as_view(), name="set-account"),
    path('create/', views.CreateIdentity.as_view(), name="create-identity"),
    path('get/', views.getIdentity.as_view(), name="get-identity"),
    path('credential/request/', views.RegisterForCredential.as_view(), name="request-credential"),
    path('credential/all/', views.AllCredentialRequest.as_view(), name="all-credential-request"),
    path('credential/issue/', views.IssueCredential.as_view(), name="issue-credential")



]
