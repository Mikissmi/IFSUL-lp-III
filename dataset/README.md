# Dataset de Produtos de Skincare

Dataset de produtos de skincare vendidos no mercado brasileiro, pensado para
alimentar uma funcionalidade de **recomendação por tipo de pele / rotina**
(ex.: quiz de pele, filtros por preocupação, sugestão de rotina manhã/noite).

## Arquivos

- `produtos_skincare.csv` — dataset final, 125 produtos.
- `generate_dataset.py` — script que gera o CSV a partir do catálogo
  curado. Rode `python3 generate_dataset.py` para regerar o arquivo (útil
  se você adicionar/editar produtos na lista `PRODUCTS`).

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

## Verificação de `link_produto`/`fonte` (101 de 125 produtos)

Uma busca verificou, produto a produto, se ele realmente existe à venda sob
esse nome e encontrou a página real da loja/site oficial — preenchendo
`link_produto` e `fonte` só quando confirmado (sem visitar a página em si,
então `imagem_url`, `preco_brl`, `avaliacao` e `num_avaliacoes` continuam
vazios; isso exige acesso de navegação real, não só busca).

**24 produtos não foram encontrados à venda sob o nome exato do catálogo** —
prova de que alguns nomes/linhas que eu havia assumido como reais mudaram ou
nunca existiram assim no Brasil. Antes de usar esses 24 em produção, vale
corrigir o nome/linha ou trocar por um produto real da mesma marca:

- La Roche-Posay — Effaclar Micro-Peeling Ultra Fino
- Vichy — Normaderm Phytosolution Esfoliante
- Eucerin — Even Brighter Sérum
- Bioderma — Sébium Tonique
- CeraVe — Loção Hidratante Facial SA; Loção Hidratante com FPS 60 (CeraVe BR só vende FPS 50)
- Neutrogena — Visibly Clear Pontos Negros
- L'Oréal Paris — Hyaluron Expert Creme (linha não vendida no Brasil)
- Sallve — Bruma Refrescante; Sérum Niacinamida 10% (só existe a versão 20%); Máscara Hidratante Calmante; Óleo Facial Nutritivo
- Skin1004 — Centella Calming Mask
- Payot — Doctor Payot Sérum Anti-Idade; Dermo Sculpt Creme
- O Boticário — Nativa SPA Ameixa Creme Facial (só existe para corpo/mãos); Photoshow Protetor Solar Facial (linha descontinuada, hoje é "Boti.Sun")
- Natura — Una Água Micelar
- Adcos — Prevent Sérum Antioxidante; Nude Base Hidratante com Cor; Even Creme Clareador (linha atual chama-se "Melan-Off")
- Avène — Hydrance Aqua-Gel; Tolerance Creme
- Granado — Água Micelar Granado (a marca não tem esse produto)

## Regerando ou expandindo o dataset

Para adicionar produtos, edite a lista `PRODUCTS` em `generate_dataset.py`
seguindo a tupla:

```python
(marca, nome, categoria, tipo_pele, preocupacao, modo_uso,
 ingrediente_principal, fps, tamanho_ml, preco_min, preco_max, descricao)
```

e rode novamente `python3 generate_dataset.py`. O `id` é recalculado
automaticamente pela ordem da lista.
