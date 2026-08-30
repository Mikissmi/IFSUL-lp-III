# Integrando o dataset ao projeto Django + MySQL

Arquivos de referência para copiar para o seu projeto (que já tem
`Usuario`, `PerfilDermatologico`, `Artigo`, `Especialista`).

## Passo a passo

1. **Adicione o model.** Copie o conteúdo de `models_produto.py` para o
   final do `models.py` do seu app (o mesmo onde estão `Usuario` e
   `PerfilDermatologico`).

2. **Gere e aplique a migration:**
   ```bash
   python manage.py makemigrations seuapp
   python manage.py migrate
   ```

3. **Crie o comando de import.** Copie
   `management/commands/import_produtos_csv.py` para
   `seuapp/management/commands/import_produtos_csv.py` (crie também
   `seuapp/management/__init__.py` e
   `seuapp/management/commands/__init__.py`, vazios). Troque o
   `from seuapp.models import Produto` pelo nome real do seu app.

4. **Importe o CSV:**
   ```bash
   python manage.py import_produtos_csv caminho/para/produtos_skincare.csv
   ```
   O comando usa `update_or_create` pela `slug`, então rodar de novo
   depois de editar o CSV apenas atualiza os registros — não duplica.

5. **Adicione a lógica de recomendação.** Copie `recomendacao.py` para
   `seuapp/recomendacao.py`.

6. **Exponha numa view.** Veja `views_exemplo.py` como ponto de partida
   e registre a URL correspondente no seu `urls.py`.

## Sobre a combinação questionário + IA facial

`recomendar_produtos(perfil)` faz duas coisas:

- **Filtro obrigatório por tipo de pele**: usa `PerfilDermatologico.tipo_pele`
  (do questionário) + o tipo detectado pela IA (se houver) + `idade` (>= 40
  também libera produtos "Madura") + sinal de sensibilidade da IA (libera
  "Sensível"). Produtos marcados como "Todos os tipos" sempre entram.
- **Pontuação por preocupação**: cruza palavras-chave do campo livre
  `objetivo` do questionário com os flags vindos da IA (`acne`, `manchas`,
  `rugas`, `sensibilidade`, `oleosidade`) contra a coluna `preocupacao` de
  cada produto, e soma pontos por correspondência. `preferencia_produto`
  (creme/gel) dá um pequeno bônus de categoria. No fim, ordena por
  pontuação e desempata pela `avaliacao`.

### ⚠️ Ajuste obrigatório: formato do `dados_ia`

A função `extrair_sinais_faciais()` em `recomendacao.py` assume que
`PerfilDermatologico.dados_ia` guarda um JSON como:

```json
{
  "tipo_pele_detectado": "oleosa",
  "acne": true,
  "manchas": false,
  "rugas": false,
  "sensibilidade": false,
  "oleosidade": 0.72
}
```

Como o formato real da sua API de reconhecimento facial pode ter nomes de
campos diferentes, **troque as chaves lidas em `dados.get(...)`** dentro
dessa função para bater com o retorno real. É o único lugar do código que
precisa mudar — todo o resto (filtro de tipo de pele, pontuação de
preocupação) já consome o dicionário normalizado que essa função devolve.
