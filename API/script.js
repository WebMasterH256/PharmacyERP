// ==================== CONFIGURAÇÃO DE API ====================

const API_URL = 'http://localhost:5500'; // URL da API FastAPI

// ==================== INICIALIZAÇÃO ====================

document.addEventListener('DOMContentLoaded', function() {
  initChart();
  setupEventListeners();
  setupMobileMenu();
  addAnimations();
  loadDashboardData(); // Carrega dados da API
});

// ==================== GRÁFICO ====================

let salesChart;

function initChart() {
  const ctx = document.getElementById('salesChart');
  
  if (!ctx) return;

  const chartData = {
    labels: ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom'],
    datasets: [
      {
        label: 'Vendas (R$)',
        data: [2100, 2400, 2800, 2200, 3100, 2500, 2450],
        borderColor: '#2563EB',
        backgroundColor: 'rgba(37, 99, 235, 0.05)',
        borderWidth: 3,
        fill: true,
        tension: 0.4,
        pointRadius: 6,
        pointBackgroundColor: '#2563EB',
        pointBorderColor: '#FFFFFF',
        pointBorderWidth: 2,
        pointHoverRadius: 8,
        pointHoverBackgroundColor: '#3B82F6',
        borderCapStyle: 'round',
        borderJoinStyle: 'round',
      }
    ]
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: true,
        position: 'top',
        labels: {
          padding: 20,
          font: {
            size: 13,
            weight: '600',
            family: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto'
          },
          color: '#111827',
          usePointStyle: true,
          pointStyle: 'circle'
        }
      },
      tooltip: {
        enabled: true,
        backgroundColor: 'rgba(17, 24, 39, 0.8)',
        padding: 12,
        titleFont: {
          size: 13,
          weight: '600'
        },
        bodyFont: {
          size: 12
        },
        borderColor: '#E5E7EB',
        borderWidth: 1,
        displayColors: true,
        callbacks: {
          label: function(context) {
            return 'Vendas: R$ ' + formatCurrency(context.raw);
          }
        }
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        max: 3500,
        ticks: {
          font: {
            size: 12,
            family: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto'
          },
          color: '#6B7280',
          callback: function(value) {
            return 'R$ ' + formatCurrency(value);
          },
          padding: 12
        },
        grid: {
          color: 'rgba(229, 231, 235, 0.5)',
          drawBorder: false,
          lineWidth: 1
        }
      },
      x: {
        ticks: {
          font: {
            size: 12,
            weight: '500',
            family: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto'
          },
          color: '#6B7280',
          padding: 8
        },
        grid: {
          display: false,
          drawBorder: false
        }
      }
    }
  };

  salesChart = new Chart(ctx, {
    type: 'line',
    data: chartData,
    options: chartOptions
  });
}

// ==================== UTILITÁRIOS ====================

function formatCurrency(value) {
  return new Intl.NumberFormat('pt-BR', {
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  }).format(value);
}

// ==================== EVENT LISTENERS ====================

function setupEventListeners() {
  // Navegação Sidebar
  const navItems = document.querySelectorAll('.nav-item');
  navItems.forEach(item => {
    item.addEventListener('click', function(e) {
      e.preventDefault();
      
      // Remove active de todos
      navItems.forEach(nav => nav.classList.remove('active'));
      
      // Adiciona ao clicado
      this.classList.add('active');

      // Fechar menu mobile se aberto
      const sidebar = document.querySelector('.sidebar');
      if (sidebar.classList.contains('active')) {
        sidebar.classList.remove('active');
      }

      // Efeito visual
      showPageTransition();
    });
  });

  // Botões de fechar alertas
  const closeButtons = document.querySelectorAll('.btn-close');
  closeButtons.forEach(btn => {
    btn.addEventListener('click', function() {
      const alertCard = this.closest('.alert-card');
      if (alertCard) {
        alertCard.style.animation = 'slideOut 0.3s ease forwards';
        setTimeout(() => {
          alertCard.remove();
        }, 300);
      }
    });
  });

  // Botão Nova Venda
  const btnNovavenda = document.querySelector('.btn-primary.btn-full');
  if (btnNovavenda) {
    btnNovavenda.addEventListener('click', function() {
      showNotification('Nova venda iniciada!', 'success');
    });
  }

  // Ícone de notificação
  const notificationBtn = document.querySelector('.icon-btn');
  if (notificationBtn) {
    notificationBtn.addEventListener('click', function() {
      showNotification('Você tem 3 notificações!', 'info');
    });
  }
}

