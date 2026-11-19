# Linha de base das melhorias do blog (M0) — 18/11/2026

Coleta só de leitura (nada foi alterado no blog nem na conta Meta). Plano: Planejamento_de_melhorias_blog_em_relação_concorrentes.pdf.

## 1. Saída por página (acessos_20261118_1115.csv, 19/10 a 18/11, sem campanhas teste_rastreio)

Saída = cliques de saída ÷ visitas. Total: 1.294 visitas e 90 cliques (6,9%).

| Página | Visitas | Cliques | Saída | Linha de base 17/11 |
|---|---:|---:|---:|---|
| /melhores-produtos-mercado-livre-2026/ (guia) | 478 | 70 | 14,6% | 478 / 70 = 14,6% (igual) |
| /tecnologia-e-informatica/ | 286 | 3 | 1,0% | 286 / 3 = 1,0% (igual) |
| / (início) | 265 | 0 | 0,0% | 269 / 0 (−4 visitas) |
| /black-friday/ | 49 | 0 | 0,0% | — |
| /5-2/ | 33 | 5 | 15,2% | — |
| /contato/ | 29 | 0 | 0,0% | — |
| /sobre/ | 25 | 0 | 0,0% | — |
| /ferramentas-e-utilidades/ | 25 | 3 | 12,0% | 25 / 3 (igual) |
| /casa-e-eletrodomesticos/ | 18 | 7 | 38,9% | 17 / 6 (+1 visita, +1 clique) |
| /audio-e-tv/ | 16 | 0 | 0,0% | 16 / 0 (igual) |
| /casa-cama-e-decoracao/ | 16 | 1 | 6,2% | — |
| /esporte-e-fitness/ | 15 | 0 | 0,0% | — |
| /beleza-e-saude/ | 14 | 0 | 0,0% | — |
| /politica-de-privacidade/ | 14 | 0 | 0,0% | — |
| /presentes-de-natal/ | 5 | 0 | 0,0% | — |
| /bebe-e-maternidade/ | 4 | 1 | 25,0% | — |
| /moda-infantil-e-juvenil/ | 2 | 0 | 0,0% | — |

Observação: o último registro do CSV é de 18/11 01:05, então os números praticamente repetem a linha de base de 17/11 (as diferenças do início e de casa-e-eletrodomesticos podem ser da faixa de corte/arquivos de teste excluídos).

## 2. Saída por origem

| Origem / meio | Visitas | Cliques | Saída |
|---|---:|---:|---:|
| direto | 700 | 32 | 4,6% |
| site / home (navegação interna) | 279 | 53 | 19,0% |
| instagram / paid (anúncio) | 260 | 2 | 0,8% |
| whatsapp (canal 19, perfil 3, sem meio 4) | 26 | 3 | 11,5% |
| facebook / social | 12 | 0 | 0,0% |
| w | 8 | 0 | 0,0% |
| instagram / stories | 5 | 0 | 0,0% |
| instagram / dm | 2 | 0 | 0,0% |
| tiktok / video | 1 | 0 | 0,0% |
| ig / social | 1 | 0 | 0,0% |

Leitura: o tráfego do anúncio (instagram/paid) é 260 visitas com apenas 2 cliques de saída (0,8%); quem navega por dentro do site (site/home) sai 19,0%.

## 3. PageSpeed (celular) — pagespeed.web.dev, 18/11/2026 ~20h21 a 20h30

A API do Google (curl) devolveu erro 429 (cota diária esgotada para as 5 páginas). Usei a página pública pagespeed.web.dev pelo Chrome (aba fechada ao final). Notas de desempenho do laboratório (Lighthouse, celular).

| Página | Nota | LCP | CLS | TBT | Peso total |
|---|---:|---:|---:|---:|---:|
| / (início) | 95 | 1,7 s | 0 | 70 ms | 449 KiB |
| /melhores-produtos-mercado-livre-2026/ | 99 | 0,6 s | 0,048 | 30 ms | 725 KiB |
| /tecnologia-e-informatica/ | 98 | 1,7 s | 0 | 10 ms | 998 KiB |
| /audio-e-tv/ | 95 | 1,7 s | 0 | 70 ms | 1.134 KiB |
| /casa-e-eletrodomesticos/ | 95 | 1,7 s | 0 | 30 ms | 905 KiB |

Outros dados lidos: Speed Index 4,8 s (início), 0,7 s (guia), 3,7 s (tecnologia), 5,2 s (áudio e TV), 5,0 s (casa). Dados de usuários reais: "Sem dados" (tráfego baixo).

## Conclusão de desempenho

- Velocidade não é o gargalo: todas as páginas têm nota 95 a 99 no celular, LCP até 1,7 s e CLS próximo de 0.
- O gargalo é a saída: tecnologia (286 visitas, 1,0%), início (265 visitas, 0 cliques) e o tráfego do anúncio (0,8%) quase não chegam ao Mercado Livre; o guia (14,6%) e casa-e-eletrodomesticos (38,9%, poucas visitas) saem bem.
- Pontos de atenção: (1) categorias de áudio e TV, casa e tecnologia pesam 900 a 1.134 KiB (imagens), com Speed Index de 3,7 a 5,2 s, ainda aceitável; (2) amostras pequenas (16 a 25 visitas) pedem cautela; (3) o CSV é de 18/11 11:15, então é uma foto do mesmo dia da linha de base; refazer a medição depois de cada melhoria.

Nenhuma alteração foi feita no blog nem na conta de anúncios Meta.
