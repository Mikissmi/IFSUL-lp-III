#!/usr/bin/env python3
"""
Busca foto, preco e avaliacao reais dos produtos do catalogo, visitando os
links de loja ja verificados (coluna link_produto) com um navegador headless
(Chromium via Playwright, para paginas que carregam o preco via JavaScript) e
lendo os dados estruturados (JSON-LD schema.org/Product, ou meta tags Open
Graph) que a propria pagina do produto expoe para aparecer no Google
Shopping.

So preenche o que ainda esta vazio: nunca sobrescreve uma foto/preco/
avaliacao ja confirmados manualmente. Paginas protegidas por captcha/anti-bot
(ex: alguns grandes varejistas) sao puladas de proposito - nao tentamos
contornar esse tipo de protecao.

Uso:
    pip install playwright beautifulsoup4
    playwright install chromium   # so se os browsers nao estiverem instalados
    python3 buscar_fotos_precos.py produtos_skincare.csv

Gera produtos_skincare.csv.atualizado (nao mexe no arquivo original) -
confira o resultado e renomeie por cima do original quando estiver bom.
"""

import csv
import json
import re
import sys
import time

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

TIMEOUT_MS = 25000
DELAY_ENTRE_REQUISICOES = 1.5  # segundos - nao sobrecarrega os sites
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)
MARCADORES_CAPTCHA = ("não sou um robô", "nao sou um robo", "captcha", "are you a human", "access denied")


def extrair_json_ld_produto(soup):
    for tag in soup.find_all("script", type="application/ld+json"):
        try:
            dados = json.loads(tag.string or "")
        except (json.JSONDecodeError, TypeError):
            continue

        candidatos = dados if isinstance(dados, list) else [dados]
        achatados = []
        for item in candidatos:
            if isinstance(item, dict) and "@graph" in item:
                achatados.extend(item["@graph"])
            else:
                achatados.append(item)

        for item in achatados:
            if isinstance(item, dict) and item.get("@type") in ("Product", ["Product"]):
                return item
    return None


def extrair_imagem(produto_jsonld, soup):
    if produto_jsonld:
        imagem = produto_jsonld.get("image")
        if isinstance(imagem, list) and imagem:
            return imagem[0]
        if isinstance(imagem, str) and imagem:
            return imagem
        if isinstance(imagem, dict) and imagem.get("url"):
            return imagem["url"]

    og_image = soup.find("meta", property="og:image")
    if og_image and og_image.get("content"):
        return og_image["content"]
    return None


def extrair_preco(produto_jsonld, soup):
    if produto_jsonld:
        offers = produto_jsonld.get("offers")
        if isinstance(offers, list) and offers:
            offers = offers[0]
        if isinstance(offers, dict):
            preco = offers.get("price") or offers.get("lowPrice")
            if preco:
                try:
                    return round(float(str(preco).replace(",", ".")), 2)
                except ValueError:
                    pass

    og_preco = soup.find("meta", property="product:price:amount") or soup.find(
        "meta", property="og:price:amount"
    )
    if og_preco and og_preco.get("content"):
        try:
            return round(float(str(og_preco["content"]).replace(",", ".")), 2)
        except ValueError:
            pass
    return None


def extrair_avaliacao(produto_jsonld):
    if not produto_jsonld:
        return None, None
    rating = produto_jsonld.get("aggregateRating")
    if isinstance(rating, dict):
        nota = rating.get("ratingValue")
        qtd = rating.get("reviewCount") or rating.get("ratingCount")
        try:
            nota = round(float(nota), 1) if nota is not None else None
        except (TypeError, ValueError):
            nota = None
        try:
            qtd = int(float(qtd)) if qtd is not None else None
        except (TypeError, ValueError):
            qtd = None
        return nota, qtd
    return None, None


def extrair_fonte(url):
    m = re.search(r"https?://(?:www\.)?([^/]+)", url)
    return m.group(1) if m else ""


def pagina_tem_captcha(texto_visivel):
    texto = texto_visivel.lower()
    return any(marcador in texto for marcador in MARCADORES_CAPTCHA)


