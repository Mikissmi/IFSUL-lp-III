# Dataset de Produtos de Skincare

Dataset de produtos de skincare vendidos no mercado brasileiro, pensado para
alimentar uma funcionalidade de **recomendação por tipo de pele / rotina**
(ex.: quiz de pele, filtros por preocupação, sugestão de rotina manhã/noite).

## Arquivos

- `produtos_skincare.csv` — dataset final, 125 produtos.
- `generate_dataset.py` — script que gera o CSV a partir do catálogo
  curado. Rode `python3 generate_dataset.py` para regerar o arquivo (útil
  se você adicionar/editar produtos na lista `PRODUCTS`). **Atenção:**
  regerar por cima do CSV atual apaga `link_produto`/`fonte`/`imagem_url`
  reais já preenchidos — não rode isso depois de ter coletado dados reais,
  a menos que também atualize a lista `PRODUCTS`.
- `buscar_fotos_precos.py` — script que visita os `link_produto` já
  verificados com um navegador headless (Playwright/Chromium, pois várias
  lojas só carregam preço via JavaScript) e extrai foto/preço/avaliação
  reais lendo o JSON-LD schema.org/Product que a própria loja expõe (o
  mesmo dado usado pelo Google Shopping), com fallback para meta tags Open
  Graph. Só aceita preço confirmado em `priceCurrency: BRL` (descarta preço
  em outra moeda, ex. sites internacionais) e remove imagens que se repetem
  em produtos diferentes (sinal de banner genérico, não foto de produto).
  Só preenche o que está vazio — nunca sobrescreve dado já confirmado
  manualmente.
  ```bash
  pip install playwright beautifulsoup4
  playwright install chromium   # só se os browsers ainda não estiverem instalados
  python3 buscar_fotos_precos.py produtos_skincare.csv
  ```
  Gera `produtos_skincare.csv.atualizado` (não mexe no original) — confira
  o resultado antes de substituir. Precisa rodar numa máquina/ambiente com
  saída de rede liberada para os domínios das lojas (por padrão, a sessão
  de execução do Claude bloqueia saída de rede externa por política da
  organização — foi preciso liberar isso nas configurações do ambiente
  antes de rodar aqui).

  **Limitações conhecidas:** Época Cosméticos, Amazon, Sephora, Droga Raia/
  Drogasil/Panvel (mesmo grupo RD) e Beleza na Web bloqueiam coleta
  automatizada (captcha ou HTTP 403/503 consistente) — **não tentamos
  contornar isso**, nem usamos Amazon por causa dos termos de uso dela.
  Quando um produto só existia nessas lojas, buscamos o mesmo produto em
  lojas alternativas (farmácias como Pague Menos, Ultrafarma, Drogal,
  Callfarma etc.) antes de desistir. Resultado atual, de 125 produtos:
  **84 com foto real, 61 com preço real (BRL confirmado), 21 com avaliação
  real.**

## Colunas

| Coluna                  | Descrição                                                                 |
|--------------------------|----------------------------------------------------------------------------|
| `id`                     | Identificador numérico sequencial do produto                              |
| `marca`                  | Marca real do produto (ex.: La Roche-Posay, Sallve, CeraVe)                |
| `nome`                   | Nome real do produto                                                       |
| `categoria`              | Limpeza, Água Micelar, Tônico, Sérum, Hidratante, Protetor Solar, Esfoliante, Máscara Facial, Óleo Facial, Contorno de Olhos |
| `tipo_pele`              | Tipo(s) de pele indicado(s), separados por `;` (Oleosa, Seca, Mista, Sensível, Normal, Madura, Todos os tipos) |
| `preocupacao`            | Preocupação(ões) que o produto trata, separadas por `;` (Acne, Oleosidade, Manchas, Rugas e Linhas Finas, Hidratação, Poros Dilatados, Sensibilidade/Rosácea, Olheiras, Firmeza, Textura Irregular, Fotoenvelhecimento) |
| `modo_uso`               | Manhã, Noite, ou Manhã e Noite                                             |
| `ingrediente_principal`  | Ativo/ingrediente de destaque do produto                                  |
| `fps`                    | Fator de proteção solar (preenchido apenas para `categoria = Protetor Solar`) |
| `tamanho_ml`             | Tamanho/volume da embalagem, em ml                                         |
| `preco_brl`              | Vazio de propósito — só preencher com preço confirmado numa fonte real (ver abaixo) |
| `avaliacao`              | Vazio de propósito — só preencher com nota confirmada numa fonte real (ver abaixo) |
| `num_avaliacoes`         | Vazio de propósito — idem                                                  |
| `fonte`                  | Vazio — nome do site de onde vieram `preco_brl`/`avaliacao`/`num_avaliacoes` (ex.: "Época Cosméticos"), pra deixar claro pro usuário final de onde saiu o dado |
| `descricao`              | Descrição curta do produto                                                 |
| `imagem_url`             | URL de imagem placeholder (ver observação abaixo)                          |
| `link_produto`           | Vazio — preencher com o link real do produto no seu catálogo/loja          |
| `slug`                   | Identificador amigável em formato URL (`marca-nome`), útil como chave/rota |

`tipo_pele` e `preocupacao` são multivalorados: separe por `;` ao processar
(ex.: `"Oleosa;Mista"` → `["Oleosa", "Mista"]`). Isso deixa o CSV simples
(um arquivo só, como pedido) mas ainda permite casar produtos com múltiplos
perfis de pele/preocupação na lógica de recomendação.

## Como os dados foram construídos (e limitações importantes)