// ==================== MENU MOBILE ====================

function setupMobileMenu() {
  const menuToggle = document.getElementById('menuToggle');
  const sidebar = document.querySelector('.sidebar');

  if (menuToggle) {
    menuToggle.addEventListener('click', function() {
      sidebar.classList.toggle('active');
    });
  }

  // Fechar sidebar ao clicar fora
  document.addEventListener('click', function(e) {
    const sidebar = document.querySelector('.sidebar');
    const menuToggle = document.getElementById('menuToggle');

    if (window.innerWidth <= 768 && sidebar.classList.contains('active')) {
      if (!sidebar.contains(e.target) && !menuToggle.contains(e.target)) {
        sidebar.classList.remove('active');
      }
    }
  });

  // Fechar sidebar ao redimensionar
  window.addEventListener('resize', function() {
    const sidebar = document.querySelector('.sidebar');
    if (window.innerWidth > 768) {
      sidebar.classList.remove('active');
    }
  });
}

// ==================== ANIMAÇÕES ====================

function addAnimations() {
  // Adiciona animações aos KPI cards
  const kpiCards = document.querySelectorAll('.kpi-card');
  kpiCards.forEach((card, index) => {
    card.style.animation = `fadeInUp 0.5s ease ${index * 0.1}s both`;
  });

  // Adiciona animações aos alert cards
  const alertCards = document.querySelectorAll('.alert-card');
  alertCards.forEach((card, index) => {
    card.style.animation = `slideInRight 0.5s ease ${0.5 + index * 0.1}s both`;
  });

  // Adiciona animações às linhas da tabela
  const tableRows = document.querySelectorAll('.sales-table tbody tr');
  tableRows.forEach((row, index) => {
    row.style.animation = `fadeInUp 0.5s ease ${0.8 + index * 0.1}s both`;
  });

  // Adiciona estilos de animação ao document
  addAnimationStyles();
}

function addAnimationStyles() {
  const style = document.createElement('style');
  style.textContent = `
    @keyframes fadeInUp {
      from {
        opacity: 0;
        transform: translateY(20px);
      }
      to {
        opacity: 1;
        transform: translateY(0);
      }
    }

    @keyframes slideInRight {
      from {
        opacity: 0;
        transform: translateX(20px);
      }
      to {
        opacity: 1;
        transform: translateX(0);
      }
    }

    @keyframes slideOut {
      from {
        opacity: 1;
        transform: translateX(0);
      }
      to {
        opacity: 0;
        transform: translateX(20px);
      }
    }

    @keyframes pulse {
      0%, 100% {
        opacity: 1;
      }
      50% {
        opacity: 0.5;
      }
    }

    @keyframes spin {
      from {
        transform: rotate(0deg);
      }
      to {
        transform: rotate(360deg);
      }
    }
  `;
  document.head.appendChild(style);
}

// ==================== NOTIFICAÇÕES ====================

