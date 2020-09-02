# Alex way
from rest_framework import serializers
from .models import CustomUser, Profile

# you could make the ProfileSerializer write_only if 
# you don’t want the UserSerializer to output the profile model’s fields too

class ProfileSerializer(serializers.Serializer):
    # user = CustomUserSerializer(many=True, read_only=True)
    rating = serializers.IntegerField()
    created = serializers.DateTimeField()
    updated = serializers.DateTimeField()
    # class Meta:
    #     model = Profile
    #     fields = "__all__"

class CustomUserSerializer(serializers.ModelSerializer):
    userprofile = ProfileSerializer()
    # id = serializers.ReadOnlyField()
    # username = serializers.CharField(max_length=200)
    # email = serializers.CharField(max_length=200)
    # password = serializers.CharField(max_length=100)

    # password = serializers.CharField(max_length=100, write_only=True, required=True,style={'input_type': 'password'})

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password','userprofile']


    
    def create(self, validated_data):
        userprofile_data = validated_data.pop('userprofile')
        new_user = CustomUser.objects.create(**validated_data)
        Profile.objects.create(user=new_user, **userprofile_data)
        return new_user
        # new_user = CustomUser.objects.create(
        #     username=validated_data['username'],
        #     email=validated_data['email']
        # )
        # new_user.set_password(validated_data['password'])
        # new_user.save()
  
        # return CustomUser.objects.create(**validated_data)

    # def update(self, instance, validated_data):
    #     CustomUser = super().update(instance, validated_data)
    #     try:
    #         CustomUser.set_password(validated_data['password'])
    #         CustomUser.save()
    #     except KeyError:
    #         pass
    #     return CustomUser

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
        userprofile.rating = userprofile_data.get(
            'rating',
            userprofile.rating
        )
        userprofile.save()
        return instance

