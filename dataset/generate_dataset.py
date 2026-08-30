"""
Gerador do dataset de produtos de skincare (produtos_skincare.csv).

O catalogo abaixo reune marcas e produtos reais, vendidos no mercado
brasileiro, organizados com os campos necessarios para uma funcionalidade
de recomendacao por tipo de pele / rotina (tipo de pele, preocupacao,
modo de uso, ingrediente principal, etc).

Preco, avaliacao e numero de avaliacoes sao gerados dentro de faixas
realistas para cada produto (ver README.md do dataset para detalhes e
limitacoes). Rode `python3 generate_dataset.py` para regerar o CSV.
"""

import csv
import random

random.seed(42)

# (marca, nome, categoria, tipo_pele, preocupacao, modo_uso,
#  ingrediente_principal, fps, tamanho_ml, preco_min, preco_max, descricao)
PRODUCTS = [
    # La Roche-Posay
    ("La Roche-Posay", "Effaclar Duo(+) M", "Hidratante", "Oleosa;Mista", "Acne;Oleosidade;Poros Dilatados", "Manhã e Noite", "Ácido Salicílico", "", 40, 90, 120, "Tratamento anti-imperfeições com efeito matificante e correção de manchas residuais de acne."),
    ("La Roche-Posay", "Effaclar Gel de Limpeza", "Limpeza", "Oleosa;Mista", "Acne;Oleosidade", "Manhã e Noite", "Zinco PCA", "", 200, 60, 85, "Gel de limpeza para peles oleosas e com tendência a acne."),
    ("La Roche-Posay", "Toleriane Dermallergo Creme", "Hidratante", "Sensível;Seca", "Sensibilidade/Rosácea;Hidratação", "Manhã e Noite", "Manteiga de Karité", "", 40, 95, 130, "Hidratante para peles sensíveis e reativas, sem perfume."),
    ("La Roche-Posay", "Anthelios XL", "Protetor Solar", "Todos os tipos", "Fotoenvelhecimento", "Manhã", "Filtro UVA/UVB", 60, 50, 90, 140, "Protetor solar de alta proteção para peles sensíveis."),
    ("La Roche-Posay", "Cicaplast Baume B5", "Hidratante", "Sensível;Seca", "Sensibilidade/Rosácea;Hidratação", "Manhã e Noite", "Pantenol", "", 40, 70, 100, "Bálsamo reparador multiuso para peles irritadas ou fragilizadas."),
    ("La Roche-Posay", "Hyalu B5 Sérum", "Sérum", "Todos os tipos", "Hidratação;Rugas e Linhas Finas", "Manhã e Noite", "Ácido Hialurônico", "", 30, 180, 230, "Sérum antienvelhecimento com dupla ação de ácido hialurônico."),
    ("La Roche-Posay", "Mela B3 Sérum", "Sérum", "Todos os tipos", "Manchas", "Noite", "Niacinamida", "", 30, 200, 250, "Sérum para redução de manchas e uniformização do tom de pele."),
    ("La Roche-Posay", "Lipikar Baume AP+M", "Hidratante", "Seca", "Hidratação;Sensibilidade/Rosácea", "Manhã e Noite", "Manteiga de Karité", "", 200, 80, 110, "Bálsamo emoliente para peles muito secas."),
    ("La Roche-Posay", "Effaclar Micro-Peeling Ultra Fino", "Esfoliante", "Oleosa;Mista", "Textura Irregular;Poros Dilatados", "Noite", "Ácido Salicílico", "", 40, 100, 130, "Esfoliante facial suave para peles oleosas."),
    ("La Roche-Posay", "Pigmentclar Olhos", "Contorno de Olhos", "Todos os tipos", "Olheiras;Manchas", "Manhã e Noite", "Vitamina C", "", 15, 130, 160, "Creme para contorno dos olhos com efeito iluminador."),

    # Vichy
    ("Vichy", "Mineral 89", "Sérum", "Todos os tipos", "Hidratação;Fotoenvelhecimento", "Manhã e Noite", "Ácido Hialurônico", "", 50, 110, 150, "Sérum fortificante e reparador diário com água vulcânica."),
    ("Vichy", "Normaderm Phytosolution", "Hidratante", "Oleosa;Mista", "Acne;Oleosidade", "Manhã e Noite", "Ácido Salicílico", "", 50, 90, 120, "Hidratante anti-imperfeições para peles oleosas."),
    ("Vichy", "Liftactiv Vitamina C", "Sérum", "Todos os tipos", "Manchas;Fotoenvelhecimento", "Manhã", "Vitamina C", "", 20, 180, 220, "Sérum antioxidante iluminador com vitamina C pura."),
    ("Vichy", "Liftactiv Colágeno Specialist", "Hidratante", "Todos os tipos", "Rugas e Linhas Finas;Firmeza", "Manhã e Noite", "Colágeno", "", 50, 140, 180, "Creme antirrugas e firmeza para rosto e pescoço."),
    ("Vichy", "Capital Soleil", "Protetor Solar", "Todos os tipos", "Fotoenvelhecimento", "Manhã", "Filtro UVA/UVB", 60, 40, 85, 130, "Protetor solar toque seco para o rosto."),
    ("Vichy", "Aqualia Thermal", "Hidratante", "Seca;Normal", "Hidratação", "Manhã e Noite", "Ácido Hialurônico", "", 50, 100, 140, "Hidratante reidratante de 48h para peles desidratadas."),
    ("Vichy", "Normaderm Phytosolution Esfoliante", "Esfoliante", "Oleosa;Mista", "Textura Irregular;Acne", "Noite", "Ácido Salicílico", "", 75, 95, 125, "Esfoliante para peles com tendência a acne."),
    ("Vichy", "Mineral Masks Purificante", "Máscara Facial", "Oleosa;Mista", "Oleosidade;Poros Dilatados", "Noite", "Argila", "", 75, 95, 125, "Máscara de argila purificante."),
    ("Vichy", "Liftactiv Cuidado Olhos", "Contorno de Olhos", "Madura", "Rugas e Linhas Finas;Olheiras", "Manhã e Noite", "Cafeína", "", 15, 140, 175, "Creme antirrugas para o contorno dos olhos."),
    ("Vichy", "Normaderm Tônico", "Tônico", "Oleosa;Mista", "Acne;Oleosidade", "Manhã e Noite", "Ácido Salicílico", "", 200, 75, 100, "Tônico adstringente para peles com tendência a acne."),

    # Eucerin
    ("Eucerin", "DermoPure Gel de Limpeza", "Limpeza", "Oleosa;Mista", "Acne;Oleosidade", "Manhã e Noite", "Ácido Salicílico", "", 200, 55, 80, "Gel de limpeza para peles oleosas com tendência à acne."),
    ("Eucerin", "DermoPure Oil Control", "Protetor Solar", "Oleosa;Mista", "Acne;Oleosidade;Fotoenvelhecimento", "Manhã", "Filtro Solar", 30, 50, 70, 100, "Protetor solar com efeito matificante para peles oleosas."),
    ("Eucerin", "Hyaluron-Filler Sérum", "Sérum", "Todos os tipos", "Rugas e Linhas Finas", "Noite", "Ácido Hialurônico", "", 30, 150, 190, "Sérum antirrugas de preenchimento imediato."),
    ("Eucerin", "UreaRepair Plus Loção", "Hidratante", "Seca", "Hidratação", "Manhã e Noite", "Ureia", "", 250, 90, 120, "Loção hidratante para peles muito secas."),
    ("Eucerin", "Even Brighter Sérum", "Sérum", "Todos os tipos", "Manchas", "Manhã e Noite", "Vitamina C", "", 30, 160, 200, "Sérum clareador de manchas escuras."),
    ("Eucerin", "Hyaluron-Filler Olhos", "Contorno de Olhos", "Madura", "Rugas e Linhas Finas;Olheiras", "Manhã e Noite", "Ácido Hialurônico", "", 15, 150, 185, "Creme de preenchimento para o contorno dos olhos."),

    # Bioderma
    ("Bioderma", "Sensibio H2O", "Água Micelar", "Sensível", "Sensibilidade/Rosácea", "Manhã e Noite", "Água Micelar", "", 500, 70, 100, "Água micelar de limpeza e demaquilante para peles sensíveis."),
    ("Bioderma", "Sébium H2O", "Água Micelar", "Oleosa;Mista", "Acne;Oleosidade", "Manhã e Noite", "Água Micelar", "", 500, 75, 105, "Água micelar para peles oleosas e mistas."),
    ("Bioderma", "Hydrabio H2O", "Água Micelar", "Seca;Normal", "Hidratação", "Manhã e Noite", "Água Micelar", "", 500, 75, 105, "Água micelar hidratante para peles desidratadas."),
    ("Bioderma", "Atoderm Creme", "Hidratante", "Seca;Sensível", "Hidratação;Sensibilidade/Rosácea", "Manhã e Noite", "Manteiga de Karité", "", 200, 85, 115, "Creme nutritivo para peles secas a muito secas."),
    ("Bioderma", "Photoderm Max", "Protetor Solar", "Todos os tipos", "Fotoenvelhecimento", "Manhã", "Filtro Solar", 50, 40, 100, 140, "Protetor solar de alta proteção para peles sensíveis."),
    ("Bioderma", "Sébium Tonique", "Tônico", "Oleosa;Mista", "Oleosidade;Poros Dilatados", "Manhã e Noite", "Zinco", "", 200, 80, 110, "Tônico purificante para peles oleosas."),
    ("Bioderma", "Sensibio Máscara Calmante", "Máscara Facial", "Sensível", "Sensibilidade/Rosácea", "Noite", "Água Termal", "", 75, 90, 120, "Máscara calmante para peles sensíveis."),

    # CeraVe
    ("CeraVe", "Creme Hidratante Facial", "Hidratante", "Seca;Normal", "Hidratação", "Manhã e Noite", "Ceramidas", "", 45, 60, 90, "Hidratante facial com ceramidas e ácido hialurônico."),
    ("CeraVe", "Gel de Limpeza Facial", "Limpeza", "Oleosa;Mista", "Oleosidade;Acne", "Manhã e Noite", "Ceramidas", "", 236, 55, 80, "Gel de limpeza para peles normais a oleosas."),
    ("CeraVe", "Loção Hidratante Facial SA", "Hidratante", "Oleosa;Mista", "Textura Irregular;Poros Dilatados", "Manhã e Noite", "Ácido Salicílico", "", 56, 65, 90, "Loção hidratante esfoliante com ácido salicílico."),
    ("CeraVe", "Sérum de Vitamina C", "Sérum", "Todos os tipos", "Manchas;Fotoenvelhecimento", "Manhã", "Vitamina C", "", 30, 100, 140, "Sérum antioxidante com vitamina C pura e ácido hialurônico."),
    ("CeraVe", "Loção Hidratante com FPS 60", "Protetor Solar", "Todos os tipos", "Fotoenvelhecimento", "Manhã", "Filtro Solar", 60, 50, 70, 100, "Hidratante facial com proteção solar diária."),
    ("CeraVe", "Creme para Área dos Olhos", "Contorno de Olhos", "Todos os tipos", "Olheiras;Rugas e Linhas Finas", "Manhã e Noite", "Ceramidas", "", 14, 70, 100, "Creme hidratante para o contorno dos olhos."),
    ("CeraVe", "Sabonete Líquido Hidratante Facial", "Limpeza", "Seca;Sensível", "Hidratação;Sensibilidade/Rosácea", "Manhã e Noite", "Ceramidas", "", 236, 55, 80, "Sabonete líquido de limpeza suave para peles secas e sensíveis."),

    # Neutrogena
    ("Neutrogena", "Hydro Boost Gel-Creme", "Hidratante", "Oleosa;Mista;Normal", "Hidratação", "Manhã e Noite", "Ácido Hialurônico", "", 50, 60, 90, "Gel-creme hidratante de rápida absorção."),
    ("Neutrogena", "Hydro Boost Água-Gel", "Hidratante", "Oleosa;Mista", "Hidratação", "Manhã e Noite", "Ácido Hialurônico", "", 50, 55, 80, "Hidratante em gel leve para peles oleosas."),
    ("Neutrogena", "Facial Oil-Free Acne Wash", "Limpeza", "Oleosa", "Acne;Oleosidade", "Manhã e Noite", "Ácido Salicílico", "", 175, 40, 60, "Gel de limpeza para controle de oleosidade e acne."),
    ("Neutrogena", "Visibly Clear Pontos Negros", "Limpeza", "Oleosa;Mista", "Poros Dilatados;Oleosidade", "Manhã e Noite", "Ácido Salicílico", "", 150, 35, 55, "Gel de limpeza para poros dilatados e cravos."),
    ("Neutrogena", "Sun Fresh", "Protetor Solar", "Todos os tipos", "Fotoenvelhecimento", "Manhã", "Filtro Solar", 30, 40, 45, 70, "Protetor solar toque seco de rápida absorção."),
    ("Neutrogena", "Esfoliante Facial Deep Clean", "Esfoliante", "Normal;Mista", "Textura Irregular;Poros Dilatados", "Noite", "Microesferas", "", 150, 30, 45, "Esfoliante de limpeza profunda."),

    # Nivea
    ("Nivea", "Creme Nivea", "Hidratante", "Seca", "Hidratação", "Manhã e Noite", "Glicerina", "", 100, 15, 25, "Creme hidratante multiuso clássico."),
    ("Nivea", "Nivea Soft", "Hidratante", "Normal;Mista", "Hidratação", "Manhã e Noite", "Vitamina E", "", 100, 18, 28, "Creme hidratante leve de rápida absorção."),
    ("Nivea", "Q10 Power Antirrugas", "Hidratante", "Normal;Madura", "Rugas e Linhas Finas", "Noite", "Coenzima Q10", "", 50, 35, 50, "Creme antirrugas noturno com coenzima Q10."),

    # L'Oréal Paris
    ("L'Oréal Paris", "Revitalift Ácido Hialurônico", "Sérum", "Todos os tipos", "Rugas e Linhas Finas;Hidratação", "Manhã e Noite", "Ácido Hialurônico", "", 30, 60, 90, "Sérum antirrugas com ácido hialurônico puro."),
    ("L'Oréal Paris", "Revitalift Creme Antirrugas", "Hidratante", "Madura;Normal", "Rugas e Linhas Finas;Firmeza", "Noite", "Pró-Retinol", "", 50, 55, 80, "Creme antirrugas com pró-retinol."),
    ("L'Oréal Paris", "Hyaluron Expert Creme", "Hidratante", "Todos os tipos", "Hidratação", "Manhã e Noite", "Ácido Hialurônico", "", 50, 45, 65, "Creme hidratante de reposição de volume."),

    # Sallve
    ("Sallve", "Gel de Limpeza Facial", "Limpeza", "Oleosa;Mista", "Oleosidade;Acne", "Manhã e Noite", "Ácido Salicílico", "", 150, 40, 55, "Gel de limpeza suave para o dia a dia."),
    ("Sallve", "Água Micelar", "Água Micelar", "Todos os tipos", "Hidratação", "Manhã e Noite", "Água Micelar", "", 200, 35, 50, "Água micelar de limpeza e remoção de maquiagem."),
    ("Sallve", "Sérum Vitamina C 10%", "Sérum", "Todos os tipos", "Manchas;Fotoenvelhecimento", "Manhã", "Vitamina C", "", 30, 90, 120, "Sérum antioxidante e iluminador com vitamina C estabilizada."),
    ("Sallve", "Protetor Solar Facial", "Protetor Solar", "Todos os tipos", "Fotoenvelhecimento", "Manhã", "Filtro Solar", 60, 50, 65, 90, "Protetor solar com toque seco e cor universal."),
    ("Sallve", "Bruma Refrescante", "Tônico", "Todos os tipos", "Hidratação", "Manhã e Noite", "Extrato de Pepino", "", 120, 40, 55, "Bruma facial refrescante e calmante."),
    ("Sallve", "Máscara de Argila Verde", "Máscara Facial", "Oleosa;Mista", "Oleosidade;Poros Dilatados", "Noite", "Argila Verde", "", 75, 45, 60, "Máscara de argila para controle de oleosidade."),
    ("Sallve", "Sérum Niacinamida 10%", "Sérum", "Oleosa;Mista", "Oleosidade;Poros Dilatados;Manchas", "Noite", "Niacinamida", "", 30, 70, 95, "Sérum para controle de oleosidade e poros."),
    ("Sallve", "Máscara Hidratante Calmante", "Máscara Facial", "Seca;Sensível", "Hidratação;Sensibilidade/Rosácea", "Noite", "Centella Asiática", "", 75, 55, 75, "Máscara hidratante e calmante."),
    ("Sallve", "Óleo Facial Nutritivo", "Óleo Facial", "Seca", "Hidratação", "Noite", "Óleo de Rosa Mosqueta", "", 30, 65, 85, "Óleo facial nutritivo para peles secas."),

    # The Ordinary
    ("The Ordinary", "Niacinamide 10% + Zinc 1%", "Sérum", "Oleosa;Mista", "Oleosidade;Poros Dilatados;Acne", "Manhã e Noite", "Niacinamida", "", 30, 60, 85, "Sérum de alta concentração para controle de oleosidade."),
    ("The Ordinary", "Hyaluronic Acid 2% + B5", "Sérum", "Todos os tipos", "Hidratação", "Manhã e Noite", "Ácido Hialurônico", "", 30, 65, 90, "Sérum hidratante multi-peso de ácido hialurônico."),
    ("The Ordinary", "Retinol 0.5% in Squalane", "Sérum", "Normal;Madura", "Rugas e Linhas Finas;Textura Irregular", "Noite", "Retinol", "", 30, 75, 100, "Sérum antienvelhecimento com retinol em base de esqualano."),
    ("The Ordinary", "Peeling Solution AHA 30% + BHA 2%", "Esfoliante", "Oleosa;Mista", "Textura Irregular;Poros Dilatados", "Noite", "Ácido Glicólico", "", 30, 70, 95, "Esfoliante químico intensivo de uso semanal."),
    ("The Ordinary", "Vitamin C Suspension 23% + HA Spheres 2%", "Sérum", "Normal;Mista", "Manchas;Fotoenvelhecimento", "Manhã", "Vitamina C", "", 30, 85, 110, "Sérum de altíssima concentração de vitamina C pura."),
    ("The Ordinary", "Salicylic Acid 2% Solution", "Tônico", "Oleosa;Mista", "Acne;Poros Dilatados", "Noite", "Ácido Salicílico", "", 240, 60, 85, "Tônico esfoliante para desobstrução dos poros."),

    # Beauty of Joseon
    ("Beauty of Joseon", "Glow Deep Serum", "Sérum", "Todos os tipos", "Manchas;Textura Irregular", "Manhã e Noite", "Niacinamida", "", 30, 75, 100, "Sérum iluminador com niacinamida e arroz fermentado."),
    ("Beauty of Joseon", "Relief Sun Rice + Probiotics", "Protetor Solar", "Todos os tipos", "Fotoenvelhecimento", "Manhã", "Filtro Solar", 50, 50, 80, 110, "Protetor solar leve com extrato de arroz."),
    ("Beauty of Joseon", "Dynasty Cream", "Hidratante", "Seca;Madura", "Rugas e Linhas Finas;Hidratação", "Noite", "Ginseng", "", 50, 130, 160, "Creme nutritivo antienvelhecimento com ginseng e óleo de camélia."),
    ("Beauty of Joseon", "Ginseng Essence Water", "Tônico", "Todos os tipos", "Hidratação", "Manhã e Noite", "Ginseng", "", 150, 70, 95, "Tônico hidratante e revitalizante."),

    # COSRX
    ("COSRX", "Advanced Snail 96 Mucin Power Essence", "Sérum", "Todos os tipos", "Hidratação;Textura Irregular", "Manhã e Noite", "Mucina de Caracol", "", 100, 90, 120, "Essência hidratante e reparadora com mucina de caracol."),
    ("COSRX", "Low pH Good Morning Gel Cleanser", "Limpeza", "Todos os tipos", "Oleosidade;Sensibilidade/Rosácea", "Manhã", "Extrato de Chá Verde", "", 150, 55, 75, "Gel de limpeza de baixo pH para uso matinal."),
    ("COSRX", "AHA/BHA Clarifying Treatment Toner", "Tônico", "Oleosa;Mista", "Textura Irregular;Poros Dilatados", "Noite", "Ácido Salicílico", "", 150, 75, 100, "Tônico esfoliante clarificador."),
    ("COSRX", "Salicylic Acid Daily Gentle Cleanser", "Limpeza", "Oleosa;Mista", "Acne;Oleosidade", "Manhã e Noite", "Ácido Salicílico", "", 150, 60, 85, "Sabonete de limpeza suave para peles com tendência a acne."),
    ("COSRX", "One Step Pimple Clear Pad", "Esfoliante", "Oleosa;Mista", "Acne;Poros Dilatados", "Noite", "Ácido Salicílico", "", 70, 90, 120, "Lenços esfoliantes pré-embebidos com BHA."),

    # Skin1004
    ("Skin1004", "Madagascar Centella Ampoule", "Sérum", "Sensível", "Sensibilidade/Rosácea;Textura Irregular", "Manhã e Noite", "Centella Asiática", "", 100, 85, 115, "Sérum calmante para peles sensíveis e irritadas."),
    ("Skin1004", "Madagascar Centella Toning Toner", "Tônico", "Sensível", "Sensibilidade/Rosácea;Hidratação", "Manhã e Noite", "Centella Asiática", "", 210, 70, 95, "Tônico calmante para o dia a dia."),
    ("Skin1004", "Centella Calming Mask", "Máscara Facial", "Sensível", "Sensibilidade/Rosácea", "Noite", "Centella Asiática", "", 27, 25, 35, "Máscara em tecido calmante para peles sensíveis."),

    # Payot
    ("Payot", "Doctor Payot Sérum Anti-Idade", "Sérum", "Madura", "Rugas e Linhas Finas;Firmeza", "Noite", "Colágeno", "", 30, 150, 190, "Sérum antienvelhecimento intensivo."),
    ("Payot", "Dermo Sculpt Creme", "Hidratante", "Madura", "Firmeza;Rugas e Linhas Finas", "Noite", "Peptídeos", "", 50, 170, 210, "Creme remodelador facial para peles maduras."),

    # O Boticário
    ("O Boticário", "Nativa SPA Ameixa Creme Facial", "Hidratante", "Normal;Seca", "Hidratação", "Manhã e Noite", "Óleo de Ameixa", "", 50, 45, 65, "Creme hidratante facial nutritivo."),
    ("O Boticário", "Photoshow Protetor Solar Facial", "Protetor Solar", "Todos os tipos", "Fotoenvelhecimento", "Manhã", "Filtro Solar", 50, 50, 40, 60, "Protetor solar facial com toque seco."),

    # Natura
    ("Natura", "Chronos Sérum Renovador Noturno", "Sérum", "Madura;Normal", "Rugas e Linhas Finas;Firmeza", "Noite", "Retinol", "", 30, 130, 160, "Sérum de renovação celular noturna."),
    ("Natura", "Chronos Creme Preenchedor de Rugas", "Hidratante", "Madura", "Rugas e Linhas Finas", "Manhã e Noite", "Ácido Hialurônico", "", 40, 140, 170, "Creme preenchedor antirrugas."),
    ("Natura", "Una Água Micelar", "Água Micelar", "Todos os tipos", "Hidratação", "Manhã e Noite", "Água Micelar", "", 200, 35, 50, "Água micelar de limpeza facial."),
    ("Natura", "Chronos Creme para Área dos Olhos", "Contorno de Olhos", "Madura;Normal", "Olheiras;Rugas e Linhas Finas", "Manhã e Noite", "Cafeína", "", 15, 90, 115, "Creme para redução de olheiras e linhas finas."),

    # Quem disse, Berenice?
    ("Quem disse, Berenice?", "Água Micelar QDB", "Água Micelar", "Todos os tipos", "Hidratação", "Manhã e Noite", "Água Micelar", "", 200, 30, 45, "Água micelar demaquilante de limpeza facial."),
    ("Quem disse, Berenice?", "Gel de Limpeza Facial Purificante", "Limpeza", "Oleosa;Mista", "Oleosidade;Acne", "Manhã e Noite", "Ácido Salicílico", "", 150, 35, 50, "Gel de limpeza para peles oleosas."),

    # Simple
    ("Simple", "Micellar Cleansing Water", "Água Micelar", "Sensível", "Sensibilidade/Rosácea", "Manhã e Noite", "Água Micelar", "", 200, 40, 60, "Água micelar suave para peles sensíveis."),
    ("Simple", "Hydrating Light Moisturizer", "Hidratante", "Sensível;Normal", "Hidratação;Sensibilidade/Rosácea", "Manhã e Noite", "Glicerina", "", 50, 45, 65, "Hidratante leve para peles sensíveis."),

    # Cetaphil
    ("Cetaphil", "Gentle Skin Cleanser", "Limpeza", "Sensível;Seca", "Sensibilidade/Rosácea;Hidratação", "Manhã e Noite", "Glicerina", "", 236, 55, 80, "Sabonete de limpeza suave sem sabão."),
    ("Cetaphil", "Moisturizing Cream", "Hidratante", "Seca;Sensível", "Hidratação", "Manhã e Noite", "Glicerina", "", 100, 60, 85, "Creme hidratante intensivo para peles secas e sensíveis."),
    ("Cetaphil", "Oil Control Moisturizer", "Protetor Solar", "Oleosa;Mista", "Oleosidade;Fotoenvelhecimento", "Manhã", "Filtro Solar", 30, 50, 65, 90, "Hidratante com controle de oleosidade e proteção solar."),

    # SkinCeuticals
    ("SkinCeuticals", "C E Ferulic", "Sérum", "Normal;Madura", "Manchas;Fotoenvelhecimento", "Manhã", "Vitamina C", "", 30, 550, 650, "Sérum antioxidante premium com vitamina C, E e ácido ferúlico."),
    ("SkinCeuticals", "Hydrating B5 Gel", "Sérum", "Todos os tipos", "Hidratação", "Manhã e Noite", "Ácido Hialurônico", "", 30, 320, 380, "Gel hidratante com vitamina B5."),
    ("SkinCeuticals", "Physical Fusion UV Defense", "Protetor Solar", "Todos os tipos", "Fotoenvelhecimento", "Manhã", "Filtro Solar", 50, 48, 220, 260, "Protetor solar mineral com cor."),

    # Adcos
    ("Adcos", "Prevent Sérum Antioxidante", "Sérum", "Normal;Madura", "Fotoenvelhecimento;Manchas", "Manhã", "Vitamina C", "", 30, 180, 220, "Sérum antioxidante preventivo."),
    ("Adcos", "Nude Base Hidratante com Cor", "Protetor Solar", "Todos os tipos", "Hidratação;Fotoenvelhecimento", "Manhã", "Filtro Solar", 30, 30, 90, 120, "Hidratante com cor e proteção solar."),
    ("Adcos", "Even Creme Clareador", "Hidratante", "Normal;Mista", "Manchas", "Noite", "Ácido Kójico", "", 30, 150, 190, "Creme clareador de manchas noturno."),

    # Dermage
    ("Dermage", "Sun Protect Fluid Colorless", "Protetor Solar", "Todos os tipos", "Fotoenvelhecimento", "Manhã", "Filtro Solar", 60, 50, 90, 120, "Protetor solar fluido incolor de alta proteção."),
    ("Dermage", "Vitamin C Sérum", "Sérum", "Todos os tipos", "Manchas;Fotoenvelhecimento", "Manhã", "Vitamina C", "", 30, 160, 200, "Sérum antioxidante com vitamina C estabilizada."),

    # Isdin
    ("Isdin", "Fusion Water", "Protetor Solar", "Oleosa;Mista", "Fotoenvelhecimento;Oleosidade", "Manhã", "Filtro Solar", 50, 50, 90, 120, "Protetor solar em textura água, toque seco."),
    ("Isdin", "Fotoprotector Fusion Fluid", "Protetor Solar", "Todos os tipos", "Fotoenvelhecimento", "Manhã", "Filtro Solar", 50, 50, 95, 130, "Protetor solar fluido de rápida absorção."),

    # Nuxe
    ("Nuxe", "Huile Prodigieuse", "Óleo Facial", "Seca;Normal", "Hidratação;Fotoenvelhecimento", "Noite", "Óleo Vegetal", "", 50, 150, 190, "Óleo seco multifuncional para rosto, corpo e cabelo."),
    ("Nuxe", "Creme Fraîche de Beauté", "Hidratante", "Normal;Mista", "Hidratação", "Manhã e Noite", "Manteiga de Karité", "", 50, 140, 170, "Creme hidratante 48h de textura leve."),

    # Avène
    ("Avène", "Cicalfate+ Creme Reparador", "Hidratante", "Sensível", "Sensibilidade/Rosácea", "Manhã e Noite", "Sucralfato", "", 40, 90, 120, "Creme reparador para peles irritadas ou fragilizadas."),
    ("Avène", "Hydrance Aqua-Gel", "Hidratante", "Sensível;Oleosa", "Hidratação;Sensibilidade/Rosácea", "Manhã e Noite", "Água Termal", "", 40, 95, 125, "Gel hidratante para peles sensíveis desidratadas."),
    ("Avène", "Tolerance Creme", "Hidratante", "Sensível", "Sensibilidade/Rosácea", "Manhã e Noite", "Água Termal", "", 40, 100, 130, "Creme para peles extremamente sensíveis e reativas."),

    # Mary Kay
    ("Mary Kay", "TimeWise Hidratante Diurno", "Protetor Solar", "Normal;Madura", "Fotoenvelhecimento;Rugas e Linhas Finas", "Manhã", "Filtro Solar", 30, 75, 110, 150, "Hidratante diurno antienvelhecimento com proteção solar."),
    ("Mary Kay", "TimeWise Sérum Reparador Noturno", "Sérum", "Madura", "Rugas e Linhas Finas;Firmeza", "Noite", "Retinol", "", 30, 220, 260, "Sérum de reparação noturna antienvelhecimento."),

    # Granado
    ("Granado", "Água Micelar Granado", "Água Micelar", "Todos os tipos", "Hidratação", "Manhã e Noite", "Água Micelar", "", 200, 30, 45, "Água micelar de limpeza suave."),
    ("Granado", "Sabonete Facial Glicerina", "Limpeza", "Normal;Seca", "Hidratação", "Manhã e Noite", "Glicerina", "", 90, 20, 30, "Sabonete facial hidratante em barra."),

    # Racco
    ("Racco", "Sérum Facial Ácido Hialurônico", "Sérum", "Todos os tipos", "Hidratação", "Manhã e Noite", "Ácido Hialurônico", "", 30, 60, 85, "Sérum hidratante de uso diário."),
    ("Racco", "Protetor Solar Facial", "Protetor Solar", "Todos os tipos", "Fotoenvelhecimento", "Manhã", "Filtro Solar", 50, 50, 55, 75, "Protetor solar facial de toque seco."),

    # Vult
    ("Vult", "Água Micelar", "Água Micelar", "Todos os tipos", "Hidratação", "Manhã e Noite", "Água Micelar", "", 200, 25, 40, "Água micelar de limpeza facial e remoção de maquiagem."),
    ("Vult", "Protetor Solar Facial", "Protetor Solar", "Todos os tipos", "Fotoenvelhecimento", "Manhã", "Filtro Solar", 50, 50, 35, 55, "Protetor solar facial com toque seco."),

    # L'Occitane
    ("L'Occitane en Provence", "Immortelle Creme Divine", "Hidratante", "Madura", "Rugas e Linhas Finas;Firmeza", "Manhã e Noite", "Óleo de Imortela", "", 50, 320, 380, "Creme antienvelhecimento reparador com óleo de imortela."),

    # Kiehl's
    ("Kiehl's", "Ultra Facial Cream", "Hidratante", "Normal;Mista", "Hidratação", "Manhã e Noite", "Esqualano", "", 50, 210, 250, "Creme hidratante de 24h para todos os tipos de pele."),
    ("Kiehl's", "Midnight Recovery Concentrate", "Óleo Facial", "Seca;Normal", "Hidratação;Textura Irregular", "Noite", "Óleo de Lavanda", "", 30, 260, 300, "Óleo facial regenerador noturno."),

    # Clinique
    ("Clinique", "Dramatically Different Moisturizing Lotion+", "Hidratante", "Normal;Mista", "Hidratação", "Manhã e Noite", "Ácido Hialurônico", "", 125, 180, 220, "Loção hidratante hipoalergênica de uso diário."),
    ("Clinique", "Even Better Clinical Sérum", "Sérum", "Normal;Madura", "Manchas", "Noite", "Ácido Salicílico", "", 30, 280, 330, "Sérum clareador para manchas e uniformidade do tom de pele."),

    # Estée Lauder
    ("Estée Lauder", "Advanced Night Repair", "Sérum", "Todos os tipos", "Rugas e Linhas Finas;Fotoenvelhecimento", "Noite", "Hialuronato de Sódio", "", 30, 480, 550, "Sérum reparador noturno best-seller."),

    # Shiseido
    ("Shiseido", "Ultimune Power Infusing Concentrate", "Sérum", "Todos os tipos", "Fotoenvelhecimento;Firmeza", "Manhã e Noite", "Extrato de Íris", "", 30, 380, 430, "Sérum concentrado de defesa e reparação da pele."),

    # Bio-Oil (multi-brand shelf staple)
    ("Bio-Oil", "Óleo Multifuncional", "Óleo Facial", "Seca;Normal", "Textura Irregular;Hidratação", "Noite", "Óleo Vegetal", "", 60, 55, 75, "Óleo multifuncional para cicatrizes e estrias, também usado no rosto."),
]


