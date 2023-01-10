from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import ProjectSerializer
from project.models import Project, Review

class GetRoutes(APIView):
    def get(self, request, *args, **kwargs):
        routes = [
           {'GET': 'api/projects'},
           {'GET': 'api/projects/id'},
           {'POST': 'api/projects/id/vote'},
           {'POST': 'api/users/token'},
           {'POST': 'api/users/token/refresh'},
         ]
        return Response(routes)

class GetProjects(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        projects = Project.objects.all()

        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

class GetProject(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk, *args, **kwargs):
       project = Project.objects.get(id=pk)

       serializer = ProjectSerializer(project)
       return Response(serializer.data)

    def post(self, request, pk, *args, **kwargs):
        project = Project.objects.get(id=pk)
        user = request.user.profile
        data = request.data
        
        review, created = Review.objects.get_or_create(owner=user, project=project)
        reviewvalue = data['value']
        review.save()
        project.getvotecount

        serializer = ProjectSerializer(project)

        return Response(serializer.data)

