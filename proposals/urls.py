from django.urls import path

from .views import (
    CreateProposalView,
    MyProposalsView,
    ProjectProposalsView,
    WithdrawProposalView,
    RejectProposalView,
    AcceptProposalView,
)

urlpatterns = [
    path("projects/<int:project_id>/proposal/",CreateProposalView.as_view(),name="create-proposal"),
    path("my-proposals/",MyProposalsView.as_view(),name="my-proposals"),
    path("projects/<int:project_id>/proposals/",ProjectProposalsView.as_view(),name="project-proposals"),
    path("proposal/<int:pk>/",WithdrawProposalView.as_view(),name="withdraw-proposal"),
    path("proposal/<int:pk>/accept/",AcceptProposalView.as_view(),name="accept-proposal"),
    path("proposal/<int:pk>/reject/",RejectProposalView.as_view(),name="reject-proposal"),
]