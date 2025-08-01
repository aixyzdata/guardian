<template>
  <MasterPage 
    :serviceConfig="serviceConfig"
    @view-changed="handleViewChange"
    @login="handleLogin"
    @logout="handleLogout"
  >
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
            <h3 class="card-title">Status do OPA</h3>
          </div>
          <div class="card-content">
            <div class="policy-status">
              <div class="status-item">
                <span class="status-label">Políticas Carregadas</span>
                <span class="status-value">{{ opaStats.loadedPolicies }}</span>
              </div>
              <div class="status-item">
                <span class="status-label">Decisões/min</span>
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
        <h2 class="view-title">Sessões Ativas</h2>
        <p class="view-subtitle">Controle de sessões em tempo real</p>
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
            <div class="session-item" v-for="session in activeSessions" :key="session.id">
              <div class="session-info">
                <span class="session-user">{{ session.user }}</span>
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

    <!-- Auditoria -->
    <div v-if="currentView === 'auditoria'" class="canonika-view">
      <div class="view-header">
        <h2 class="view-title">Logs de Auditoria</h2>
        <p class="view-subtitle">Histórico de eventos do sistema</p>
      </div>

      <div class="audit-container">
        <div class="canonika-card">
          <div class="card-header">
            <h3 class="card-title">Eventos Recentes</h3>
          </div>
          <div class="card-content">
            <div class="audit-event" v-for="event in auditEvents" :key="event.id" :class="event.level">
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
  </MasterPage>
</template>

<script>
import MasterPage from './components/MasterPage.vue'

export default {
  name: 'App',
  components: {
    MasterPage
  },
  data() {
    return {
      currentView: 'dashboard',
      
      // Configuração do serviço Guardian
      serviceConfig: {
        name: 'GUARDIAN',
        description: 'Sistema de Segurança e Autenticação',
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
    handleViewChange(viewId) {
      this.currentView = viewId
    },
    
    handleLogin(user) {
      this.user = user
      console.log('Usuário logado:', user)
    },
    
    handleLogout() {
      this.user = null
      console.log('Usuário deslogado')
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
/* View Styles */
.canonika-view {
  width: 100%;
}

.view-header {
  margin-bottom: 2rem;
}

.view-title {
  font-size: 2rem;
  font-weight: 600;
  color: #e2e8f0;
  margin-bottom: 0.5rem;
}

.view-subtitle {
  color: #94a3b8;
  font-size: 1rem;
}

/* Dashboard Grid */
.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

/* Cards */
.canonika-card {
  background: rgba(15, 23, 42, 0.8);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.card-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #e2e8f0;
  margin: 0;
}

.refresh-btn {
  background: rgba(59, 130, 246, 0.1);
  color: #3b82f6;
  border: 1px solid #3b82f6;
  padding: 0.5rem;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
}

.refresh-btn:hover {
  background: #3b82f6;
  color: white;
}

/* Service Status */
.service-status {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 0;
  border-bottom: 1px solid rgba(148, 163, 184, 0.1);
}

.service-status:last-child {
  border-bottom: none;
}

.service-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.service-icon {
  width: 2rem;
  height: 2rem;
  background: rgba(59, 130, 246, 0.1);
  border-radius: 6px;
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
  font-weight: 500;
  color: #e2e8f0;
}

.service-status {
  font-size: 0.875rem;
  font-weight: 500;
}

.service-status.online {
  color: #10b981;
}

.service-status.offline {
  color: #ef4444;
}

/* Quick Actions */
.quick-actions {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.canonika-btn {
  padding: 0.75rem 1rem;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  border: none;
}

.canonika-btn-primary {
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  color: white;
}

.canonika-btn-primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 10px 25px -5px rgba(59, 130, 246, 0.4);
}

.canonika-btn-secondary {
  background: rgba(148, 163, 184, 0.1);
  color: #94a3b8;
  border: 1px solid rgba(148, 163, 184, 0.2);
}

.canonika-btn-secondary:hover {
  background: rgba(148, 163, 184, 0.2);
  color: #e2e8f0;
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

.session-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem;
  background: rgba(51, 65, 85, 0.5);
  border-radius: 6px;
  margin-bottom: 0.5rem;
}

.session-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.session-user {
  font-weight: 500;
  color: #e2e8f0;
}

.session-ip {
  font-size: 0.875rem;
  color: #94a3b8;
}

.session-time {
  font-size: 0.75rem;
  color: #64748b;
}

/* Audit */
.audit-container {
  display: grid;
  gap: 1.5rem;
}

.audit-event {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem;
  background: rgba(51, 65, 85, 0.5);
  border-radius: 6px;
  margin-bottom: 0.5rem;
}

.audit-event.info {
  border-left: 3px solid #3b82f6;
}

.audit-event.warn {
  border-left: 3px solid #f59e0b;
}

.audit-event.error {
  border-left: 3px solid #ef4444;
}

.event-icon {
  width: 2rem;
  height: 2rem;
  background: rgba(59, 130, 246, 0.1);
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #3b82f6;
}

.event-details {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.event-message {
  font-weight: 500;
  color: #e2e8f0;
}

.event-user {
  font-size: 0.875rem;
  color: #94a3b8;
}

.event-time {
  font-size: 0.75rem;
  color: #64748b;
}
</style> 