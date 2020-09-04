from django.http import Http404
from rest_framework import status, permissions, generics, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Project, Pledge, Category
from .serializers import ProjectSerializer, PledgeSerializer, ProjectDetailSerializer, CategoryProjectSerializer, CategorySerializer, ProjectTotalSerializer
from .permissions import IsOwnerOrReadOnly, isSuperUser

class CategoryList(APIView):
    permission_classes = [isSuperUser,permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
        
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
       
        if serializer.is_valid():
            print(request.user.is_superuser)

            if (request.user.is_superuser):

                serializer.save()
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                    )
        return Response(
            serializer.errors,
            status=status.HTTP_401_UNAUTHORIZED
            )

class ProjectList(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProjectSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class FilterView(generics.ListAPIView):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['category', 'deadline', 'owner']
    # def get_queryset(self):
    #     queryset = Project.objects.all()
    #     ...
    #     category = self.request.query_params.get('category', None)
    #     date_created = self.request.query_params.get('date_created', None)
    #     ...
    #     if category is not None:
    #         queryset = queryset.filter(category=category)
    #     if date_created is not None:
    #         queryset = queryset.filter(date_created=date_created)
    #     return queryset

class CategoryProject(generics.RetrieveAPIView):
    permission_classes = [isSuperUser]
    queryset = Category.objects.all()
    serializer_class = CategoryProjectSerializer
    lookup_field = 'category'

class ProjectDetail(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = Project.objects.all()
    serializer_class = ProjectDetailSerializer

    def get_object(self, pk):
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise Http404
    
    def get(self, request, pk):
        project = self.get_object(pk)
        serializer = ProjectDetailSerializer(project)
        return Response(serializer.data)

    def put(self, request, pk):
        project = self.get_object(pk)
        self.check_object_permissions(request, project)
        data = request.data
        serializer = ProjectDetailSerializer(
            instance=project,
            data=data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        project = self.get_object(pk)
        self.check_object_permissions(request, project)

        try:
            project.delete()
            return Response(status = status.HTTP_204_NO_CONTENT)
        except Project.DoesNotExist:
            raise Http404

class PledgeList(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        pledges = Pledge.objects.all()
        serializer = PledgeSerializer(pledges, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = PledgeSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(supporter=request.user)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class PledgeDetail(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]

    def get_object(self, pk):
        try:
            return Pledge.objects.get(pk=pk)
        except Pledge.DoesNotExist:
            raise Http404
    
    def get(self, request, pk):
        pledge = self.get_object(pk)
        serializer = PledgeSerializer(pledge)
        return Response(serializer.data)

    def put(self, request, pk):
        pledge = self.get_object(pk)
        self.check_object_permissions(request, pledge)
        data = request.data
        serializer = PledgeSerializer(
            instance=pledge,
            data=data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data, 
                status = status.HTTP_201_CREATED
            )
        return Response (
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
    def delete(self, request, pk):
        pledge = self.get_object(pk)
        self.check_object_permissions(request, pledge)

        try:
            pledge.delete()
            return Response(status = status.HTTP_204_NO_CONTENT)
        except Pledge.DoesNotExist:
            raise Http404

class ProjectTotals(APIView):
    
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        projects = Project.objects.all()
        serializer = ProjectTotalSerializer(projects, many=True)
        return Response(serializer.data)