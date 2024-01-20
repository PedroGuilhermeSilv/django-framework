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
from .models import Category
from tag.models import Tag

class TagSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    slug = serializers.SlugField()

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

```
### PrimaryKeyRelatedField
- Para serializar campos que possuem relacionamento como `category` que é uma ForeignKey, podemos utilizar o PrimaryKeyRelatedField:
    1. Usando `PrimaryKeyRelatedField` passamos uma queryset com a busca que ele deve fazer no banco e nos retornará o id dessa categoria e se for um relacionamento many to many devemos informar que `many=True`.

### SerializerMethodField()
- Podemos também fazer o response com a junção de dois atributos.
    1. Pimeiro, adicione o atributo na classe serializer com o método “SerializerMethodField()”.
    2. Depois adicione uma função chamada get_nomedoatributo().
    3. Nesta função retorne os valores desejados.

### StringRelatedField()
- Ao utilizar StringRelatedField e implementar a classe __str__ no modelo, especificamos o atributo relacionado no source. Isso resultará no retorno do atributo configurado na classe __str__.

    1. Ao criar a classe serializadora para o atributo, podemos instanciá-la para obter todos os objetos desejados.

### HyperlinkedRelatedField
- Este campo simplifica a representação de relacionamentos ao criar hiperlinks automáticos para os objetos relacionados.
    1. Crie o atributo serializer com o método `HyperlinkedRelatedField` e passe os seguintes parâmetros:
    - many: Se será mais de um objeto.
    - source: o atributo referente ao model.
    - queryset: como deve buscar no banco.
    - view_name: a rota que ele deve se referenciar.

### ModelSerializer
- Em vez de serializar atributo por atributo podemos utilizar o MoldeSerializer para fazer isso de maneira "automática".
1. Cria a classe serializadora passando como parâmetro `serializer.ModelSerializer`.
2. Detro desta classe crie uma subclasse Meta.
3. Informe o model de referência e os fields desejados:
```
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id','name','slug']
```
### Decoretors api_view
- No django rest podemos usar um decoretor em nossa view para referênciar essa rota class view. Podemos passar alguns parâmetros como  `@api_view(http_method_names=['GET'])` informando os métodos https suportados.

### Serializer para recebimento de dados.
- O serializer desempenha um papel crucial, não apenas convertendo nosso objeto de consulta para JSON, mas também realizando o processo inverso ao receber dados via JSON. Existem algumas diferenças nos argumentos entre essas duas operações. Ao enviar dados, utilizamos uma instância, enquanto ao receber, usamos o parâmetro 'data'. Além disso, a função is_valid() é essencial para verificar quais campos são obrigatórios em nosso modelo. 
```
@api_view(http_method_names=["get", "post"])
def recipe_api_list(request):
    if request.method == "GET":
        recipes = Recipe.objects.get_published()[:10]
        serializer = RecipeSerializer(
            instance=recipes, many=True, context={"request": request}
        )
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = RecipeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

```
### Validate no Serializer
- É possível personalizar a validação dos dados por meio da função validate(self, attrs). No arquivo do seu serializador, adicione essa função se desejar usar mais de um argumento para validação. Caso prefira validar de forma individual, é necessário criar uma função no formato validate_nomeatributo(self, value). Dessa maneira, somente o atributo desejado será passado. Ao levantar uma exceção, também é essencial utilizar o erro do serializador, raise serializers.ValidationError(), para que o Django Rest Framework o reconheça como uma requisição inválida (bad request).

```
    def validate(self, attrs):
        super_validate = super().validate(attrs)
        title = attrs.get('title')
        description = attrs.get('description')
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
        if len(title) < 5:
            raise serializers.ValidationError('Must have at least 5 chars.')
        return title
```