def processar_linha(page, linha):
    url = linha.get("link_produto", "").strip()
    if not url:
        return "sem_link"

    tem_imagem = bool(linha.get("imagem_url")) and "placehold.co" not in linha["imagem_url"]
    tem_preco = bool(linha.get("preco_brl"))
    if tem_imagem and tem_preco:
        return "ja_completo"

    try:
        page.goto(url, wait_until="load", timeout=TIMEOUT_MS)
        page.wait_for_timeout(2500)  # da tempo pro JS terminar de montar a pagina
        texto_visivel = page.inner_text("body")
        if pagina_tem_captcha(texto_visivel):
            return "bloqueado_por_captcha"
        html = page.content()
    except Exception as exc:
        print(f"  [erro] {url} -> {exc}")
        return "erro"

    soup = BeautifulSoup(html, "html.parser")
    produto_jsonld = extrair_json_ld_produto(soup)

    achou_algo = False

    if not tem_imagem:
        imagem = extrair_imagem(produto_jsonld, soup)
        if imagem:
            linha["imagem_url"] = imagem
            achou_algo = True

    if not tem_preco:
        preco = extrair_preco(produto_jsonld, soup)
        if preco:
            linha["preco_brl"] = str(preco)
            achou_algo = True

        nota, qtd = extrair_avaliacao(produto_jsonld)
        if nota:
            linha["avaliacao"] = str(nota)
        if qtd:
            linha["num_avaliacoes"] = str(qtd)
        if nota or qtd:
            achou_algo = True

        if preco or nota:
            linha["fonte"] = extrair_fonte(url)

    return "atualizado" if achou_algo else "nada_encontrado"


def remover_imagens_duplicadas(linhas):
    """
    Se a MESMA URL de imagem aparece em produtos diferentes, e quase certo
    que e uma imagem generica (banner de boas-vindas, logo, etc.), nao uma
    foto de produto - limpa essas pra nao mostrar foto errada.
    """
    contagem = {}
    for linha in linhas:
        img = linha.get("imagem_url", "")
        if img and "placehold.co" not in img:
            contagem[img] = contagem.get(img, 0) + 1

    duplicadas = {img for img, qtd in contagem.items() if qtd > 1}
    removidas = 0
    for linha in linhas:
        if linha.get("imagem_url") in duplicadas:
            print(f"  [aviso] imagem duplicada removida: {linha['marca']} - {linha['nome']} ({linha['imagem_url'][:80]})")
            linha["imagem_url"] = ""
            removidas += 1
    return removidas


def main():
    if len(sys.argv) != 2:
        print("Uso: python3 buscar_fotos_precos.py produtos_skincare.csv")
        sys.exit(1)

    caminho_csv = sys.argv[1]
    with open(caminho_csv, encoding="utf-8") as f:
        leitor = csv.DictReader(f)
        fieldnames = leitor.fieldnames
        linhas = list(leitor)

    contagem = {
        "atualizado": 0, "nada_encontrado": 0, "erro": 0,
        "sem_link": 0, "ja_completo": 0, "bloqueado_por_captcha": 0,
    }

    with sync_playwright() as p:
        try:
            browser = p.chromium.launch()
        except Exception:
            # ambiente da sessao Claude: versao instalada nao bate com a que
            # o pacote playwright espera por padrao, entao aponta direto pro
            # executavel. Rodando na sua propria maquina com
            # `playwright install chromium`, esse except nunca deveria disparar.
            browser = p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
        page = browser.new_page(user_agent=USER_AGENT)

        for i, linha in enumerate(linhas, start=1):
            if not linha.get("link_produto"):
                contagem["sem_link"] += 1
                continue

            print(f"[{i}/{len(linhas)}] {linha['marca']} - {linha['nome']}")
            resultado = processar_linha(page, linha)
            contagem[resultado] += 1
            print(f"  -> {resultado}")

            if resultado not in ("sem_link", "ja_completo"):
                time.sleep(DELAY_ENTRE_REQUISICOES)

        browser.close()

    print("\nVerificando imagens duplicadas entre produtos diferentes...")
    removidas = remover_imagens_duplicadas(linhas)

    saida = caminho_csv + ".atualizado"
    with open(saida, "w", newline="", encoding="utf-8") as f:
        escritor = csv.DictWriter(f, fieldnames=fieldnames)
        escritor.writeheader()
        escritor.writerows(linhas)

    print("\nResumo:")
    for chave, valor in contagem.items():
        print(f"  {chave}: {valor}")
    print(f"  imagens duplicadas removidas: {removidas}")
    print(f"\nArquivo gerado: {saida}")
    print("Confira o resultado e, se estiver bom, substitua o produtos_skincare.csv original por ele.")


if __name__ == "__main__":
    main()
