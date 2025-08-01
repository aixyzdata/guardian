<template>
  <div id="app" class="canonika-app">
    <!-- Header futurista -->
    <header class="canonika-header">
      <div class="header-content">
        <div class="logo-section">
          <div class="logo-icon">
            <div class="logo-hexagon"></div>
            <div class="logo-pulse"></div>
          </div>
          <div class="logo-text-container">
            <h1 class="logo-text">CANONIKA</h1>
            <div class="module-title-with-icon">
              <div :class="['module-icon', serviceConfig.iconClass]"></div>
              <span class="logo-subtitle">{{ serviceConfig.name }}</span>
            </div>
          </div>
        </div>
        <div class="header-actions">
          <div v-if="user" class="user-info">
            <div class="user-avatar">
              <span>{{ user.name.charAt(0).toUpperCase() }}</span>
            </div>
            <span class="user-name">{{ user.name }}</span>
            <div class="user-menu">
              <button @click="logout" class="logout-btn">
                <i class="fas fa-sign-out-alt"></i>
                Sair
              </button>
            </div>
          </div>
          <div class="system-status">
            <div class="status-indicator online"></div>
            <span>ONLINE</span>
          </div>
        </div>
      </div>
      <div class="header-glow"></div>
    </header>

    <div class="canonika-layout" :class="{ 'sidebar-collapsed': sidebarCollapsed }">
      <!-- Toggle button para menu retrátil -->
      <button 
        v-if="user" 
        @click="toggleSidebar" 
        class="sidebar-toggle"
        :class="{ 'sidebar-collapsed': sidebarCollapsed }"
      >
        <i class="fas fa-bars"></i>
      </button>

      <!-- Sidebar futurista -->
      <nav class="canonika-sidebar" v-if="user" :class="{ 'sidebar-collapsed': sidebarCollapsed }">
        <div class="sidebar-header">
          <div class="nav-icon active">
            <i class="nav-dot"></i>
            <span v-if="!sidebarCollapsed">SEGURANÇA</span>
          </div>
        </div>
        
        <ul class="nav-menu">
          <!-- Menu items dinâmicos baseados na configuração -->
          <template v-for="menuItem in serviceConfig.menuItems" :key="menuItem.id">
            <!-- Item simples -->
            <li v-if="!menuItem.submenu" class="nav-item" :class="{ active: currentView === menuItem.id }">
              <div class="nav-link" @click="setView(menuItem.id)">
                <div class="nav-icon">
                  <i :class="menuItem.icon"></i>
                </div>
                <div v-if="!sidebarCollapsed" class="nav-text">
                  <span class="nav-title">{{ menuItem.title }}</span>
                  <span v-if="menuItem.subtitle" class="service-subtitle">{{ menuItem.subtitle }}</span>
                </div>
              </div>
            </li>
            
            <!-- Item com submenu -->
            <li v-else class="nav-item" :class="{ active: openSubmenus[menuItem.id] }">
              <div class="nav-link" @click="toggleSubmenu(menuItem.id)">
                <div class="nav-icon">
                  <i :class="menuItem.icon"></i>
                </div>
                <div v-if="!sidebarCollapsed" class="nav-text">
                  <span class="nav-title">{{ menuItem.title }}</span>
                  <span v-if="menuItem.subtitle" class="service-subtitle">{{ menuItem.subtitle }}</span>
                </div>
                <i v-if="!sidebarCollapsed" :class="openSubmenus[menuItem.id] ? 'fas fa-chevron-down' : 'fas fa-chevron-right'" class="submenu-icon"></i>
              </div>
              
              <!-- Submenu -->
              <ul v-if="!sidebarCollapsed" class="nav flex-column submenu" :class="{ show: openSubmenus[menuItem.id] }">
                <li v-for="subItem in menuItem.submenu" :key="subItem.id" class="nav-item">
                  <div class="nav-link" @click="setView(subItem.id)">
                    <div class="nav-icon">
                      <i :class="subItem.icon"></i>
                    </div>
                    <div class="nav-text">
                      <div class="nav-title">{{ subItem.title }}</div>
                      <div v-if="subItem.subtitle" class="service-subtitle">{{ subItem.subtitle }}</div>
                    </div>
                  </div>
                </li>
              </ul>
            </li>
          </template>
        </ul>
      </nav>

      <!-- Main Content -->
      <main class="canonika-main">
        <!-- Dashboard -->
        <div v-if="currentView === 'dashboard'" class="canonika-view">
          <div class="view-header">
            <h2 class="view-title">Dashboard de Segurança</h2>
            <p class="view-subtitle">Monitoramento em tempo real do sistema</p>
          </div>

          <div class="dashboard-grid">
            <!-- Status dos Serviços -->
            <div class="canonika-card">
              <div class="card-header">
                <h3 class="card-title">Status dos Serviços</h3>
                <button @click="refreshStatus" class="refresh-btn">
                  <i class="fas fa-sync-alt"></i>
                </button>
              </div>
              <div class="card-content">
                <div class="service-status" v-for="service in serviceStatus" :key="service.name">
                  <div class="service-info">
                    <div class="service-icon">
                      <i :class="service.icon"></i>
                    </div>
                    <div class="service-details">
                      <span class="service-name">{{ service.name }}</span>
                      <span class="service-status" :class="service.status">{{ service.statusText }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Ações Rápidas -->
            <div class="canonika-card">
              <div class="card-header">
                <h3 class="card-title">Ações Rápidas</h3>
              </div>
              <div class="card-content">
                <div class="quick-actions">
                  <button @click="openKeycloakAdmin" class="canonika-btn canonika-btn-primary">
                    <i class="fas fa-users-cog"></i>
                    Keycloak Admin
                  </button>
                  <button @click="openOPA" class="canonika-btn canonika-btn-secondary">
                    <i class="fas fa-shield-alt"></i>
                    OPA Console
                  </button>
                  <button @click="viewAuditLogs" class="canonika-btn canonika-btn-secondary">
                    <i class="fas fa-file-alt"></i>
                    Logs de Auditoria
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Autenticação -->
        <div v-if="currentView === 'autenticacao'" class="canonika-view">
          <div class="view-header">
            <h2 class="view-title">Sistema de Autenticação</h2>
            <p class="view-subtitle">Configurações de login e segurança</p>
          </div>

          <div class="auth-container">
            <div class="canonika-card">
              <div class="card-header">
                <h3 class="card-title">Configurações de Segurança</h3>
              </div>
              <div class="card-content">
                <div class="auth-method">
                  <div class="method-icon">
                    <i class="fas fa-key"></i>
                  </div>
                  <div class="method-info">
                    <span class="method-name">Autenticação OAuth/OIDC</span>
                    <span class="method-status enabled">Ativo</span>
                  </div>
                  <button @click="toggleAuthMethod" class="canonika-btn canonika-btn-small">
                    Configurar
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Autorização -->
        <div v-if="currentView === 'autorizacao'" class="canonika-view">
          <div class="view-header">
            <h2 class="view-title">Sistema de Autorização</h2>
            <p class="view-subtitle">Políticas OPA e controle de acesso</p>
          </div>

          <div class="authorization-container">
            <div class="canonika-card">
              <div class="card-header">
                <h3 class="card-title">Status OPA</h3>
                <div class="card-actions">
                  <button @click="openOPA" class="canonika-btn canonika-btn-secondary">
                    <i class="fas fa-external-link-alt"></i>
                    Abrir OPA
                  </button>
                </div>
              </div>
              <div class="card-content">
                <div class="policy-status">
                  <div class="status-item">
                    <span class="status-label">Status OPA:</span>
                    <span class="status-value online">Online</span>
                  </div>
                  <div class="status-item">
                    <span class="status-label">Políticas Carregadas:</span>
                    <span class="status-value">{{ opaStats.loadedPolicies }}</span>
                  </div>
                  <div class="status-item">
                    <span class="status-label">Decisões/Minuto:</span>
                    <span class="status-value">{{ opaStats.decisionsPerMinute }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Sessões -->
        <div v-if="currentView === 'sessoes'" class="canonika-view">
          <div class="view-header">
            <h2 class="view-title">Gestão de Sessões</h2>
            <p class="view-subtitle">Controle de sessões ativas</p>
          </div>

          <div class="sessions-container">
            <div class="canonika-card">
              <div class="card-header">
                <h3 class="card-title">Sessões Ativas</h3>
                <button @click="refreshSessions" class="refresh-btn">
                  <i class="fas fa-sync-alt"></i>
                </button>
              </div>
              <div class="card-content">
                <div class="sessions-list">
                  <div class="session-item" v-for="session in activeSessions" :key="session.id">
                    <div class="session-info">
                      <span class="user-name">{{ session.user }}</span>
                      <span class="session-ip">{{ session.ip }}</span>
                      <span class="session-time">{{ session.lastActivity }}</span>
                    </div>
                    <button @click="terminateSession(session.id)" class="canonika-btn canonika-btn-danger">
                      Encerrar
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Auditoria -->
        <div v-if="currentView === 'auditoria'" class="canonika-view">
          <div class="view-header">
            <h2 class="view-title">Logs de Auditoria</h2>
            <p class="view-subtitle">Histórico de eventos de segurança</p>
          </div>

          <div class="audit-container">
            <div class="canonika-card">
              <div class="card-header">
                <h3 class="card-title">Eventos Recentes</h3>
              </div>
              <div class="card-content">
                <div class="audit-events">
                  <div class="event-item" v-for="event in auditEvents" :key="event.id" :class="event.level">
                    <div class="event-icon">
                      <i :class="event.icon"></i>
                    </div>
                    <div class="event-details">
                      <span class="event-message">{{ event.message }}</span>
                      <span class="event-user">{{ event.user }}</span>
                      <span class="event-time">{{ event.timestamp }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      currentView: 'dashboard',
      sidebarCollapsed: false,
      openSubmenus: {},
      
      // Configuração do serviço Guardian
      serviceConfig: {
        name: 'GUARDIAN',
        iconClass: 'fas fa-shield-alt',
        menuItems: [
          {
            id: 'dashboard',
            title: 'Dashboard',
            icon: 'fas fa-tachometer-alt',
            subtitle: 'Visão Geral'
          },
          {
            id: 'keycloak',
            title: 'Keycloak Admin',
            icon: 'fas fa-users-cog',
            subtitle: 'Gestão de Usuários'
          },
          {
            id: 'autenticacao',
            title: 'Autenticação',
            icon: 'fas fa-key',
            subtitle: 'Login & MFA'
          },
          {
            id: 'autorizacao',
            title: 'Autorização',
            icon: 'fas fa-shield-alt',
            subtitle: 'OPA & Políticas'
          },
          {
            id: 'sessoes',
            title: 'Sessões',
            icon: 'fas fa-clock',
            subtitle: 'Controle Ativo'
          },
          {
            id: 'auditoria',
            title: 'Auditoria',
            icon: 'fas fa-file-alt',
            subtitle: 'Logs & Relatórios'
          }
        ]
      },
      
      user: {
        id: 'admin-001',
        name: 'Administrador',
        email: 'admin@canonika.io',
        roles: ['admin', 'security_admin']
      },
      
      // Status dos serviços
      serviceStatus: [
        { name: 'Keycloak', status: 'online', statusText: 'Online', icon: 'fas fa-users-cog' },
        { name: 'OPA', status: 'online', statusText: 'Online', icon: 'fas fa-shield-alt' },
        { name: 'PostgreSQL', status: 'online', statusText: 'Online', icon: 'fas fa-database' },
        { name: 'Redis', status: 'online', statusText: 'Online', icon: 'fas fa-memory' }
      ],
      
      // Estatísticas OPA
      opaStats: {
        loadedPolicies: 5,
        decisionsPerMinute: 245
      },
      
      // Sessões ativas
      activeSessions: [
        { id: 1, user: 'admin@canonika.io', ip: '192.168.1.100', lastActivity: '2 min atrás' },
        { id: 2, user: 'user1@canonika.io', ip: '192.168.1.101', lastActivity: '5 min atrás' },
        { id: 3, user: 'user2@canonika.io', ip: '192.168.1.102', lastActivity: '10 min atrás' }
      ],
      
      // Eventos de auditoria
      auditEvents: [
        { id: 1, level: 'info', service: 'keycloak', message: 'Login bem-sucedido', user: 'admin@canonika.io', ip: '192.168.1.100', timestamp: '2 min atrás', icon: 'fas fa-sign-in-alt' },
        { id: 2, level: 'warn', service: 'opa', message: 'Tentativa de acesso negada', user: 'user1@canonika.io', ip: '192.168.1.101', timestamp: '5 min atrás', icon: 'fas fa-ban' },
        { id: 3, level: 'error', service: 'guardian', message: 'Falha na conexão com OPA', user: 'system', ip: 'localhost', timestamp: '10 min atrás', icon: 'fas fa-exclamation-triangle' }
      ]
    }
  },
  
  methods: {
    setView(view) {
      this.currentView = view
    },
    
    toggleSidebar() {
      this.sidebarCollapsed = !this.sidebarCollapsed
    },
    
    toggleSubmenu(menuId) {
      this.$set(this.openSubmenus, menuId, !this.openSubmenus[menuId])
    },
    
    logout() {
      // Implementar logout via Keycloak
      window.location.href = 'http://localhost:8080/auth/realms/canonika/protocol/openid-connect/logout'
    },
    
    refreshStatus() {
      // Implementar refresh do status dos serviços
      console.log('Atualizando status dos serviços...')
    },
    
    openKeycloakAdmin() {
      window.open('http://localhost:8080/admin', '_blank')
    },
    
    openOPA() {
      window.open('http://localhost:8181', '_blank')
    },
    
    viewAuditLogs() {
      this.setView('auditoria')
    },
    
    toggleAuthMethod() {
      // Implementar toggle do método de autenticação
      console.log('Alterando método de autenticação...')
    },
    
    refreshSessions() {
      // Implementar refresh das sessões
      console.log('Atualizando sessões...')
    },
    
    terminateSession(sessionId) {
      // Implementar encerramento de sessão
      this.activeSessions = this.activeSessions.filter(s => s.id !== sessionId)
    }
  }
}
</script>

