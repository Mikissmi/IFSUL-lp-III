# Exemplo de view que expõe a recomendação. Adapte para sua URL/serializer
# (DRF, JsonResponse puro, template, etc.)

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .models import PerfilDermatologico
from .recomendacao import recomendar_produtos


@login_required
def produtos_recomendados(request):
    try:
        perfil = PerfilDermatologico.objects.get(usuario=request.user)
    except PerfilDermatologico.DoesNotExist:
        return JsonResponse(
            {'erro': 'Usuário ainda não preencheu o perfil dermatológico.'},
            status=404,
        )

    produtos = recomendar_produtos(perfil)

    dados = [
        {
            'id': p.id,
            'marca': p.marca,
            'nome': p.nome,
            'categoria': p.categoria,
            'preco': str(p.preco),
            'avaliacao': str(p.avaliacao),
            'imagem_url': p.imagem_url,
            'link_produto': p.link_produto,
        }
        for p in produtos
    ]
    return JsonResponse({'produtos': dados})
