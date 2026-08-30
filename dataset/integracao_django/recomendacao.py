# Salve em: seuapp/recomendacao.py
#
# ATENÇÃO: a função extrair_sinais_faciais() abaixo assume um formato de
# JSON para PerfilDermatologico.dados_ia. Ajuste as chaves lidas em
# `dados.get(...)` para bater com o retorno real da sua API de
# reconhecimento facial.
#
# Formato assumido (exemplo):
# {
#   "tipo_pele_detectado": "oleosa",
#   "acne": true,
#   "manchas": false,
#   "rugas": false,
#   "sensibilidade": false,
#   "oleosidade": 0.72
# }

import json

from django.db.models import Q

from .models import PerfilDermatologico, Produto

# Traduz o valor salvo no questionário/IA (minúsculo) para o rótulo usado
# no dataset (com inicial maiúscula, em "tipo_pele" do Produto)
MAPA_TIPO_PELE = {
    'oleosa': 'Oleosa',
    'seca': 'Seca',
    'mista': 'Mista',
    'normal': 'Normal',
}

# Palavras-chave buscadas no campo livre `objetivo` do questionário,
# mapeadas para os rótulos de `preocupacao` usados no dataset.
PALAVRAS_CHAVE_PREOCUPACAO = {
    'acne': 'Acne', 'espinha': 'Acne',
    'oleosidade': 'Oleosidade', 'oleosa': 'Oleosidade',
    'mancha': 'Manchas', 'melasma': 'Manchas',
    'ruga': 'Rugas e Linhas Finas', 'linha fina': 'Rugas e Linhas Finas',
    'envelhecimento': 'Fotoenvelhecimento',
    'hidrata': 'Hidratação', 'ressecad': 'Hidratação',
    'poro': 'Poros Dilatados', 'crav': 'Poros Dilatados',
    'sensí': 'Sensibilidade/Rosácea', 'rosácea': 'Sensibilidade/Rosácea',
    'vermelhid': 'Sensibilidade/Rosácea',
    'olheira': 'Olheiras',
    'firmeza': 'Firmeza', 'flacidez': 'Firmeza',
    'textura': 'Textura Irregular',
}

CATEGORIA_POR_PREFERENCIA = {
    'creme': {'Hidratante', 'Contorno de Olhos', 'Máscara Facial'},
    'gel': {'Limpeza', 'Sérum', 'Tônico', 'Água Micelar', 'Esfoliante'},
}


def extrair_sinais_faciais(dados_ia_raw):
    """Faz o parse do JSON salvo em PerfilDermatologico.dados_ia."""
    if not dados_ia_raw:
        return {}
    try:
        dados = json.loads(dados_ia_raw)
    except (json.JSONDecodeError, TypeError):
        return {}

    return {
        'tipo_pele_detectado': dados.get('tipo_pele_detectado'),
        'acne': bool(dados.get('acne')),
        'manchas': bool(dados.get('manchas')),
        'rugas': bool(dados.get('rugas')),
        'sensibilidade': bool(dados.get('sensibilidade')),
        'oleosidade': float(dados.get('oleosidade') or 0),
    }


def tipos_pele_compativeis(perfil, sinais_faciais):
    tipos = {'Todos os tipos'}

    tipo_questionario = MAPA_TIPO_PELE.get(perfil.tipo_pele)
    if tipo_questionario:
        tipos.add(tipo_questionario)

    tipo_ia = MAPA_TIPO_PELE.get(sinais_faciais.get('tipo_pele_detectado'))
    if tipo_ia:
        tipos.add(tipo_ia)

    if perfil.idade >= 40:
        tipos.add('Madura')

    if sinais_faciais.get('sensibilidade'):
        tipos.add('Sensível')

    return tipos


def preocupacoes_do_perfil(perfil, sinais_faciais):
    encontradas = set()
    objetivo = (perfil.objetivo or '').lower()

    for palavra, rotulo in PALAVRAS_CHAVE_PREOCUPACAO.items():
        if palavra in objetivo:
            encontradas.add(rotulo)

    if sinais_faciais.get('acne'):
        encontradas.add('Acne')
    if sinais_faciais.get('manchas'):
        encontradas.add('Manchas')
    if sinais_faciais.get('rugas'):
        encontradas.add('Rugas e Linhas Finas')
    if sinais_faciais.get('sensibilidade'):
        encontradas.add('Sensibilidade/Rosácea')
    if sinais_faciais.get('oleosidade', 0) >= 0.5:
        encontradas.add('Oleosidade')

    return encontradas


def recomendar_produtos(perfil: PerfilDermatologico, limite=8):
    """
    Combina o questionário (PerfilDermatologico) com os sinais da IA
    facial (PerfilDermatologico.dados_ia) para pontuar e ordenar os
    produtos mais adequados.
    """
    sinais_faciais = extrair_sinais_faciais(perfil.dados_ia)
    tipos_compat = tipos_pele_compativeis(perfil, sinais_faciais)
    preocupacoes = preocupacoes_do_perfil(perfil, sinais_faciais)
    categorias_preferidas = CATEGORIA_POR_PREFERENCIA.get(
        perfil.preferencia_produto, set()
    )

    filtro_tipo_pele = Q()
    for tipo in tipos_compat:
        filtro_tipo_pele |= Q(tipo_pele__icontains=tipo)

    candidatos = Produto.objects.filter(filtro_tipo_pele)

    pontuados = []
    for produto in candidatos:
        pontos = 0.0
        pontos += 2 * len(preocupacoes & set(produto.preocupacoes()))
        if produto.categoria in categorias_preferidas:
            pontos += 1
        pontos += float(produto.avaliacao) * 0.1  # desempate por nota
        pontuados.append((pontos, produto))

    pontuados.sort(key=lambda item: item[0], reverse=True)
    return [produto for _, produto in pontuados[:limite]]
