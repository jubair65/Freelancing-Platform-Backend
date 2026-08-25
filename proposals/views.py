from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db import transaction
from rest_framework.exceptions import ValidationError

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


class AcceptProposalView(generics.UpdateAPIView):
    serializer_class = ProposalSerializer
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        proposal = get_object_or_404(
            Proposal.objects.select_related("project"),
            id=kwargs["pk"],
        )

        project = proposal.project

        if request.user.role != User.Role.CLIENT:
            raise PermissionDenied(
                "Only clients can accept proposals."
            )

        if project.client_id != request.user.id:
            raise PermissionDenied(
                "You can only manage proposals for your own projects."
            )

        if project.status != Project.Status.OPEN:
            raise ValidationError(
                "Only open projects can accept proposals."
            )

        if proposal.status != Proposal.Status.PENDING:
            raise ValidationError(
                "Only pending proposals can be accepted."
            )

        proposal.status = Proposal.Status.ACCEPTED
        proposal.save(update_fields=["status"])

        Proposal.objects.filter(
            project=project,
            status=Proposal.Status.PENDING,
        ).exclude(
            id=proposal.id
        ).update(
            status=Proposal.Status.REJECTED
        )

        project.assigned_freelancer = proposal.freelancer
        project.status = Project.Status.IN_PROGRESS
        project.save(
            update_fields=[
                "assigned_freelancer",
                "status",
            ]
        )

        return Response(
            {
                "message": "Proposal accepted successfully.",
                "proposal": ProposalSerializer(proposal).data,
                "project_status": project.status,
                "assigned_freelancer": {
                    "id": proposal.freelancer.id,
                    "name": proposal.freelancer.name,
                    "email": proposal.freelancer.email,
                },
            },
            status=status.HTTP_200_OK,
        )


class RejectProposalView(generics.UpdateAPIView):
    serializer_class = ProposalSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        proposal = get_object_or_404(
            Proposal.objects.select_related("project"),
            id=kwargs["pk"],
        )

        if request.user.role != User.Role.CLIENT:
            raise PermissionDenied(
                "Only clients can reject proposals."
            )

        if proposal.project.client_id != request.user.id:
            raise PermissionDenied(
                "You can only manage proposals for your own projects."
            )

        if proposal.status != Proposal.Status.PENDING:
            raise ValidationError(
                "Only pending proposals can be rejected."
            )

        proposal.status = Proposal.Status.REJECTED
        proposal.save(update_fields=["status"])

        return Response(
            {
                "message": "Proposal rejected successfully.",
                "proposal": ProposalSerializer(proposal).data,
            },
            status=status.HTTP_200_OK,
        )