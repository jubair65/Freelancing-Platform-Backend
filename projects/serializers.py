from rest_framework import serializers

from .models import Project


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            "id",
            "client",
            "assigned_freelancer",
            "title",
            "category",
            "budget",
            "description",
            "required_skills",
            "deadline",
            "experience_level",
            "status",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "client",
            "assigned_freelancer",
            "status",
            "created_at",
        ]

    def validate_budget(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Budget must be greater than zero."
            )
        return value