from django.urls import path

from .views import (
    ProjectDetailView,
    ProjectListCreateView,
    StartProjectView,
    CompleteProjectView,
    CancelProjectView,
)

urlpatterns = [
    path("projects/",ProjectListCreateView.as_view(),name="project-list-create"),
    path("projects/<int:pk>/",ProjectDetailView.as_view(),name="project-detail"),
path(
        "project/<int:pk>/start/",
        StartProjectView.as_view(),
        name="project-start",
    ),
    path(
        "project/<int:pk>/complete/",
        CompleteProjectView.as_view(),
        name="project-complete",
    ),
    path(
        "project/<int:pk>/cancel/",
        CancelProjectView.as_view(),
        name="project-cancel",
    ),
]