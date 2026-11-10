<?php
/**
 * RASTREADOR DE ACESSOS POR ANÚNCIO — comprenolink.net
 * -----------------------------------------------------
 * Registra, de forma anônima (LGPD), cada visita ao blog e cada clique
 * em link de afiliado (meli.la / Mercado Livre), guardando de qual
 * anúncio/rede o visitante veio (utm_*, ttclid, fbclid, gclid, app do TikTok,
 * Instagram, Facebook...), dispositivo, sistema e navegador.
 *
 * INSTALAÇÃO (grátis):
 *   1. No painel WordPress: Plugins > Adicionar novo > "Code Snippets" > Instalar > Ativar.
 *   2. Snippets > Adicionar novo > cole TODO este arquivo (pode apagar a linha "<?php" do topo).
 *   3. Troque RASTREIO_CHAVE abaixo por uma senha longa sua (a mesma vai no config do Python).
 *   4. Marque "Executar snippet em todo o site" > Salvar e ativar.
 *
 * Os dados ficam no SEU banco (tabela wp_rastreio_acessos). Nada é enviado a terceiros.
 */

if (!defined('ABSPATH')) {
    return;
}

define('RASTREIO_CHAVE', 'sOTxXVA2QDHq3jrWlfCBeaz6JK8dpn7oN0Ry1bkv59bcwfrq');
define('RASTREIO_VERSAO_DB', '1');
define('RASTREIO_DIAS_GUARDAR', 400);

function rastreio_tabela()
{
    global $wpdb;
    return $wpdb->prefix . 'rastreio_acessos';
}

/* ---------- 1. Cria a tabela na primeira execução ---------- */
add_action('init', function () {
    if (get_option('rastreio_versao_db') === RASTREIO_VERSAO_DB) {
        return;
    }
    global $wpdb;
    require_once ABSPATH . 'wp-admin/includes/upgrade.php';
    $t = rastreio_tabela();
    $c = $wpdb->get_charset_collate();
    dbDelta("CREATE TABLE $t (
        id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
        criado_em DATETIME NOT NULL,
        tipo VARCHAR(10) NOT NULL,
        visitante VARCHAR(40) NOT NULL DEFAULT '',
        sessao VARCHAR(40) NOT NULL DEFAULT '',
        pagina VARCHAR(255) NOT NULL DEFAULT '',
        origem VARCHAR(60) NOT NULL DEFAULT '',
        meio VARCHAR(60) NOT NULL DEFAULT '',
        campanha VARCHAR(100) NOT NULL DEFAULT '',
        conteudo VARCHAR(100) NOT NULL DEFAULT '',
        referencia VARCHAR(120) NOT NULL DEFAULT '',
        app VARCHAR(30) NOT NULL DEFAULT '',
        dispositivo VARCHAR(15) NOT NULL DEFAULT '',
        sistema VARCHAR(20) NOT NULL DEFAULT '',
        navegador VARCHAR(20) NOT NULL DEFAULT '',
        ip_hash VARCHAR(16) NOT NULL DEFAULT '',
        produto VARCHAR(160) NOT NULL DEFAULT '',
        link VARCHAR(255) NOT NULL DEFAULT '',
        PRIMARY KEY  (id),
        KEY criado_em (criado_em),
        KEY campanha (campanha)
    ) $c;");
    update_option('rastreio_versao_db', RASTREIO_VERSAO_DB);
});

/* ---------- 2. Identifica app / dispositivo pelo User-Agent ---------- */
function rastreio_classificar_ua($ua)
{
    $app = '';
    $apps = [
        'TikTok'    => '/musical_ly|BytedanceWebview|TikTok|trill_/i',
        'Instagram' => '/Instagram/i',
        'Facebook'  => '/FBAN|FBAV|FB_IAB|FBIOS/i',
        'Kwai'      => '/Kwai/i',
        'Pinterest' => '/Pinterest/i',
        'Telegram'  => '/Telegram/i',
        'LinkedIn'  => '/LinkedInApp/i',
        'Snapchat'  => '/Snapchat/i',
    ];
    foreach ($apps as $nome => $re) {
        if (preg_match($re, $ua)) {
            $app = $nome;
            break;
        }
    }

    if (preg_match('/iPad|Tablet|Tab\b/i', $ua)) {
        $disp = 'tablet';
    } elseif (preg_match('/Mobi|Android|iPhone|iPod/i', $ua)) {
        $disp = 'celular';
    } else {
        $disp = 'computador';
    }

    if (preg_match('/Android/i', $ua))                $so = 'Android';
    elseif (preg_match('/iPhone|iPad|iPod/i', $ua))   $so = 'iOS';
    elseif (preg_match('/Windows/i', $ua))            $so = 'Windows';
    elseif (preg_match('/Mac OS X|Macintosh/i', $ua)) $so = 'macOS';
    elseif (preg_match('/CrOS/i', $ua))               $so = 'ChromeOS';
    elseif (preg_match('/Linux/i', $ua))              $so = 'Linux';
    else                                              $so = 'Outro';

    if (preg_match('/Edg\//i', $ua))                  $nav = 'Edge';
    elseif (preg_match('/SamsungBrowser/i', $ua))     $nav = 'Samsung';
    elseif (preg_match('/OPR\/|Opera/i', $ua))        $nav = 'Opera';
    elseif (preg_match('/Firefox|FxiOS/i', $ua))      $nav = 'Firefox';
    elseif (preg_match('/Chrome|CriOS/i', $ua))       $nav = 'Chrome';
    elseif (preg_match('/Safari/i', $ua))             $nav = 'Safari';
    else                                              $nav = 'Outro';

    return ['app' => $app, 'dispositivo' => $disp, 'sistema' => $so, 'navegador' => $nav];
}