function showNotification(message, type = 'info') {
  const notification = document.createElement('div');
  notification.className = `notification notification-${type}`;
  notification.innerHTML = `
    <i class="fas fa-${getNotificationIcon(type)}"></i>
    <span>${message}</span>
  `;

  // Estilos da notificação
  const notificationStyle = document.createElement('style');
  notificationStyle.textContent = `
    .notification {
      position: fixed;
      top: 20px;
      right: 20px;
      padding: 16px 24px;
      border-radius: 12px;
      font-weight: 600;
      font-size: 14px;
      display: flex;
      align-items: center;
      gap: 12px;
      z-index: 2000;
      animation: slideInRight 0.3s ease;
      box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
    }

    .notification-success {
      background: linear-gradient(135deg, #22C55E 0%, #16A34A 100%);
      color: white;
    }

    .notification-error {
      background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%);
      color: white;
    }

    .notification-info {
      background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
      color: white;
    }

    .notification i {
      font-size: 16px;
    }

    @media (max-width: 768px) {
      .notification {
        top: 10px;
        right: 10px;
        left: 10px;
        justify-content: center;
      }
    }
  `;

  if (!document.querySelector('style[data-notification-styles]')) {
    notificationStyle.setAttribute('data-notification-styles', 'true');
    document.head.appendChild(notificationStyle);
  }

  document.body.appendChild(notification);

  // Remove após 3 segundos
  setTimeout(() => {
    notification.style.animation = 'slideOut 0.3s ease forwards';
    setTimeout(() => {
      notification.remove();
    }, 300);
  }, 3000);
}

function getNotificationIcon(type) {
  const icons = {
    success: 'check-circle',
    error: 'exclamation-circle',
    info: 'info-circle'
  };
  return icons[type] || 'info-circle';
}

// ==================== TRANSIÇÕES DE PÁGINA ====================

function showPageTransition() {
  const pageContent = document.getElementById('pageContent');
  
  pageContent.style.opacity = '0.7';
  pageContent.style.transition = 'opacity 0.2s ease';

  setTimeout(() => {
    pageContent.style.opacity = '1';
  }, 200);
}

// ==================== EFEITOS HOVER ====================

document.addEventListener('DOMContentLoaded', function() {
  const cards = document.querySelectorAll('.kpi-card, .card, .alert-card');
  
  cards.forEach(card => {
    card.addEventListener('mouseenter', function() {
      this.style.transition = 'all 0.3s ease';
    });
  });
});

// ==================== ATUALIZAÇÃO DE DADOS ====================

// Carrega dados do dashboard da API
async function loadDashboardData() {
  try {
    showNotification('Carregando dados...', 'info');
    
    // Faz requisição para o endpoint de dashboard
    const response = await fetch(`${API_URL}/relatorios/dashboard`);
    
    if (!response.ok) {
      throw new Error(`Erro na API: ${response.status}`);
    }
    
    const data = await response.json();
    
    // Atualiza os KPI cards com dados da API
    updateKPIWithData(data);
    
    showNotification('Dados carregados com sucesso!', 'success');
  } catch (error) {
    console.error('Erro ao carregar dashboard:', error);
    showNotification('Erro ao conectar com a API', 'error');
  }
}

// Atualiza KPI cards com dados da API
function updateKPIWithData(data) {
  if (!data.resumo) return;
  
  const kpiValues = [
    {
      selector: '.kpi-primary .kpi-value',
      value: 'R$ ' + formatCurrency(data.financeiro_mes?.receita_bruta || 0),
      change: '+12% vs. mês passado'
    },
    {
      selector: '.kpi-success .kpi-value',
      value: 'R$ ' + formatCurrency(data.financeiro_mes?.lucro_bruto || 0),
      change: (data.financeiro_mes?.lucro_bruto / data.financeiro_mes?.receita_bruta * 100).toFixed(0) + '% de margem'
    },
    {
      selector: '.kpi-warning .kpi-value',
      value: data.resumo.total_medicamentos_ativos || 0,
      change: 'Medicamentos ativos'
    },
    {
      selector: '.kpi-danger .kpi-value',
      value: data.resumo.alertas_pendentes || 0,
      change: 'Alertas pendentes'
    }
  ];

  kpiValues.forEach(item => {
    const element = document.querySelector(item.selector);
    if (element) {
      element.textContent = item.value;
    }
    
    const changeElement = element?.parentElement?.querySelector('.kpi-change');
    if (changeElement) {
      changeElement.textContent = item.change;
    }
  });
}

// Carrega lista de medicamentos
async function loadMedicamentos() {
  try {
    const response = await fetch(`${API_URL}/medicamentos`);
    const data = await response.json();
    console.log('Medicamentos carregados:', data);
    return data;
  } catch (error) {
    console.error('Erro ao carregar medicamentos:', error);
    return [];
  }
}

