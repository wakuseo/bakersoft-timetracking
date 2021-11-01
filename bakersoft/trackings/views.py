from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from bakersoft.trackings.models import Project, Work
from bakersoft.trackings.serializers import ProjectSerializer, WorkSerializer


class ProjectViewSet(
    RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet
):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()

    @action(detail=True, methods=["POST"])
    def complete(self, request, pk=None):
        """Endpoint to complete a task and return the related obj"""
        project = get_object_or_404(self.get_queryset(), pk=pk)
        project.complete()
        serializer = self.serializer_class(project)

        return Response(status=status.HTTP_200_OK, data=serializer.data)


class WorkViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = WorkSerializer
    queryset = Work.objects.all()

    @action(detail=True, methods=["POST"])
    def complete(self, request, pk=None):
        """Endpoint to complete a task and return the related obj"""
        work = get_object_or_404(self.get_queryset(), pk=pk)
        work.complete()
        serializer = self.serializer_class(work)

        return Response(status=status.HTTP_200_OK, data=serializer.data)