<style scoped>
/* Reset CSS Universal */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  margin: 0 !important;
  padding: 0 !important;
  border: none !important;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  width: 100%;
  height: 100%;
  overflow-x: hidden;
}

/* App Container */
.canonika-app {
  min-height: 100vh;
  background: linear-gradient(135deg, #1e293b 0%, #334155 50%, #475569 100%);
  color: #e2e8f0;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Header */
.canonika-header {
  background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 50%, #1e40af 100%);
  padding: 1rem 2rem;
  position: relative;
  overflow: hidden;
  height: 60px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: relative;
  z-index: 2;
  height: 100%;
}

.logo-section {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.logo-icon {
  position: relative;
  width: 2.5rem;
  height: 2.5rem;
}

.logo-hexagon {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
  clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.logo-pulse {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 0.25rem;
  height: 0.25rem;
  background: #ffffff;
  border-radius: 50%;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; transform: translate(-50%, -50%) scale(1); }
  50% { opacity: 0.7; transform: translate(-50%, -50%) scale(1.1); }
}

.logo-text-container {
  display: flex;
  flex-direction: column;
}

.logo-text {
  font-size: 1.5rem;
  font-weight: 700;
  color: #ffffff;
  letter-spacing: 0.1em;
  margin: 0;
}

.logo-subtitle {
  font-size: 0.8rem;
  color: #94a3b8;
  font-weight: 500;
  letter-spacing: 0.05em;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.system-status {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.8rem;
  color: #94a3b8;
}

.status-indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.status-indicator.online {
  background: #10b981;
  animation: pulse 2s infinite;
}

.logout-btn {
  background: rgba(239, 68, 68, 0.2);
  border: 1px solid #ef4444;
  color: #ef4444;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-size: 0.8rem;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.logout-btn:hover {
  background: #ef4444;
  color: white;
}

/* Layout */
.canonika-layout {
  display: flex;
  min-height: calc(100vh - 60px);
}

/* Sidebar */
.canonika-sidebar {
  width: 280px;
  background: rgba(30, 41, 59, 0.9);
  border-right: 1px solid #475569;
  padding: 1rem 0;
  backdrop-filter: blur(10px);
}

.sidebar-header {
  padding: 0 1.5rem 1rem;
  border-bottom: 1px solid #475569;
  margin-bottom: 1rem;
}

.nav-icon {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #94a3b8;
  font-size: 0.8rem;
  font-weight: 600;
}

.nav-icon.active {
  color: #3b82f6;
}

.nav-dot {
  width: 6px;
  height: 6px;
  background: currentColor;
  border-radius: 50%;
}

.nav-menu {
  list-style: none;
}

.nav-item {
  margin-bottom: 0.5rem;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.75rem 1.5rem;
  color: #94a3b8;
  cursor: pointer;
  transition: all 0.3s;
  border-radius: 0 8px 8px 0;
}

.nav-link:hover {
  background: rgba(59, 130, 246, 0.1);
  color: #3b82f6;
}

.nav-item.active .nav-link {
  background: rgba(59, 130, 246, 0.2);
  color: #3b82f6;
  border-right: 3px solid #3b82f6;
}

.nav-icon {
  width: 20px;
  text-align: center;
}

.nav-text {
  display: flex;
  flex-direction: column;
}

.nav-title {
  font-weight: 600;
  font-size: 0.9rem;
}

.service-subtitle {
  font-size: 0.7rem;
  color: #64748b;
  margin-top: 0.1rem;
}

/* Main Content */
.canonika-main {
  flex: 1;
  padding: 2rem;
  overflow-y: auto;
}

.canonika-view {
  max-width: 1200px;
}

.view-header {
  margin-bottom: 2rem;
}

.view-title {
  font-size: 2rem;
  font-weight: 700;
  color: #ffffff;
  margin-bottom: 0.5rem;
}

.view-subtitle {
  color: #94a3b8;
  font-size: 1rem;
}

/* Cards */
.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 1.5rem;
}

.canonika-card {
  background: rgba(30, 41, 59, 0.9);
  border: 1px solid #475569;
  border-radius: 12px;
  backdrop-filter: blur(10px);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #475569;
}

.card-title {
  font-size: 1.2rem;
  font-weight: 600;
  color: #ffffff;
}

.card-content {
  padding: 1.5rem;
}

.refresh-btn {
  background: none;
  border: none;
  color: #94a3b8;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 6px;
  transition: all 0.3s;
}

.refresh-btn:hover {
  background: rgba(59, 130, 246, 0.1);
  color: #3b82f6;
}

/* Service Status */
.service-status {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 0;
  border-bottom: 1px solid #334155;
}

.service-status:last-child {
  border-bottom: none;
}

.service-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.service-icon {
  width: 40px;
  height: 40px;
  background: rgba(59, 130, 246, 0.1);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #3b82f6;
}

.service-details {
  display: flex;
  flex-direction: column;
}

.service-name {
  font-weight: 600;
  color: #ffffff;
}

.service-status {
  font-size: 0.8rem;
  margin-top: 0.2rem;
}

.service-status.online {
  color: #10b981;
}

.service-status.offline {
  color: #ef4444;
}

/* Quick Actions */
.quick-actions {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.canonika-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  text-decoration: none;
  justify-content: center;
}

.canonika-btn-primary {
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
  color: white;
}

.canonika-btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(59, 130, 246, 0.3);
}

.canonika-btn-secondary {
  background: rgba(59, 130, 246, 0.1);
  color: #3b82f6;
  border: 1px solid #3b82f6;
}

.canonika-btn-secondary:hover {
  background: #3b82f6;
  color: white;
}

.canonika-btn-danger {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
  border: 1px solid #ef4444;
}

.canonika-btn-danger:hover {
  background: #ef4444;
  color: white;
}

.canonika-btn-small {
  padding: 0.5rem 0.75rem;
  font-size: 0.8rem;
}

/* Auth Methods */
.auth-container {
  display: grid;
  gap: 1.5rem;
}

.auth-method {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem;
  background: rgba(51, 65, 85, 0.5);
  border-radius: 8px;
  border: 1px solid #475569;
  margin-bottom: 1rem;
}

.method-icon {
  width: 40px;
  height: 40px;
  background: rgba(59, 130, 246, 0.1);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #3b82f6;
}

.method-info {
  flex: 1;
  margin-left: 1rem;
}

.method-name {
  display: block;
  font-weight: 600;
  color: #ffffff;
}

.method-status {
  font-size: 0.8rem;
  margin-top: 0.2rem;
}

.method-status.enabled {
  color: #10b981;
}

.method-status.disabled {
  color: #ef4444;
}

/* Authorization */
.authorization-container {
  display: grid;
  gap: 1.5rem;
}

.policy-status {
  display: grid;
  gap: 1rem;
}

.status-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem;
  background: rgba(51, 65, 85, 0.5);
  border-radius: 6px;
}

.status-label {
  color: #94a3b8;
  font-size: 0.9rem;
}

.status-value {
  font-weight: 600;
}

.status-value.online {
  color: #10b981;
}

/* Sessions */
.sessions-container {
  display: grid;
  gap: 1.5rem;
}

.sessions-list {
  display: grid;
  gap: 0.5rem;
}

.session-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem;
  background: rgba(51, 65, 85, 0.5);
  border-radius: 8px;
  border: 1px solid #475569;
}

