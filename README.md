# Django Rest Framework

## Seção 25: Django Rest Framework - Criando uma API (Application Programming Interface)

### Aula 281 - Primeira Function Based view
- Tanto o django web quanto o django rest possuem seus métodos de http response para lidar com as requisições http. Pelo lado web ele enviará templates e pelo lado do rest será enviado jsons.

### Aula 282 até 285
- Serializer: No Django, é necessário utilizar serializers, os quais transformarão dicionários Python em arquivos JSON por meio de respostas HTTP. Essa abordagem lembra muito a criação dos models, seguindo a mesma linha de raciocínio.

views.py
```
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
```

serializer.py
```
from rest_framework import serializers

class RecipeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=500)
    description = serializers.CharField(max_length=165)
    preparation = serializers.SerializerMethodField()
    def get_preparation(self,recipe):
        return f'{recipe.preparation_time} {recipe.preparation_time_unit}'
```

- É possível juntar dois atributos e retornar no http response:
1. Pimeiro, adicione o atributo na classe serializer com o método “SerializerMethodField()”.
2. Depois adicione uma função chamada get_nomedoatributo(): e retorne os atributos desejado.



