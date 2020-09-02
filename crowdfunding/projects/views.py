from django.http import Http404
from rest_framework import status, permissions,generics
from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework import status
from .models import Project, Pledge, Category
from .serializers import ProjectSerializer, PledgeSerializer, ProjectDetailSerializer, CategoryProjectSerializer, CategorySerializer
from .permissions import IsOwnerOrReadOnly, isSuperUser

class CategoryList(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, isSuperUser]


    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
        
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
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

class ProjectListAuthor(generics.ListAPIView):
    serializer_class = ProjectSerializer
    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Project.objects.all()
        username = self.request.query_params.get('username', None)
        category = self.request.query_params.get('category', None)
        if username is not None:
            queryset = queryset.filter(owner__username=username)
        if category is not None:
            queryset = queryset.filter(category=category)
        return queryset


    # def get_queryset(self):
    #     return Project.objects.all()  

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['Project'] = Project.objects.all().order_by('category')
#         return context

class CategoryProject(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, isSuperUser]
    
    # queryset = Project.objects.all()
    # serializer_class = CategoryProjectSerializer
    # lookup_field = 'category'
    # queryset = request.GET.get("category")
    queryset = Category.objects.all()
    serializer_class = CategoryProjectSerializer
    lookup_field = 'category'

    # def get_queryset(self):
    #     '''Return all projects.'''
    #     qs = Project.objects.all()   
    #     q = self.request.GET.get("category")
    #     if q: 
    #         qs = qs.filter(category=q)
    #     return qs
    
# http://localhost:8000/news/filter/?cuisine_type=American


# class Category(APIView):
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#     queryset = Project.objects.all()
#     serializer_class = ProjectSerializer

#     def get_object(self, pk):
#         try:
#             return Project.objects.get(pk=pk)
#         except Project.DoesNotExist:
#             raise Http404


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
