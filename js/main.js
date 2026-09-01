/* ==========================================================================
   Hotel Pousada Aquários — main.js

   Fase 1: configuração central do site.
   Fase 3: header sticky e ativação dos pontos de contato do WhatsApp.
   ========================================================================== */
'use strict';

/**
 * Dados de contato do site.
 *
 * Número confirmado com o proprietário. Com ele preenchido, initWhatsApp()
 * ativa todos os pontos marcados com data-whatsapp e revela o botão
 * flutuante. Para tirar o WhatsApp do ar, basta esvaziar `whatsapp`.
 */
const AQUARIOS = {
  // Somente dígitos, com DDI e DDD. (31) 99520-6536
  whatsapp: '5531995206536',

  // Mensagem curta e pré-preenchida: identifica que o contato veio do site,
  // sem obrigar o hóspede a preencher formulário dentro do WhatsApp.
  whatsappMessage: 'Olá! Vim pelo site e gostaria de fazer uma reserva.',
};

/**
 * Monta o link de conversa do WhatsApp.
 * @returns {string|null} URL do wa.me, ou null se o número ainda não foi confirmado.
 */
function buildWhatsAppLink(message = AQUARIOS.whatsappMessage) {
  if (!AQUARIOS.whatsapp) return null;
  return `https://wa.me/${AQUARIOS.whatsapp}?text=${encodeURIComponent(message)}`;
}

/**
 * Ativa todos os pontos de contato marcados com [data-whatsapp].
 *
 * Sem número confirmado:
 *   - elementos com [hidden] continuam ocultos (é o caso do botão flutuante);
 *   - os demais mantêm o href de fallback escrito no HTML.
 */
function initWhatsApp() {
  const href = buildWhatsAppLink();
  if (!href) return;

  document.querySelectorAll('[data-whatsapp]').forEach((el) => {
    el.setAttribute('href', href);
    el.setAttribute('target', '_blank');
    el.setAttribute('rel', 'noopener');
    el.removeAttribute('hidden');
  });

  // Reserva no rodapé a faixa ocupada pelo botão flutuante (ver style.css)
  document.body.classList.add('aq-com-fab');
}

/**
 * Dá peso ao header depois que a página rola.
 * Usa rAF para não recalcular estilo a cada evento de scroll.
 */
function initHeader() {
  const header = document.querySelector('[data-header]');
  if (!header) return;

  let ticking = false;
  const update = () => {
    header.classList.toggle('aq-header--scrolled', window.scrollY > 8);
    ticking = false;
  };

  window.addEventListener('scroll', () => {
    if (ticking) return;
    ticking = true;
    window.requestAnimationFrame(update);
  }, { passive: true });

  update();
}

/**
 * Carrega o mapa do Google só depois do clique.
 *
 * O iframe puxa vários recursos de terceiros. Quem só quer o endereço ou o
 * botão de rota — a maioria, no celular — não paga por isso.
 */
function initMapa() {
  const caixa = document.querySelector('[data-mapa]');
  if (!caixa) return;

  const botao = caixa.querySelector('[data-mapa-abrir]');
  const src = caixa.getAttribute('data-mapa-src');
  if (!botao || !src) return;

  botao.addEventListener('click', () => {
    const iframe = document.createElement('iframe');
    iframe.src = src;
    iframe.title = 'Mapa da localização da Hotel Pousada Aquários';
    iframe.loading = 'lazy';
    iframe.referrerPolicy = 'no-referrer-when-downgrade';
    iframe.allowFullscreen = true;
    caixa.innerHTML = '';
    caixa.classList.remove('aq-empty');
    caixa.appendChild(iframe);
  }, { once: true });
}

/**
 * Preenche o ano corrente em qualquer elemento [data-ano-atual].
 */
function initAnoAtual() {
  const ano = String(new Date().getFullYear());
  document.querySelectorAll('[data-ano-atual]').forEach((el) => {
    el.textContent = ano;
  });
}

document.addEventListener('DOMContentLoaded', () => {
  initHeader();
  initWhatsApp();
  initMapa();
  initAnoAtual();
});
