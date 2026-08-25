from django.urls import path

from .views import (
    ClientDashboardView,
    FreelancerDashboardView,
)

urlpatterns = [
    path("client/dashboard/",ClientDashboardView.as_view(),name="client-dashboard"),
    path("freelancer/dashboard/",FreelancerDashboardView.as_view(),name="freelancer-dashboard"),
]