from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, generics, viewsets
from .models import CustomUser, Profile
from .serializers import CustomUserSerializer, ProfileSerializer
from .permissions import IsOwnerOrReadOnly, isSuperUser
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied

# https://stackoverflow.com/questions/55913920/django-rest-framework-displaying-the-users-profile

# class Profile(APIView):
#     # serializer_class = ProfileSerializer

#     def get(self, request, *args, **kwargs):
#         user = get_object_or_404(CustomUser, pk=kwargs['user_id'])
#         print (user)
#         # print (user.userprofile)

#         profile_serializer = ProfileSerializer(user.userprofile)
#         return Response(profile_serializer.data)
    
    # def get_object(self, pk):
    #     try:
    #         return Projects.objects.get(pk=pk)
    #     except Projects.DoesNotExist:
    #         raise Http404
    

    # def get_queryset(self):
    #     return Profile.objects.filter(user=self.kwargs['user_id'])

    # def get_queryset(self):
    #     """
    #     This view should return a list of all the purchases
    #     for the currently authenticated user.
    #     """
    #     user = self.request.user
    #     return Projects.objects.filter(owner__username=user)

class CustomUserList(APIView):
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

class CustomUserDetail(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly, isSuperUser]

    def get_object(self, pk):
        try:
            return CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)


    def put(self, request, pk):
        user = self.get_object(pk)
        self.check_object_permissions(request, user)
        data = request.data
        serializer = CustomUserSerializer(
            instance=user,
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
        user = self.get_object(pk)
        self.check_object_permissions(request, user)

        try:
            user.delete()
            return Response(status = status.HTTP_204_NO_CONTENT)
        except CustomUser.DoesNotExist:
            raise Http404
# raise PermissionDenied()



# class Profile(viewsets.ViewSet):
#     def get(self, request, *args, **kwargs):
#         user = get_object_or_404(CustomUser, pk=kwargs['user_id'])
#         profile_serializer = ProfileSerializer(user.profile)
#         return Response(profile_serializer.data)