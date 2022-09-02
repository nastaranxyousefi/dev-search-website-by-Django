from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import ProjectSerializer, ReviewSerializer
from projects.models import Project, Review, Tag

@api_view(['GET'])
def get_routes(request):
    routes = [
        {'GET':'/api/projects/'},
        {'GET': '/api/projects/id'},
        {'POST': '/api/projects/id/vote'},

        {'POST':'/api/token'},
        {'POST': '/api/token/refresh'},
    ]
    return Response(routes)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_projects(request):
    print('user:', request.user)
    print('user email:', request.user.email)
    projects = Project.objects.all()
    project_serialize = ProjectSerializer(projects, many=True)

    return Response(project_serialize.data)


@api_view(['GET'])
def get_project(request, pk):
    project = Project.objects.get(id=pk)
    project_serialize = ProjectSerializer(project, many=False)

    return Response(project_serialize.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def project_vote(request, pk):
    project = Project.objects.get(id=pk)
    user = request.user.profile
    posted_data = request.data

    review, created = Review.objects.get_or_create(
        owner = user,
        project = project,
    )

    review.value = posted_data['value']
    review.body = posted_data['body']
    review.save()
    project.get_vote_count

    print(posted_data['value'])
    project_serialize = ProjectSerializer(project, many=False)
    return Response(project_serialize.data)


@api_view(['DELETE'])
def remove_tag(request):
    tagId = request.data['tag']
    projectId = request.data['project']

    project = Project.objects.get(id=projectId)
    tag = Tag.objects.get(id=tagId)

    project.tags.remove(tag)

    return Response('tag was deleted!')