- **Marca, nome, categoria, ingrediente principal e tamanho** são baseados
  em produtos reais e amplamente conhecidos, vendidos no Brasil (farmácia,
  Sephora, Época Cosméticos, Beleza na Web etc.), cobrindo ~35 marcas.
- **Preço, avaliação, número de avaliações e fonte ficam vazios de
  propósito.** A primeira versão deste dataset gerava esses valores dentro
  de faixas realistas — mas um número fabricado, mesmo "realista", ainda é
  fabricado: mostrar isso pro usuário final como se fosse avaliação de
  verdade é prova social falsa. Preencha essas quatro colunas só quando
  tiver uma fonte real e verificável (uma página de produto de loja/site
  oficial) — e guarde o link dessa página em `link_produto`, pra o próprio
  usuário poder conferir/comprar. Enquanto uma linha não tiver `fonte`
  preenchida, a interface deve tratar preço/avaliação como "não
  verificado", não esconder o fato de que é um vazio.
- **`imagem_url`** aponta para um serviço de placeholder
  (`placehold.co`) com o nome do produto — não são fotos reais dos
  produtos (evita usar imagens de marcas sem licença/verificação). Troque
  pelas imagens reais do seu catálogo antes de publicar no site.
- **`link_produto`** foi deixado vazio de propósito, pelo mesmo motivo:
  evitar inventar URLs de páginas de produto que podem não existir ou
  estar erradas. Preencha com os links reais da loja/parceiro que você for
  usar.

## Verificação de dados reais (duas rodadas de pesquisa)

Produto a produto, verificamos se cada um existe à venda sob esse nome
exato, visitando a página real da loja (não só buscando) e lendo o preço/
imagem/avaliação direto do HTML — em duas rodadas: primeiro nas lojas mais
óbvias (Época Cosméticos, Amazon, site oficial da marca), depois, para quem
ainda faltava, numa busca por lojas alternativas (farmácias, outros
varejistas) quando a loja original bloqueava a coleta.

**41 produtos continuam sem foto/preço verificados**, ou porque a loja
acessível bloqueia a coleta de dados (Beleza na Web, Vult, Quem Disse
Berenice, COSRX One Step Pimple Clear Pad), ou porque o nome/linha do
catálogo não bate com nada realmente à venda no Brasil hoje — nomes mudaram,
produto é só internacional, ou a linha foi descontinuada/renomeada:

- Vichy — Aqualia Thermal
- Eucerin — Even Brighter Sérum (linha atual se chama "Anti-Pigment")
- Bioderma — Photoderm Max; Sébium Tonique; Sensibio Máscara Calmante
- CeraVe — Loção Hidratante Facial SA; Sérum de Vitamina C; Loção com FPS 60 (CeraVe BR só vende FPS 50, sem "SA" facial, sem vitamina C)
- Neutrogena — Facial Oil-Free Acne Wash; Visibly Clear Pontos Negros (loja BR vende como linha "Purified Skin")
- L'Oréal Paris — Hyaluron Expert Creme (linha não vendida no Brasil)
- Sallve — Bruma Refrescante; Sérum Niacinamida 10% (só existe a versão 20%); Máscara Hidratante Calmante; Óleo Facial Nutritivo (parecem descontinuados)
- The Ordinary — Peeling Solution AHA 30% + BHA 2% (único preço BR achado estava esgotado)
- COSRX — One Step Pimple Clear Pad (só em lojas bloqueadas)
- Skin1004 — Centella Calming Mask (produto exato não existe, só a "Watergel Ampoule Mask")
- Payot — Doctor Payot Sérum Anti-Idade; Dermo Sculpt Creme
- O Boticário — Nativa SPA Ameixa Creme Facial (só existe para corpo/mãos); Photoshow Protetor Solar Facial (linha descontinuada, hoje é "Boti.Sun")
- Natura — Una Água Micelar (linha "Una" não vende água micelar)
- Quem disse, Berenice? — Água Micelar QDB (só em lojas bloqueadas)
- Simple — Micellar Cleansing Water
- Cetaphil — Moisturizing Cream (só achado em kit, imagem serviria pra 2 produtos)
- SkinCeuticals — Hydrating B5 Gel
- Adcos — Prevent Sérum Antioxidante; Nude Base Hidratante com Cor; Even Creme Clareador (linha atual chama-se "Melan-Off")
- Dermage — Sun Protect Fluid Colorless (só achado com cor)
- Isdin — Fotoprotector Fusion Fluid (só achada a linha "Fusion Water", produto diferente)
- Nuxe — Huile Prodigieuse; Creme Fraîche de Beauté (só lojas internacionais)
- Avène — Hydrance Aqua-Gel; Tolerance Creme
- Granado — Água Micelar Granado (a marca não tem esse produto)
- Racco — Sérum Facial Ácido Hialurônico; Protetor Solar Facial (marca de venda direta/revendedora, sem preço público)
- Vult — Protetor Solar Facial (site oficial bloqueia a coleta)
- L'Occitane en Provence — Immortelle Creme Divine (só achado em USD/lojas internacionais)

Antes de usar esses 41 em produção, vale corrigir o nome/linha ou trocar
por um produto real da mesma marca.

## Regerando ou expandindo o dataset

Para adicionar produtos, edite a lista `PRODUCTS` em `generate_dataset.py`
seguindo a tupla:

```python
(marca, nome, categoria, tipo_pele, preocupacao, modo_uso,
 ingrediente_principal, fps, tamanho_ml, preco_min, preco_max, descricao)
```

e rode novamente `python3 generate_dataset.py`. O `id` é recalculado
automaticamente pela ordem da lista.
