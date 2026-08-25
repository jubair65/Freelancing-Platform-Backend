from rest_framework import serializers

from .models import Proposal


class ProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proposal
        fields = [
            "id",
            "project",
            "freelancer",
            "bid_amount",
            "cover_letter",
            "delivery_time",
            "status",
            "submitted_at",
        ]
        read_only_fields = [
            "id",
            "project",
            "freelancer",
            "status",
            "submitted_at",
        ]

    def validate_bid_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Bid amount must be greater than zero."
            )
        return value

    def validate_delivery_time(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Delivery time must be greater than zero."
            )
        return value