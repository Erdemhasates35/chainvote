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

from django.urls import path, include
from .views import get_candidate_count, get_candidate_info, get_voter_status, vote, get_votes_for_candidate, add_candidate

urlpatterns = [
    path('api/candidate-count/', get_candidate_count, name='get_candidate_count'),
    path('api/candidate-info/<int:candidate_id>/', get_candidate_info, name='get_candidate_info'),
    path('api/voter-status/<str:address>/', get_voter_status, name='get_voter_status'),
    path('api/vote/', vote, name='vote'),
    path('api/votes-for-candidate/<int:candidate_id>/', get_votes_for_candidate, name='get_votes_for_candidate'),
    path('api/add-candidate/', add_candidate, name='add_candidate'),
]