// Carrega lista de lotes
async function loadLotes() {
  try {
    const response = await fetch(`${API_URL}/lotes`);
    const data = await response.json();
    console.log('Lotes carregados:', data);
    return data;
  } catch (error) {
    console.error('Erro ao carregar lotes:', error);
    return [];
  }
}

// Carrega lista de alertas
async function loadAlertas() {
  try {
    const response = await fetch(`${API_URL}/alertas`);
    const data = await response.json();
    console.log('Alertas carregados:', data);
    return data;
  } catch (error) {
    console.error('Erro ao carregar alertas:', error);
    return [];
  }
}

function updateKPIValues() {
  const values = [
    {
      selector: '.kpi-primary .kpi-value',
      value: 'R$ ' + formatCurrency(Math.random() * 5000),
      change: '+' + Math.floor(Math.random() * 20) + '%'
    },
    {
      selector: '.kpi-success .kpi-value',
      value: 'R$ ' + formatCurrency(Math.random() * 2000),
      change: Math.floor(Math.random() * 50) + '% de margem'
    },
    {
      selector: '.kpi-warning .kpi-value',
      value: Math.floor(Math.random() * 200),
      change: Math.floor(Math.random() * 20) + ' produtos ativos'
    },
    {
      selector: '.kpi-danger .kpi-value',
      value: Math.floor(Math.random() * 10),
      change: 'Alertas ativos'
    }
  ];

  values.forEach(item => {
    const element = document.querySelector(item.selector);
    if (element) {
      element.style.animation = 'pulse 0.3s ease';
      setTimeout(() => {
        element.textContent = item.value;
        element.style.animation = 'none';
      }, 150);
    }
  });
}

// ==================== INICIALIZAÇÃO DE DADOS ====================

// Simula atualização de dados a cada 30 segundos
setInterval(() => {
  // Você pode chamar updateKPIValues() aqui para simular dados reais
  // updateKPIValues();
}, 30000);

// ==================== FUNÇÕES AUXILIARES ====================

// Detecta tema escuro/claro do sistema
function detectTheme() {
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  return prefersDark ? 'dark' : 'light';
}

// Função para simular loading
function showLoading(element) {
  const loadingHTML = `
    <div style="display: flex; align-items: center; justify-content: center; padding: 40px;">
      <i class="fas fa-spinner" style="font-size: 32px; animation: spin 1s linear infinite; color: #2563EB;"></i>
    </div>
  `;
  element.innerHTML = loadingHTML;
}

// Função para formatar data
function formatDate(date) {
  return new Intl.DateTimeFormat('pt-BR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }).format(date);
}

// ==================== ACCESSIBILITY ====================

// Melhora acessibilidade com teclado
document.addEventListener('keydown', function(e) {
  // ESC para fechar menu mobile
  if (e.key === 'Escape') {
    const sidebar = document.querySelector('.sidebar');
    if (sidebar.classList.contains('active')) {
      sidebar.classList.remove('active');
    }
  }

  // Tab navigation
  if (e.key === 'Tab') {
    const buttons = document.querySelectorAll('button, a, input');
    document.addEventListener('focus', function(e) {
      if (e.target.tagName === 'BUTTON' || e.target.tagName === 'A') {
        e.target.style.outline = '2px solid #2563EB';
        e.target.style.outlineOffset = '2px';
      }
    }, true);
  }
});

// ==================== OBSERVAÇÃO DE MUDANÇAS ====================

// Observer para recarregar gráfico quando necessário
const observer = new MutationObserver(function(mutations) {
  mutations.forEach(function(mutation) {
    if (mutation.addedNodes.length) {
      // Você pode disparar lógica aqui quando o DOM muda
    }
  });
});

const config = { childList: true, subtree: true };
observer.observe(document.body, config);

// ==================== EXPORT ====================

// Deixa funções globais acessíveis para extensões futuras
window.PharmacyERP = {
  updateKPIValues,
  showNotification,
  formatCurrency,
  formatDate,
  initChart
};