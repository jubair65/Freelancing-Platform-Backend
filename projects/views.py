from django.db.models import Q
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from accounts.models import User

from .models import Project
from .permissions import IsClient
from .serializers import ProjectSerializer


class ProjectListCreateView(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated(), IsClient()]

        return [IsAuthenticated()]

    def get_queryset(self):
        queryset = Project.objects.select_related(
            "client",
            "assigned_freelancer",
        ).all()

        search = self.request.query_params.get("search")
        category = self.request.query_params.get("category")

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search)
                | Q(description__icontains=search)
                | Q(required_skills__icontains=search)
            )

        if category:
            queryset = queryset.filter(
                category__iexact=category
            )

        return queryset.order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(client=self.request.user)


class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Project.objects.select_related(
            "client",
            "assigned_freelancer",
        )

    def update(self, request, *args, **kwargs):
        project = self.get_object()

        if request.user.role != User.Role.CLIENT:
            from rest_framework.exceptions import PermissionDenied

            raise PermissionDenied(
                "Only clients can edit projects."
            )

        if project.client_id != request.user.id:
            from rest_framework.exceptions import PermissionDenied

            raise PermissionDenied(
                "You can only edit your own projects."
            )

        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        project = self.get_object()

        if request.user.role != User.Role.CLIENT:
            from rest_framework.exceptions import PermissionDenied

            raise PermissionDenied(
                "Only clients can delete projects."
            )

        if project.client_id != request.user.id:
            from rest_framework.exceptions import PermissionDenied

            raise PermissionDenied(
                "You can only delete your own projects."
            )

        return super().destroy(request, *args, **kwargs)