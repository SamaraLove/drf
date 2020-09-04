from rest_framework import serializers
from .models import Project, Pledge, Category
from django.utils import timezone
# from django.db.models import Sum

class CategorySerializer(serializers.Serializer):
    # queryset = Project.objects.all()
    # serializer_class = CategoryProjectSerializer
    # lookup_field = 'category'
    # queryset = request.GET.get("category")
    category = serializers.CharField(max_length=100)
    lookup_field = 'category'
        
    def create(self, validated_data):
        return Category.objects.create(**validated_data)

class ProjectSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    title = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=None)
    goal = serializers.IntegerField()
    image = serializers.URLField()
    is_open = serializers.BooleanField()
    date_created = serializers.DateTimeField()
    company = serializers.CharField(required=False,max_length=100)
    deadline = serializers.DateField()
    # owner = serializers.CharField(max_length=200)
    owner = serializers.ReadOnlyField(source='owner.username')

    category = serializers.SlugRelatedField(queryset = Category.objects.all(), read_only = False, slug_field='category')
    # vehicle_category = serializers.SlugRelatedField(queryset = Category.objects.all(), read_only = False, slug_field='vehicle_category')

    last_update_at = serializers.DateTimeField()
    # is_backing = serializers.BooleanField()

    def create(self, validated_data):
        return Project.objects.create(**validated_data)

    # def get_progress_goal(self,obj):
    #     queryset = Pledge.objects.all()
    #     total = 0
    #     for instance in queryset:
    #         total += instance.amount
    #     return total


    # class Meta:
    #     model = Project
    
    # def get_category(self,obj):
    #     return obj.get_category_display()

    # def get_vehicle_category(self,obj):
    #     return obj.get_vehicle_category_display()
        


class CategoryProjectSerializer(CategorySerializer):
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
    pledge_total = serializers.SerializerMethodField(read_only=True)

    no_of_pledges = serializers.SerializerMethodField(read_only=True)
    biggest_contribution = serializers.SerializerMethodField(read_only=True)
    
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
        # instance.vehicle_category = validated_data.get('vehicle_category', instance.vehicle_category)
        instance.save()
        return instance
    
    def get_pledge_total(self, obj):
        queryset = Pledge.objects.filter(project = obj.id)        
        total = 0
        for instance in queryset:
            total += instance.amount
        return total
    
    def get_no_of_pledges(self, obj):
        queryset = Pledge.objects.filter(project = obj.id)        
        total = 0
        for instance in queryset:
            total += instance.amount
            # print (total)
        return total

    def get_biggest_contribution(self,obj):
        queryset = Pledge.objects.filter(project = obj.id)        
        amount = 0
        for instance in queryset:
            if amount > instance.amount or amount == instance.amount:
                amount = amount
                # name = instance.supporter
            else: 
                amount = instance.amount
                # print(amount)
                # name = instance.supporter
                # print(name)
        return amount

class ProjectTotalSerializer(ProjectSerializer):
    pledge_total = serializers.SerializerMethodField(read_only=True)
    no_of_pledges = serializers.SerializerMethodField(read_only=True)
    biggest_contributor= serializers.SerializerMethodField(read_only=True)

    def get_pledge_total(self, obj):
        queryset = Pledge.objects.all()
        queryset = Pledge.objects.filter(project = obj.id)   
        total = 0
        for instance in queryset:
            total += instance.amount
        return total
    
    def get_no_of_pledges(self, obj):
        queryset = Pledge.objects.all(project = obj.id)
        total = 0
        for instance in queryset:
            total += instance.amount
            # print (total)
        return total
    
    def get_biggest_contributor(self,obj):
        queryset = Pledge.objects.all(project = obj.id)
        amount = 0
        for instance in queryset:
            if amount > instance.amount or amount == instance.amount:
                amount = amount
            else: 
                amount = instance.amount
                # name = instance.supporter
        return amount