<?php
/**
 * SEM PREÇO NOS CARTÕES - comprenolink.net (instalado em 22/10/2026, Code Snippets id 8)
 * Tira o preço de cada produto (cartões do plugin Hostinger Affiliate, que buscam o preço
 * ao vivo, e cartões criados pelo painel). O lugar do preço fica vazio; o botão continua.
 *
 * INSTALAÇÃO (se precisar refazer): Snippets > Adicionar novo > título "Sem preço nos cartões" >
 * cole este arquivo (pode apagar a linha "<?php" do topo) > "Executar em todo o site" >
 * Salvar e ativar. Depois limpe o cache (LiteSpeed Cache > Limpar tudo).
 * Para voltar a mostrar o preço: desative este snippet e limpe o cache.
 */

if (!defined('ABSPATH')) {
    return;
}

add_filter('the_content', function ($html) {
    if (strpos($html, 'product-price') === false) {
        return $html;
    }
    return preg_replace(
        '~<div class="hostinger-affiliate-block-single-type__product-price">.*?</div>\s*(?=<div class="hostinger-affiliate-block-single-type__product-button-wrap">)~s',
        '',
        $html
    );
}, 99);
