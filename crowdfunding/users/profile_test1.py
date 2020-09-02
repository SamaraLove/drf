from rest_framework import serializers
from .models import CustomUser, Profile

# you could make the ProfileSerializer write_only if 
# you don’t want the UserSerializer to output the profile model’s fields too

class CustomUserSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    username = serializers.CharField(max_length=200)
    email = serializers.CharField(max_length=200)
    password = serializers.CharField(max_length=100)

    # password = serializers.CharField(max_length=100, write_only=True, required=True,style={'input_type': 'password'})

    
    def create(self, validated_data):
        new_user = CustomUser.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        new_user.set_password(validated_data['password'])
        new_user.save()
        return new_user
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
        instance.id = validated_data.get('id', instance.id)
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.password = validated_data.get('password', instance.password)
        instance.save()
        return instance

class ProfileSerializer(serializers.Serializer):
    user = CustomUserSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = "__all__"