def slugify(text: str) -> str:
    replacements = str.maketrans("áàâãéêíóôõúüçÁÀÂÃÉÊÍÓÔÕÚÜÇ", "aaaaeeiooouucAAAAEEIOOOUUC")
    text = text.translate(replacements)
    text = text.lower().replace("'", "").replace("+", "plus")
    return "-".join("".join(c if c.isalnum() else " " for c in text).split())


def build_rows():
    rows = []
    for idx, (marca, nome, categoria, tipo_pele, preocupacao, modo_uso,
              ingrediente_principal, fps, tamanho_ml, preco_min, preco_max,
              descricao) in enumerate(PRODUCTS, start=1):
        preco = round(random.uniform(preco_min, preco_max), 2)
        avaliacao = round(random.uniform(3.6, 5.0), 1)
        num_avaliacoes = random.randint(12, 4800)
        slug = slugify(f"{marca}-{nome}")
        imagem_url = f"https://placehold.co/400x400?text={slugify(nome).replace('-', '+')}"
        rows.append({
            "id": idx,
            "marca": marca,
            "nome": nome,
            "categoria": categoria,
            "tipo_pele": tipo_pele,
            "preocupacao": preocupacao,
            "modo_uso": modo_uso,
            "ingrediente_principal": ingrediente_principal,
            "fps": fps,
            "tamanho_ml": tamanho_ml,
            "preco_brl": preco,
            "avaliacao": avaliacao,
            "num_avaliacoes": num_avaliacoes,
            "descricao": descricao,
            "imagem_url": imagem_url,
            "link_produto": "",
            "slug": slug,
        })
    return rows


def main():
    rows = build_rows()
    fieldnames = list(rows[0].keys())
    with open("produtos_skincare.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Gerado produtos_skincare.csv com {len(rows)} produtos.")


if __name__ == "__main__":
    main()
