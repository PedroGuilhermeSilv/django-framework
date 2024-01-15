from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..models import Recipe
from ..serializers import RecipeSerializer
from rest_framework import status


@api_view()
def recipe_api_list(request):
   recipes= Recipe.objects.get_published()[:10]
   serializer = RecipeSerializer(instance=recipes,many=True)
   return Response(serializer.data)

@api_view()
def recipe_api_detail(request,pk):
   recipe= Recipe.objects.get_published.filter(pk=pk).first()
   if recipe:
    serializer = RecipeSerializer(instance=recipe)
    return Response(serializer.data)
   else:
    return Response({"detail":"not found"}, status=status.HTTP_404_NOT_FOUND)