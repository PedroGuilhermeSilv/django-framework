from rest_framework import serializers 
from .models import Category
from tag.models import Tag

class TagSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField()
    # name = serializers.CharField(max_length=255)
    # slug = serializers.SlugField()
    class Meta:
        model = Tag
        fields = ['id','name','slug']

class RecipeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=500)
    description = serializers.CharField(max_length=165)
    preparation = serializers.SerializerMethodField()
    def get_preparation(self,recipe):
        return f'{recipe.preparation_time} {recipe.preparation_time_unit}'
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all()
    )

    category_name = serializers.StringRelatedField(
        source='category'
    )
    author = serializers.StringRelatedField()
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    tag_object = TagSerializer(many=True,source='tags')
    tag_links =serializers.HyperlinkedRelatedField(
        many=True,
        source='tags',
        queryset=Tag.objects.all(),
        view_name='recipes:recipe_api_v2_tag'
        )