/* IP nunca é gravado: só um hash que muda todo dia (conta visitantes únicos sem identificar ninguém). */
function rastreio_ip_hash()
{
    $ip = $_SERVER['HTTP_CF_CONNECTING_IP'] ?? '';
    if ($ip === '' && !empty($_SERVER['HTTP_X_FORWARDED_FOR'])) {
        $ip = trim(explode(',', $_SERVER['HTTP_X_FORWARDED_FOR'])[0]);
    }
    if ($ip === '') {
        $ip = $_SERVER['REMOTE_ADDR'] ?? '';
    }
    return substr(hash('sha256', $ip . wp_salt('auth') . gmdate('Y-m-d')), 0, 12);
}

/* ---------- 3. API: recebe eventos e exporta dados ---------- */
add_action('rest_api_init', function () {
    register_rest_route('rastreio/v1', '/evento', [
        'methods'             => 'POST',
        'permission_callback' => '__return_true',
        'callback'            => 'rastreio_registrar',
    ]);
    register_rest_route('rastreio/v1', '/dados', [
        'methods'             => 'GET',
        'permission_callback' => function (WP_REST_Request $r) {
            $chave = (string) $r->get_header('x_rastreio_chave');
            return RASTREIO_CHAVE !== 'TROQUE-POR-UMA-SENHA-LONGA-E-SECRETA'
                && hash_equals(RASTREIO_CHAVE, $chave);
        },
        'callback'            => 'rastreio_exportar',
    ]);
});

function rastreio_registrar(WP_REST_Request $r)
{
    global $wpdb;
    $vazio = new WP_REST_Response(null, 204);

    $d = json_decode($r->get_body(), true);
    if (!is_array($d)) {
        return $vazio;
    }
    $tipo = $d['tipo'] ?? '';
    if (!in_array($tipo, ['visita', 'clique'], true)) {
        return $vazio;
    }

    $ua = substr((string) $r->get_header('user_agent'), 0, 400);
    if ($ua === '' || preg_match('/bot|crawl|spider|slurp|preview|facebookexternalhit|WhatsApp\/|Lighthouse|HeadlessChrome|PageSpeed/i', $ua)) {
        return $vazio;
    }

    // Limite anti-spam: até 200 eventos por hora por visitante (hash do IP)
    $ip_hash = rastreio_ip_hash();
    $lim_key = 'rastreio_lim_' . $ip_hash;
    $n = (int) get_transient($lim_key);
    if ($n >= 200) {
        return $vazio;
    }
    set_transient($lim_key, $n + 1, HOUR_IN_SECONDS);

    $txt = function ($k, $max) use ($d) {
        return mb_substr(sanitize_text_field((string) ($d[$k] ?? '')), 0, $max);
    };

    // Guarda só o domínio de onde veio (ex: www.google.com), ignorando o próprio site
    $referencia = '';
    if (!empty($d['referencia'])) {
        $host = (string) wp_parse_url((string) $d['referencia'], PHP_URL_HOST);
        $proprio = (string) wp_parse_url(home_url(), PHP_URL_HOST);
        if ($host !== '' && strcasecmp($host, $proprio) !== 0) {
            $referencia = mb_substr(strtolower($host), 0, 120);
        }
    }

    $info = rastreio_classificar_ua($ua);

    $wpdb->insert(rastreio_tabela(), [
        'criado_em'   => current_time('mysql'),
        'tipo'        => $tipo,
        'visitante'   => preg_replace('/[^a-z0-9]/i', '', $txt('visitante', 40)),
        'sessao'      => preg_replace('/[^a-z0-9]/i', '', $txt('sessao', 40)),
        'pagina'      => $txt('pagina', 255),
        'origem'      => strtolower($txt('origem', 60)),
        'meio'        => strtolower($txt('meio', 60)),
        'campanha'    => $txt('campanha', 100),
        'conteudo'    => $txt('conteudo', 100),
        'referencia'  => $referencia,
        'app'         => $info['app'],
        'dispositivo' => $info['dispositivo'],
        'sistema'     => $info['sistema'],
        'navegador'   => $info['navegador'],
        'ip_hash'     => $ip_hash,
        'produto'     => $tipo === 'clique' ? $txt('produto', 160) : '',
        'link'        => $tipo === 'clique' ? esc_url_raw(mb_substr((string) ($d['link'] ?? ''), 0, 255)) : '',
    ]);

    // Limpeza ocasional de registros antigos
    if (mt_rand(1, 200) === 1) {
        $wpdb->query($wpdb->prepare(
            'DELETE FROM ' . rastreio_tabela() . ' WHERE criado_em < %s',
            gmdate('Y-m-d H:i:s', time() - RASTREIO_DIAS_GUARDAR * DAY_IN_SECONDS)
        ));
    }

    return $vazio;
}

