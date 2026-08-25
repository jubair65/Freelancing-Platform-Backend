from django.conf import settings
from django.db import models

from projects.models import Project


class Proposal(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        ACCEPTED = "accepted", "Accepted"
        REJECTED = "rejected", "Rejected"
        WITHDRAWN = "withdrawn", "Withdrawn"

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="proposals",
    )
    freelancer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="proposals",
    )
    bid_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )
    cover_letter = models.TextField()
    delivery_time = models.PositiveIntegerField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["project", "freelancer"],
                name="unique_project_freelancer_proposal",
            )
        ]

    def __str__(self):
        return f"{self.freelancer.email} - {self.project.title}"