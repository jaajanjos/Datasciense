<?php
/**
 * LOGIN DO PAINEL DO BLOG — comprenolink.net
 * ------------------------------------------
 * A Hostinger (LiteSpeed) remove o cabeçalho "Authorization" antes de ele chegar ao
 * WordPress, então a "senha de aplicativo" do painel nunca é vista. O painel manda o
 * mesmo login também no cabeçalho "X-WP-Auth"; este snippet o devolve ao WordPress.
 * A senha continua sendo validada pelo próprio WordPress (senha de aplicativo).
 *
 * INSTALAÇÃO: Snippets > Adicionar novo > título "Login do painel do blog" > cole
 * este arquivo (pode apagar a linha "<?php" do topo) > "Executar snippet em todo o site"
 * > Salvar e ativar.
 */

if (!defined('ABSPATH')) {
    return;
}

if (empty($_SERVER['PHP_AUTH_USER']) && !empty($_SERVER['HTTP_X_WP_AUTH'])) {
    $login = base64_decode(preg_replace('/^Basic\s+/i', '', (string) $_SERVER['HTTP_X_WP_AUTH']), true);
    if ($login !== false && strpos($login, ':') !== false) {
        list($_SERVER['PHP_AUTH_USER'], $_SERVER['PHP_AUTH_PW']) = explode(':', $login, 2);
    }
}