function rastreio_exportar(WP_REST_Request $r)
{
    global $wpdb;

    // Nunca deixar o cache (LiteSpeed/Hostinger) guardar esta resposta
    if (!defined('DONOTCACHEPAGE')) {
        define('DONOTCACHEPAGE', true);
    }
    do_action('litespeed_control_set_nocache', 'rastreio: exportacao privada');

    $desde = (string) $r->get_param('desde');
    if (!preg_match('/^\d{4}-\d{2}-\d{2}$/', $desde)) {
        $desde = wp_date('Y-m-d', time() - 90 * DAY_IN_SECONDS);
    }
    $linhas = $wpdb->get_results($wpdb->prepare(
        'SELECT * FROM ' . rastreio_tabela() . ' WHERE criado_em >= %s ORDER BY id ASC LIMIT 100000',
        $desde . ' 00:00:00'
    ), ARRAY_A);

    $resp = new WP_REST_Response([
        'gerado_em' => current_time('mysql'),
        'desde'     => $desde,
        'total'     => count($linhas),
        'eventos'   => $linhas,
    ]);
    $resp->header('Cache-Control', 'no-store, private, max-age=0');
    return $resp;
}

/* ---------- 4. Script no rodapé do blog (não roda para você logado como admin/editor) ---------- */
add_action('wp_footer', function () {
    if (is_admin() || current_user_can('edit_posts')) {
        return;
    }
    $api = esc_url_raw(rest_url('rastreio/v1/evento'));
    ?>
<script>
(function () {
  var API = <?php echo wp_json_encode($api); ?>;
  function ler(s, k) { try { return window[s].getItem(k); } catch (e) { return null; } }
  function gravar(s, k, v) { try { window[s].setItem(k, v); } catch (e) {} }
  function novoId() { return Date.now().toString(36) + Math.random().toString(36).slice(2, 10); }

  var visitante = ler('localStorage', 'rastreio_vid');
  if (!visitante) { visitante = novoId(); gravar('localStorage', 'rastreio_vid', visitante); }
  var sessao = ler('sessionStorage', 'rastreio_sid');
  if (!sessao) { sessao = novoId(); gravar('sessionStorage', 'rastreio_sid', sessao); }

  var p = new URLSearchParams(location.search);
  var utm = {
    origem: p.get('utm_source') || '', meio: p.get('utm_medium') || '',
    campanha: p.get('utm_campaign') || '', conteudo: p.get('utm_content') || ''
  };
  // Sem UTM? Usa os identificadores de clique que as plataformas de anúncio colocam na URL
  if (!utm.origem) {
    if (p.get('ttclid'))      { utm.origem = 'tiktok';   utm.meio = 'cpc'; }
    else if (p.get('fbclid')) { utm.origem = 'facebook'; utm.meio = utm.meio || 'social'; }
    else if (p.get('gclid'))  { utm.origem = 'google';   utm.meio = 'cpc'; }
  }
  // Mantém a origem durante toda a visita (para os cliques em outras páginas)
  if (utm.origem) { gravar('sessionStorage', 'rastreio_utm', JSON.stringify(utm)); }
  else { try { utm = JSON.parse(ler('sessionStorage', 'rastreio_utm')) || utm; } catch (e) {} }

  function enviar(dados) {
    dados.visitante = visitante; dados.sessao = sessao; dados.pagina = location.pathname;
    for (var k in utm) { dados[k] = utm[k]; }
    var corpo = JSON.stringify(dados);
    if (navigator.sendBeacon && navigator.sendBeacon(API, corpo)) { return; }
    try { fetch(API, { method: 'POST', body: corpo, keepalive: true }); } catch (e) {}
  }

  function produtoDoLink(a) {
    var el = a;
    while (el && el !== document.body) {
      var irmao = el.previousElementSibling;
      while (irmao) {
        if (/^H[23]$/.test(irmao.tagName)) { return irmao.textContent.trim().slice(0, 150); }
        var t = irmao.querySelectorAll ? irmao.querySelectorAll('h2,h3') : [];
        if (t.length) { return t[t.length - 1].textContent.trim().slice(0, 150); }
        irmao = irmao.previousElementSibling;
      }
      el = el.parentElement;
    }
    return (a.textContent || '').trim().slice(0, 150);
  }

  enviar({ tipo: 'visita', referencia: document.referrer });

  function aoClicar(e) {
    var a = e.target && e.target.closest ? e.target.closest('a[href]') : null;
    if (!a || !/meli\.la|mercadolivre\.com|mercadolibre\.com/i.test(a.href)) { return; }
    enviar({ tipo: 'clique', link: a.href, produto: produtoDoLink(a) });
  }
  document.addEventListener('click', aoClicar, true);
  document.addEventListener('auxclick', aoClicar, true);
})();
</script>
    <?php
}, 99);
