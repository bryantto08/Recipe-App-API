"""
Serializers for recipe APIs
"""

from rest_framework import serializers

from core.models import Recipe, Tag, Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for Ingredients"""
    class Meta:
        model = Ingredient
        fields = ["id", "name"]
        read_only_fields = ["id"]

class TagSerializer(serializers.ModelSerializer):
    """Serializer for Tags"""
    class Meta:
        model = Tag
        fields = [
            "id", "name"
        ]
        read_only_fields = ["id"]

class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipes"""
    # Nesting Serializers
    tags = TagSerializer(many=True, required=False)  # List of Tags in Recipe Serializer
    ingredients = IngredientSerializer(many=True, required=False)
    class Meta:
        model = Recipe
        fields = [
            "id", "title", "time_minutes","price", "link", "tags", "ingredients", "image"
        ]
        read_only_fields = ["id"]
    
    def _get_or_create_tags(self, tags, recipe):  # Edited get_or_create
        """Handle getting or creating tags as needed"""
        auth_user = self.context["request"].user  # Getting Authenticated User
        
        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(  # Original get or create
                user=auth_user,
                **tag,
            )
            recipe.tags.add(tag_obj)

    def _get_or_create_ingredients(self, ingredients, recipe):
        """Handle getting or creating ingredients as needed"""
        auth_user = self.context["request"].user

        for ingredient in ingredients: # Loop through ingredient
            ingredient_obj, create = Ingredient.objects.get_or_create (
                user=auth_user,  # Get or create an ingredient obj
                **ingredient,
            )
            # add that obj to the recipe ingredient attr
            recipe.ingredients.add(ingredient_obj)

    """
    Validated data is the data passed when the user sends data to api
    """
    def create(self, validated_data):
        """Create a recipe."""
        """
        We want to remove tags from validated data because the tag attr in
        recipes is a ManyToMany field meaning that it connects Tag Models to the Recipe
        Model. Thus, we have to create the Tag Model First and then add it seperately
        """
        tags = validated_data.pop("tags", [])  # Remove tag data from validated data
        ingredients = validated_data.pop("ingredients",[])
        recipe = Recipe.objects.create(**validated_data)
        self._get_or_create_tags(tags, recipe) 
        self._get_or_create_ingredients(ingredients, recipe) 

        return recipe

    """
    Instance provides current recipe object. Since this is the update
    Method, an instance already exists as opposed to a create method
    where it doesnt exist
    """
    def update(self, instance, validated_data):
        """Update recipe: for better understanding: Video 101"""
        tags = validated_data.pop("tags", None)
        ingredients = validated_data.pop("ingredients", None)
        if tags is not None:
            instance.tags.clear()
            self._get_or_create_tags(tags, instance)
        
        if ingredients is not None:
            instance.ingredients.clear()  # Clear all ingredients first
            # Add all ingredients saved in the ingredients variable
            self._get_or_create_ingredients(ingredients, instance)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for recipe detail view which is an extension of 
    Recipe Serializer which is why that is the base class
    """

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ["description"]


class RecipeImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading images to recipes"""

    class Meta:
        model = Recipe
        fields = ["id", "image"]
        read_only_fields = ["id"]
        extra_kwargs = {"image": {"required": "True"}}
    