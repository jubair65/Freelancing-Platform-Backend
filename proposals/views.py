from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.models import User
from projects.models import Project

from .models import Proposal
from .permissions import IsFreelancer
from .serializers import ProposalSerializer


class CreateProposalView(generics.CreateAPIView):
    serializer_class = ProposalSerializer
    permission_classes = [IsAuthenticated, IsFreelancer]

    def perform_create(self, serializer):
        project_id = self.kwargs["project_id"]

        project = get_object_or_404(
            Project,
            id=project_id,
        )

        if project.status != Project.Status.OPEN:
            raise PermissionDenied(
                "Proposals can only be submitted to open projects."
            )

        serializer.save(
            project=project,
            freelancer=self.request.user,
        )


class MyProposalsView(generics.ListAPIView):
    serializer_class = ProposalSerializer
    permission_classes = [
        IsAuthenticated,
        IsFreelancer,
    ]

    def get_queryset(self):
        return Proposal.objects.filter(
            freelancer=self.request.user
        ).select_related(
            "project",
            "freelancer",
        ).order_by("-submitted_at")


class ProjectProposalsView(generics.ListAPIView):
    serializer_class = ProposalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        project_id = self.kwargs["project_id"]

        project = get_object_or_404(
            Project,
            id=project_id,
        )

        if project.client_id != self.request.user.id:
            raise PermissionDenied(
                "You can only view proposals for your own projects."
            )

        return Proposal.objects.filter(
            project=project
        ).select_related(
            "project",
            "freelancer",
        ).order_by("-submitted_at")


class WithdrawProposalView(generics.DestroyAPIView):
    serializer_class = ProposalSerializer
    permission_classes = [
        IsAuthenticated,
        IsFreelancer,
    ]

    def get_queryset(self):
        return Proposal.objects.filter(
            freelancer=self.request.user,
            status=Proposal.Status.PENDING,
        )

    def perform_destroy(self, instance):
        instance.status = Proposal.Status.WITHDRAWN
        instance.save(
            update_fields=["status"]
        )