.session-info {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}

.user-name {
  font-weight: 600;
  color: #ffffff;
}

.session-ip {
  font-size: 0.8rem;
  color: #94a3b8;
}

.session-time {
  font-size: 0.8rem;
  color: #64748b;
}

/* Audit */
.audit-container {
  display: grid;
  gap: 1.5rem;
}

.audit-events {
  display: grid;
  gap: 0.5rem;
}

.event-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: rgba(51, 65, 85, 0.5);
  border-radius: 8px;
  border-left: 4px solid;
}

.event-item.info {
  border-left-color: #3b82f6;
}

.event-item.warn {
  border-left-color: #f59e0b;
}

.event-item.error {
  border-left-color: #ef4444;
}

.event-icon {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.8rem;
}

.event-item.info .event-icon {
  background: rgba(59, 130, 246, 0.2);
  color: #3b82f6;
}

.event-item.warn .event-icon {
  background: rgba(245, 158, 11, 0.2);
  color: #f59e0b;
}

.event-item.error .event-icon {
  background: rgba(239, 68, 68, 0.2);
  color: #ef4444;
}

.event-details {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}

.event-message {
  font-weight: 600;
  color: #ffffff;
}

.event-user {
  font-size: 0.8rem;
  color: #94a3b8;
}

.event-time {
  font-size: 0.8rem;
  color: #64748b;
}

/* Responsive */
@media (max-width: 768px) {
  .canonika-sidebar {
    width: 100%;
    position: fixed;
    bottom: 0;
    left: 0;
    z-index: 1000;
    border-right: none;
    border-top: 1px solid #475569;
  }
  
  .canonika-main {
    margin-bottom: 80px;
  }
  
  .dashboard-grid {
    grid-template-columns: 1fr;
  }
}
</style> 