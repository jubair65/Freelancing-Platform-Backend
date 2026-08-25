from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User
from projects.models import Project
from proposals.models import Proposal


class ClientDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != User.Role.CLIENT:
            return Response(
                {
                    "detail": "Only clients can access the client dashboard."
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        projects = Project.objects.filter(
            client=request.user
        )

        total_projects = projects.count()

        active_projects = projects.filter(
            status=Project.Status.IN_PROGRESS
        ).count()

        completed_projects = projects.filter(
            status=Project.Status.COMPLETED
        ).count()

        total_proposals_received = Proposal.objects.filter(
            project__client=request.user
        ).count()

        return Response(
            {
                "total_projects": total_projects,
                "active_projects": active_projects,
                "completed_projects": completed_projects,
                "total_proposals_received": total_proposals_received,
            },
            status=status.HTTP_200_OK,
        )


class FreelancerDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != User.Role.FREELANCER:
            return Response(
                {
                    "detail": (
                        "Only freelancers can access "
                        "the freelancer dashboard."
                    )
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        proposals = Proposal.objects.filter(
            freelancer=request.user
        )

        applied_projects = proposals.count()

        active_projects = Project.objects.filter(
            assigned_freelancer=request.user,
            status=Project.Status.IN_PROGRESS,
        ).count()

        completed_projects = Project.objects.filter(
            assigned_freelancer=request.user,
            status=Project.Status.COMPLETED,
        ).count()

        accepted_proposals = proposals.filter(
            status=Proposal.Status.ACCEPTED
        ).count()

        return Response(
            {
                "applied_projects": applied_projects,
                "active_projects": active_projects,
                "completed_projects": completed_projects,
                "accepted_proposals": accepted_proposals,
            },
            status=status.HTTP_200_OK,
        )