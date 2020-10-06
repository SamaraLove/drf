from rest_framework import serializers
from .models import CustomUser, Profile

class ProfileSerializer(serializers.Serializer):
    # rating = serializers.IntegerField(required=False)
    created = serializers.DateTimeField(required=Fals)
    updated = serializers.DateTimeField(required=Fals)
    # profile_img = serializers.ImageField(required=False, allow_empty_file=True)
    profile_img = serializers.URLField(required=False)
    bio = serializers.CharField(required=False, max_length=500)
    location = serializers.CharField(required=False, max_length=30)

class CustomUserSerializer(serializers.ModelSerializer):
    userprofile = ProfileSerializer()

    password = serializers.CharField(max_length=100, write_only=True, required=True,style={'input_type': 'password'})
    # password = serializers.CharField(max_length=100)
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password','userprofile']
        lookup_field = 'username'

    def create(self, validated_data):
        password = validated_data.pop('password')
        userprofile_data = validated_data.pop('userprofile')
        new_user = CustomUser.objects.create(**validated_data)
        Profile.objects.create(user=new_user, **userprofile_data)
        new_user.set_password(password)
        new_user.save()
        return new_user

    def update(self, instance, validated_data):
        userprofile_data = validated_data.pop('userprofile')
        # Unless the application properly enforces that this field is
        # always set, the following could raise a `DoesNotExist`, which
        # would need to be handled.
        try:
            userprofile = instance.userprofile
        except CustomUser.userprofile.RelatedObjectDoesNotExist:
            userprofile = Profile.objects.create(user=instance, **userprofile_data)

        instance.id = validated_data.get('id', instance.id)
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.password = validated_data.get('password', instance.password)
        instance.save()

        userprofile.created = userprofile_data.get(
            'created',
            userprofile.created
        )
        userprofile.updated = userprofile_data.get(
            'updated',
            userprofile.updated
        )
        # userprofile.rating = userprofile_data.get(
        #     'rating',
        #     userprofile.rating
        # )
        userprofile.profile_img = userprofile_data.get(
            'profile_img',
            userprofile.profile_img
        )
        userprofile.bio = userprofile_data.get(
            'bio',
            userprofile.bio
        )
        userprofile.location = userprofile_data.get(
            'location',
            userprofile.location
        )

        userprofile.save()
        return instance

