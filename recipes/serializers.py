from rest_framework import serializers
from .models import Category
from tag.models import Tag
from .models import Recipe
from attr import attrs
from collections import defaultdict


class TagSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField()
    # name = serializers.CharField(max_length=255)
    # slug = serializers.SlugField()
    class Meta:
        model = Tag
        fields = ["id", "name", "slug"]


class RecipeSerializer(serializers.Serializer):
    class Meta:
        model = Recipe
        fields = [
            "id",
            "title",
            "description",
            "author",
            "category",
            "tags",
            "public",
            "preparation",
            "tag_objects",
            "tag_links",
        ]

    public = serializers.BooleanField(
        source="is_published",
        read_only=True,
    )
    preparation = serializers.SerializerMethodField(
        method_name="any_method_name",
        read_only=True,
    )
    category = serializers.StringRelatedField(
        read_only=True,
    )
    tag_objects = TagSerializer(
        many=True,
        source="tags",
        read_only=True,
    )
    tag_links = serializers.HyperlinkedRelatedField(
        many=True,
        source="tags",
        view_name="recipes:recipes_api_v2_tag",
        read_only=True,
    )

    def any_method_name(self, recipe):
        return f"{recipe.preparation_time} {recipe.preparation_time_unit}"

    def validate(self, attrs):
        super_validate = super().validate(attrs)
        print("atributis", attrs.get("title"))

        title = attrs.get("title")
        description = attrs.get("description")

        if title == description:
            raise serializers.ValidationError(
                {
                    "title": ["Posso", "ter", "mais de um erro"],
                    "description": ["Posso", "ter", "mais de um erro"],
                }
            )

        return super_validate

    def validate_title(self, value):
        title = value
        print('title', title)

        if len(title) < 5:
            raise serializers.ValidationError("Must have at least 5 chars.")

        return title
