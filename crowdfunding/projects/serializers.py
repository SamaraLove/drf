from rest_framework import serializers
from .models import Project, Pledge
from django.utils import timezone

class ProjectSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    title = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=None)
    goal = serializers.IntegerField()
    image = serializers.URLField()
    is_open = serializers.BooleanField()
    date_created = serializers.DateTimeField()
    # owner = serializers.CharField(max_length=200)
    owner = serializers.ReadOnlyField(source='owner.username')
    category  = serializers.ChoiceField(choices=Project.CATEGORY_CHOICES)
    vehicle_category = serializers.ChoiceField(choices=Project.VehicleType_CHOICES)
    
    def create(self, validated_data):
        return Project.objects.create(**validated_data)

    class Meta:
        model = Project
    
    # def get_category(self,obj):
    #     return obj.get_category_display()

    # def get_vehicle_category(self,obj):
    #     return obj.get_vehicle_category_display()
        
class CategoryProjectSerializer(serializers.Serializer):
    project_categories = ProjectSerializer(many=True, read_only=True)


    

class PledgeSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    amount = serializers.IntegerField()
    comment = serializers.CharField(max_length=200)
    anonymous = serializers.BooleanField()
    # supporter = serializers.CharField(max_length=200)
    supporter = serializers.ReadOnlyField(source='supporter.username')
    project_id = serializers.IntegerField()

    def create(self, validated_data):
        return Pledge.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.amount = validated_data.get('amount', instance.amount)
        instance.comment = validated_data.get('comment', instance.comment)
        instance.anonymous = validated_data.get('anonymous', instance.anonymous)
        instance.supporter = validated_data.get('supporter', instance.supporter)
        instance.project_id = validated_data.get('project_id', instance.project_id)
        instance.save()
        return instance

class ProjectDetailSerializer(ProjectSerializer):
    pledges = PledgeSerializer(many=True, read_only=True)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.goal = validated_data.get('goal', instance.goal)
        instance.image = validated_data.get('image', instance.image)
        instance.is_open = validated_data.get('is_open', instance.is_open)
        instance.date_created = validated_data.get('date_created', instance.date_created)
        instance.owner = validated_data.get('owner', instance.owner)
        instance.category = validated_data.get('category', instance.category)
        instance.vehicle_category = validated_data.get('vehicle_category', instance.vehicle_category)
        instance.save()
        return instance