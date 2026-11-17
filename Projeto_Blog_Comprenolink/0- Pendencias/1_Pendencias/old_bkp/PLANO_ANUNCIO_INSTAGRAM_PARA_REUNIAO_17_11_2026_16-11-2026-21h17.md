# Plano do anúncio Instagram — para a reunião de 17/11/2026, 15:00

Status: **só proposta**. Nada foi instalado no blog, nada foi alterado na conta de anúncios, nada foi publicado. Cada item abaixo precisa de "de acordo" do dono.

## 0. Pontos que mudam a conversa (ler primeiro)

1. **Data de término.** O conjunto `teste_11a13_11_conjunto` termina em **16/11**, não em 30/11. Para "ir até 30/11" é preciso prorrogar e, provavelmente, aumentar a verba (a verba vitalícia é R$ 50, já quase toda gasta). Isso é decisão do dono e tem custo.
2. **A meta de 50 compras não cabe em R$ 50.** Com R$ 0,27 por visualização da página, R$ 50 compram cerca de 185 visualizações. Veja a conta na seção 3.
3. **A Meta não enxerga a compra.** O Pixel do Meta não roda no Mercado Livre. O que dá para medir é até o **clique de saída** no blog. A compra só aparece depois, no relatório do ML Afiliados (com atraso de dias).
4. **Os números diferem um pouco.** Na leitura de 16/11 às 10h eu tinha CTR de links 8,27% e CPC R$ 0,19 (período do conjunto inteiro). Os números do prompt (CTR 7,46%, CPC R$ 0,21, R$ 0,27 por visualização) vêm de outro recorte. Confirmar o período antes de decidir.
5. **Política do blog e das artes:** sem preço na arte ou na legenda, sem "mais vendido", sem "melhor...", sem "garantido". Por isso os ganchos abaixo **não citam os R$ 147**.
6. **Regras do ML Afiliados para anúncio pago** (uso de cupons, canais, tráfego pago para link de afiliado) precisam ser conferidas antes de gastar mais. Isso já estava na lista de pendências de SEO/anúncio.

---

## 1. Rastreamento de cliques de saída no blog

Ideia: o blog é nosso, então **o Pixel do Meta e o GA4 podem rodar no blog**. Só o Mercado Livre não aceita. Ao clicar no botão de afiliado, o blog dispara um evento (`clique_saida_ml`) antes de abrir o Mercado Livre.

Pré-requisitos a verificar (eu não alterei nada):
- GA4 do blog (ligação com o Search Console e evento principal já feitos em 13/11): confirmar o ID `G-XXXXXXXXXX`.
- Pixel do Meta no blog: confirmar se já está instalado. Se não estiver, instalar o Pixel (ou usar só GA4).
- Onde colar: tema Futurio > código no `<head>`/rodapé (ou plugin de código no WordPress). Fazer cópia (backup) antes.

```html
<script>
(function () {
  // Domínios de saída para o Mercado Livre (links de afiliado meli.la e páginas do ML)
  var DOMINIOS = ['meli.la', 'mercadolivre.com.br', 'mercadolibre.com'];

  function ehSaidaML(a) {
    if (!a || !a.href) return false;
    try {
      var host = new URL(a.href, location.href).hostname;
      return DOMINIOS.some(function (d) { return host === d || host.endsWith('.' + d); });
    } catch (e) { return false; }
  }

  function enviar(a) {
    var dados = {
      destino: (a.href || '').split('?')[0],
      texto: (a.textContent || '').trim().slice(0, 80),
      pagina: location.pathname,
      item: (a.closest('[id^="item-"]') || {}).id || ''
    };
    // GA4
    if (typeof gtag === 'function') {
      gtag('event', 'clique_saida_ml', dados);
    } else if (window.dataLayer) {
      window.dataLayer.push(Object.assign({ event: 'clique_saida_ml' }, dados));
    }
    // Pixel do Meta (só funciona se o Pixel estiver instalado no BLOG)
    if (typeof fbq === 'function') {
      fbq('trackCustom', 'CliqueSaidaML', dados);
    }
  }

  document.addEventListener('click', function (e) {
    var a = e.target.closest ? e.target.closest('a') : null;
    if (ehSaidaML(a)) enviar(a);
  }, true);

  // Também em clique com o botão do meio (abrir em nova aba)
  document.addEventListener('auxclick', function (e) {
    if (e.button !== 1) return;
    var a = e.target.closest ? e.target.closest('a') : null;
    if (ehSaidaML(a)) enviar(a);
  }, true);
})();
</script>
```

Depois de instalar (só com "de acordo"):
- Marcar `clique_saida_ml` como **evento principal** no GA4.
- Testar com o DebugView do GA4 e o "Test Events" do Gerenciador de Eventos da Meta.
- Se o Pixel estiver no blog, criar uma **Conversão personalizada** `CliqueSaidaML` e (só mais tarde, com volume) trocar o objetivo do anúncio para ela.

Limite: o clique de saída mede **intenção**, não compra. Ele não prova que a venda aconteceu.

---

## 2. Dois ganchos novos de 3 segundos (teste A/B)

O produto anunciado é o de R$ 147, mas **o preço não aparece**. Onde está `[PRODUTO]`, usar o nome do guia; só usar características que estejam no guia ou no anúncio do Mercado Livre.

