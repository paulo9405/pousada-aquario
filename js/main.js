/* ==========================================================================
   Hotel Pousada Aquários — main.js

   Fase 1: configuração central do site.
   Fase 3: header sticky e ativação dos pontos de contato do WhatsApp.
   ========================================================================== */
'use strict';

/**
 * Dados de contato do site.
 *
 * ATENÇÃO: nada aqui foi confirmado com o proprietário (ver seção 26 do
 * roadmap). Enquanto `whatsapp` estiver vazio, nenhum link de WhatsApp
 * é publicado: o botão flutuante fica oculto e o botão "Reservar" leva
 * para a página de contato. Não preencher com o número do Google sem
 * confirmar antes.
 */
const AQUARIOS = {
  // Somente dígitos, com DDI e DDD. Ex.: '5538999999999'
  whatsapp: '',

  // Mensagem pré-preenchida do WhatsApp (roadmap, seção 22)
  whatsappMessage:
    'Olá! Encontrei a Hotel Pousada Aquários pelo site ' +
    'e gostaria de consultar disponibilidade.\n\n' +
    'Check-in:\n' +
    'Check-out:\n' +
    'Número de hóspedes:',
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
  initAnoAtual();
});
