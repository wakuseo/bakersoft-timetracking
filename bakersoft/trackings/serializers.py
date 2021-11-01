from rest_framework import serializers

from bakersoft.trackings.models import Project, Work


class WorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Work
        fields = ["uuid", "name", "status", "completed", "elapsed_time"]


class ProjectSerializer(serializers.ModelSerializer):
    works = WorkSerializer(read_only=True, many=True)

    class Meta:
        model = Project
        fields = [
            "uuid",
            "name",
            "manager",
            "status",
            "completed",
            "elapsed_time",
            "works",
        ]
