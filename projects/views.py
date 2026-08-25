from django.db.models import Q
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


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



class StartProjectView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        project = get_object_or_404(
            Project,
            id=kwargs["pk"],
        )

        if request.user.role != User.Role.CLIENT:
            raise PermissionDenied(
                "Only clients can start projects."
            )

        if project.client_id != request.user.id:
            raise PermissionDenied(
                "You can only manage your own projects."
            )

        if project.status != Project.Status.OPEN:
            raise ValidationError(
                "Only open projects can be started."
            )

        if project.assigned_freelancer_id is None:
            raise ValidationError(
                "A freelancer must be assigned before starting the project."
            )

        project.status = Project.Status.IN_PROGRESS
        project.save(update_fields=["status"])

        return Response(
            {
                "message": "Project started successfully.",
                "project_id": project.id,
                "status": project.status,
            },
            status=status.HTTP_200_OK,
        )


class CompleteProjectView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        project = get_object_or_404(
            Project,
            id=kwargs["pk"],
        )

        if project.status != Project.Status.IN_PROGRESS:
            raise ValidationError(
                "Only in-progress projects can be completed."
            )

        is_client = (
            request.user.role == User.Role.CLIENT
            and project.client_id == request.user.id
        )

        is_assigned_freelancer = (
            request.user.role == User.Role.FREELANCER
            and project.assigned_freelancer_id == request.user.id
        )

        if not (is_client or is_assigned_freelancer):
            raise PermissionDenied(
                "You are not allowed to complete this project."
            )

        project.status = Project.Status.COMPLETED
        project.save(update_fields=["status"])

        return Response(
            {
                "message": "Project completed successfully.",
                "project_id": project.id,
                "status": project.status,
            },
            status=status.HTTP_200_OK,
        )


class CancelProjectView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        project = get_object_or_404(
            Project,
            id=kwargs["pk"],
        )

        if request.user.role != User.Role.CLIENT:
            raise PermissionDenied(
                "Only clients can cancel projects."
            )

        if project.client_id != request.user.id:
            raise PermissionDenied(
                "You can only cancel your own projects."
            )

        if project.status not in [
            Project.Status.OPEN,
            Project.Status.IN_PROGRESS,
        ]:
            raise ValidationError(
                "This project cannot be cancelled."
            )

        project.status = Project.Status.CANCELLED
        project.save(update_fields=["status"])

        return Response(
            {
                "message": "Project cancelled successfully.",
                "project_id": project.id,
                "status": project.status,
            },
            status=status.HTTP_200_OK,
        )