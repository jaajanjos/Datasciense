// Meta Pixel (comprenolink.net) - Pixel ID 1128603339935423 - criado em 17/11/2026.
// Só carrega depois que o visitante clica em "Aceitar" (aviso simples de cookies, LGPD).
// Evento personalizado SaidaML = clique para o Mercado Livre. Não roda para quem está logado como editor.
// Para desligar: desativar este snippet. NÃO mexe no Rastreador de anúncios (snippet 5).
add_action('wp_footer', function () {
    if (is_admin() || current_user_can('edit_posts')) {
        return;
    }
    ?>
<div id="cnl-aviso" style="display:none;position:fixed;left:12px;right:12px;bottom:12px;z-index:99999;background:#1f2937;color:#fff;padding:12px 14px;border-radius:10px;font:14px/1.4 Arial,sans-serif;box-shadow:0 4px 16px rgba(0,0,0,.3);max-width:640px;margin:0 auto">
  <span>Usamos cookies e o Pixel da Meta para medir os anúncios e melhorar o blog. Você aceita?</span>
  <span style="display:block;margin-top:8px">
    <button id="cnl-sim" type="button" style="background:#16a34a;color:#fff;border:0;border-radius:6px;padding:8px 14px;margin-right:8px;cursor:pointer">Aceitar</button>
    <button id="cnl-nao" type="button" style="background:transparent;color:#fff;border:1px solid #9ca3af;border-radius:6px;padding:8px 14px;cursor:pointer">Recusar</button>
  </span>
</div>
<script>
(function () {
  var ID = '1128603339935423';
  function ler() { try { return localStorage.getItem('cnl_consent'); } catch (e) { return null; } }
  function gravar(v) { try { localStorage.setItem('cnl_consent', v); } catch (e) {} }
  var carregado = false;
  function pixel() {
    if (carregado) { return; } carregado = true;
    !function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');
    fbq('init', ID);
    fbq('track', 'PageView');
    function aoClicar(e) {
      var a = e.target && e.target.closest ? e.target.closest('a[href]') : null;
      if (!a || !/meli\.la|mercadolivre\.com|mercadolibre\.com/i.test(a.href)) { return; }
      fbq('trackCustom', 'SaidaML', { pagina: location.pathname });
    }
    document.addEventListener('click', aoClicar, true);
    document.addEventListener('auxclick', aoClicar, true);
  }
  var c = ler();
  if (c === 'sim') { pixel(); return; }
  if (c === 'nao') { return; }
  var box = document.getElementById('cnl-aviso');
  if (!box) { return; }
  box.style.display = 'block';
  document.getElementById('cnl-sim').onclick = function () { gravar('sim'); box.style.display = 'none'; pixel(); };
  document.getElementById('cnl-nao').onclick = function () { gravar('nao'); box.style.display = 'none'; };
})();
</script>
    <?php
}, 100);