**Opção A — pergunta direta (vídeo ou imagem)**
- Texto na tela (0 a 3 s): **"Você já viu este [PRODUTO]?"**
- Fala/legenda curta: "Achei no Mercado Livre. Olha os detalhes antes de decidir."
- Chamada final: "Toque para ver os detalhes no blog."
- Variação de imagem estática: título forte "Já viu este [PRODUTO]?" + foto real do produto + "Veja os detalhes".

**Opção B — "3 coisas para olhar antes"**
- Texto na tela (0 a 3 s): **"3 coisas para olhar antes de comprar [PRODUTO]"**
- Cena 2: três características reais, uma por vez (só as confirmadas).
- Chamada final: "Veja os detalhes no Mercado Livre pelo blog."
- Variação de imagem estática: título "3 coisas para ver antes" + lista curta.

Como testar: mesma verba, mesmo público, **só o gancho muda**. Não editar o anúncio que está rodando (reinicia o aprendizado): criar um anúncio novo dentro do mesmo conjunto, ou duplicar. Cada criativo precisa de pelo menos cerca de 1.000 impressões antes de comparar. Incluir "link de afiliado" na legenda, como já fazemos.

---

## 3. Funil até as 50 compras — a conta

Etapas, com o que cada uma mede:

| Etapa | Onde medir | Dado |
|---|---|---|
| Impressão → clique no link | Meta | CTR (hoje 7,46%) |
| Clique → visualização da página | Meta | custo por visualização (hoje R$ 0,27) |
| Visualização → **clique de saída** | GA4 / Pixel no blog | **taxa de saída (nova)** |
| Clique de saída → compra | Relatório do ML Afiliados | taxa de compra (atraso de dias) |

Quantas visualizações de página para 50 compras (cenários de **exemplo**, não são dados medidos):

| Taxa de saída | Compra no ML | Visualizações necessárias | Custo a R$ 0,27 |
|---|---|---|---|
| 40% | 3% | cerca de 4.200 | cerca de R$ 1.125 |
| 30% | 2% | cerca de 8.300 | cerca de R$ 2.250 |
| 20% | 1% | cerca de 25.000 | cerca de R$ 6.750 |

Leitura direta: **com R$ 50 a meta de 50 compras não é alcançável**. O que R$ 50 pode entregar é **medir a taxa de saída**. Isso responde a pergunta do gargalo.

Custo por compra estimado = R$ 0,27 ÷ (taxa de saída × taxa de compra). No cenário 30% e 2%: cerca de R$ 45 por compra. **Só compensa se a comissão por venda do produto for maior que isso.** Preciso da comissão real do item no ML Afiliados (varia por categoria) para fechar a conta.

Passo a passo proposto (sem gastar mais por enquanto):
1. **Dia 1:** instalar o rastreamento (seção 1), testar, marcar o evento no GA4.
2. **Dias 1 a 3:** com o tráfego que ainda chega, medir a **taxa de saída** (cliques de saída ÷ visualizações). Regra de leitura: abaixo de 15%, o problema é a página do blog; acima de 30%, o público é bom.
3. **Dias 3 a 5:** se a taxa de saída for boa, criar o novo gancho (A ou B) com a mesma verba pequena e comparar.
4. **Dia 7:** cruzar com vendas do ML Afiliados (relatório já lido semanalmente) para estimar a taxa de compra.
5. **Decisão (reunião):** só então definir se vale gastar mais. Meta de partida já discutida: 150 visitas reais com até R$ 0,35 por visita.

Ajuste sem gastar mais: melhorar a página do blog (botão de afiliado mais visível no topo do item, descrição curta, só dados confirmados) costuma subir a taxa de saída sem custo de mídia.

---

## 4. Checklist técnico no Gerenciador de Anúncios (alertas preventivos)

Marcar uma vez por dia, só olhar (não alterar):
- [ ] **Data de término** do conjunto: está em 16/11. Prorrogar só com "de acordo".
- [ ] **Limite de gastos da conta**: a Meta mostrou "limite de gastos da conta quase atingido". Conferir o valor do limite e quanto falta.
- [ ] **Verba vitalícia** (R$ 50): quanto sobra; o anúncio para quando acaba.
- [ ] **Forma de pagamento**: ativa e sem recusa.
- [ ] **Status**: "Ativo" e sem aviso de reprovação ou "limitado".
- [ ] **Fase de aprendizado**: evitar editar anúncio, público ou criativo no meio. Mudança de verba maior que cerca de 20% reinicia o aprendizado.
- [ ] **Frequência**: acima de 2,5 indica fadiga do criativo (hoje 1,02, tranquilo).
- [ ] **Atribuição**: "clique em 7 dias ou visualização em 1 dia" pode superestimar visitas reais; sempre cruzar com o Analytics.
- [ ] **UTMs** nos links do anúncio, para o GA4 separar o que veio do Instagram pago.
- [ ] **Regras do ML Afiliados** sobre tráfego pago: conferir antes de aumentar a verba.

---

## 5. O que levar para decidir amanhã (15:00)

1. Quanto o dono aceita gastar para **medir a taxa de saída** (sugestão: manter R$ 50 ou até R$ 100, sem subir limite da conta ainda).
2. Prorrogar o anúncio até 30/11? Isso exige verba e talvez subir o limite de gastos da conta.
3. Autorizar instalar o rastreamento no blog (com backup do tema antes).
4. Informar a **comissão por venda** do item de R$ 147 (ML Afiliados) para fechar o custo por compra.
5. Qual dos dois ganchos (A ou B) produzir primeiro, e qual produto entra.
6. Confirmar a leitura das regras do ML sobre anúncio pago.
