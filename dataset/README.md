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
| `preco_brl`              | Preço estimado em reais (R$)                                               |
| `avaliacao`              | Nota média simulada (escala 0–5)                                           |
| `num_avaliacoes`         | Número simulado de avaliações                                             |
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
- **Preço, avaliação e número de avaliações são gerados dentro de faixas
  realistas**, não foram raspados de nenhum site em tempo real — não uso
  ferramentas de scraping/preços ao vivo. Antes de usar em produção,
  vale conferir/atualizar os preços reais junto aos fornecedores ou a uma
  API de preços do seu catálogo.
- **`imagem_url`** aponta para um serviço de placeholder
  (`placehold.co`) com o nome do produto — não são fotos reais dos
  produtos (evita usar imagens de marcas sem licença/verificação). Troque
  pelas imagens reais do seu catálogo antes de publicar no site.
- **`link_produto`** foi deixado vazio de propósito, pelo mesmo motivo:
  evitar inventar URLs de páginas de produto que podem não existir ou
  estar erradas. Preencha com os links reais da loja/parceiro que você for
  usar.

## Regerando ou expandindo o dataset

Para adicionar produtos, edite a lista `PRODUCTS` em `generate_dataset.py`
seguindo a tupla:

```python
(marca, nome, categoria, tipo_pele, preocupacao, modo_uso,
 ingrediente_principal, fps, tamanho_ml, preco_min, preco_max, descricao)
```

e rode novamente `python3 generate_dataset.py`. O `id` é recalculado
automaticamente pela ordem da lista.
