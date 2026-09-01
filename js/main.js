/* ==========================================================================
   Hotel Pousada Aquários — main.js
   Fase 1: configuração central do site. Sem manipulação de DOM ainda —
   navbar, menu mobile e botão flutuante de WhatsApp entram na Fase 3.
   ========================================================================== */
'use strict';

/**
 * Dados de contato do site.
 *
 * ATENÇÃO: nada aqui foi confirmado com o proprietário (ver seção 26 do
 * roadmap). Enquanto `whatsapp` estiver vazio, nenhum link de WhatsApp
 * deve ser publicado. Não preencher com o número do Google sem confirmar.
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
 * Preenche o ano corrente em qualquer elemento [data-ano-atual].
 * Usado no rodapé a partir da Fase 3.
 */
function initAnoAtual() {
  const ano = String(new Date().getFullYear());
  document.querySelectorAll('[data-ano-atual]').forEach((el) => {
    el.textContent = ano;
  });
}

document.addEventListener('DOMContentLoaded', () => {
  initAnoAtual();
});
