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

      <!-- Conteúdo principal -->
      <main :class="['canonika-main', { 'sidebar-collapsed': sidebarCollapsed }]">
        <!-- Tela de login -->
        <div v-if="!user" class="login-container">
          <div class="login-card">
            <div class="login-header">
              <div class="login-logo">
                <div class="logo-hexagon-large"></div>
                <div class="logo-pulse-large"></div>
              </div>
              <h2 class="login-title">Acesso ao {{ serviceConfig.name }}</h2>
              <p class="login-subtitle">{{ serviceConfig.description }}</p>
            </div>
            <form @submit.prevent="login" class="login-form">
              <div class="form-group">
                <div class="input-container">
                  <span class="input-icon">👤</span>
                  <input 
                    v-model="loginForm.username" 
                    type="text" 
                    placeholder="Usuário" 
                    class="form-input"
                    required
                  >
                </div>
              </div>
              <div class="form-group">
                <div class="input-container">
                  <span class="input-icon">🔒</span>
                  <input 
                    v-model="loginForm.password" 
                    type="password" 
                    placeholder="Senha" 
                    class="form-input"
                    required
                  >
                </div>
              </div>
              <button type="submit" class="login-btn">
                <span>🚀</span> Entrar
              </button>
            </form>
          </div>
        </div>

        <!-- Conteúdo do serviço -->
        <div v-else class="service-content">
          <slot></slot>
        </div>
      </main>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MasterPage',
  props: {
    serviceConfig: {
      type: Object,
      required: true,
      default: () => ({
        name: 'Serviço',
        description: 'Descrição do serviço',
        iconClass: 'icon-default',
        menuItems: []
      })
    }
  },
  data() {
    return {
      user: null,
      sidebarCollapsed: false,
      currentView: 'dashboard',
      openSubmenus: {},
      loginForm: {
        username: '',
        password: ''
      }
    }
  },
  methods: {
    toggleSidebar() {
      this.sidebarCollapsed = !this.sidebarCollapsed
    },
    setView(viewId) {
      this.currentView = viewId
      this.$emit('view-changed', viewId)
    },
    toggleSubmenu(menuId) {
      this.$set(this.openSubmenus, menuId, !this.openSubmenus[menuId])
    },
    login() {
      // Simular login para desenvolvimento
      this.user = {
        id: 'admin-001',
        name: 'Administrador',
        email: 'admin@canonika.io',
        roles: ['admin', 'security_admin']
      }
      this.$emit('login', this.user)
    },
    logout() {
      this.user = null
      this.$emit('logout')
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
}

/* Layout Principal */
.canonika-app {
  min-height: 100vh;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
  color: #e2e8f0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* Header Futurista */
.canonika-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  background: rgba(15, 23, 42, 0.95);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(148, 163, 184, 0.1);
  padding: 0.75rem 0;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 1.5rem;
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
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
  position: relative;
}

.logo-pulse {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 0.5rem;
  height: 0.5rem;
  background: #ffffff;
  border-radius: 50%;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { 
    opacity: 1; 
    transform: translate(-50%, -50%) scale(1);
  }
  50% { 
    opacity: 0.7; 
    transform: translate(-50%, -50%) scale(1.2);
  }
}

.logo-text-container {
  display: flex;
  flex-direction: column;
}

.logo-text {
  font-size: 1.5rem;
  font-weight: 700;
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0;
}

.module-title-with-icon {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 0.25rem;
}

.module-icon {
  width: 1rem;
  height: 1rem;
  background: linear-gradient(135deg, #10b981, #059669);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.5rem;
  color: white;
}

.logo-subtitle {
  font-size: 0.875rem;
  color: #94a3b8;
  font-weight: 500;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.user-avatar {
  width: 2rem;
  height: 2rem;
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 600;
  font-size: 0.875rem;
}

.user-name {
  color: #e2e8f0;
  font-weight: 500;
}

.user-menu {
  position: relative;
}

.logout-btn {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
  border: 1px solid #ef4444;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.logout-btn:hover {
  background: #ef4444;
  color: white;
}

.system-status {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: rgba(16, 185, 129, 0.1);
  border: 1px solid #10b981;
  border-radius: 6px;
  font-size: 0.875rem;
  color: #10b981;
}

.status-indicator {
  width: 0.5rem;
  height: 0.5rem;
  border-radius: 50%;
  animation: pulse 2s ease-in-out infinite;
}

.status-indicator.online {
  background: #10b981;
}

.header-glow {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, #3b82f6, transparent);
}

/* Layout Principal */
.canonika-layout {
  display: flex;
  min-height: 100vh;
  padding-top: 4rem;
}

/* Sidebar Toggle */
.sidebar-toggle {
  position: fixed;
  top: 5rem;
  left: 1rem;
  z-index: 999;
  background: rgba(15, 23, 42, 0.9);
  border: 1px solid rgba(148, 163, 184, 0.2);
  color: #e2e8f0;
  padding: 0.5rem;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s;
  backdrop-filter: blur(10px);
}

.sidebar-toggle:hover {
  background: rgba(59, 130, 246, 0.1);
  border-color: #3b82f6;
}

.sidebar-toggle.sidebar-collapsed {
  left: 1rem;
}

/* Sidebar Futurista */
.canonika-sidebar {
  width: 280px;
  background: rgba(15, 23, 42, 0.95);
  backdrop-filter: blur(10px);
  border-right: 1px solid rgba(148, 163, 184, 0.1);
  padding: 1rem 0;
  transition: all 0.3s ease;
  overflow-y: auto;
  height: calc(100vh - 4rem);
}

.canonika-sidebar.sidebar-collapsed {
  width: 4rem;
}

.sidebar-header {
  padding: 0 1rem 1rem;
  border-bottom: 1px solid rgba(148, 163, 184, 0.1);
  margin-bottom: 1rem;
}

.nav-icon.active {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #94a3b8;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.nav-dot {
  width: 0.25rem;
  height: 0.25rem;
  background: #3b82f6;
  border-radius: 50%;
}

.nav-menu {
  list-style: none;
  padding: 0;
  margin: 0;
}

.nav-item {
  margin: 0.25rem 0;
}

.nav-link {
  display: flex;
  align-items: center;
  padding: 0.75rem 1rem;
  color: #94a3b8;
  text-decoration: none;
  transition: all 0.2s;
  cursor: pointer;
  position: relative;
}

.nav-link:hover {
  background: rgba(59, 130, 246, 0.1);
  color: #3b82f6;
}

.nav-item.active .nav-link {
  background: rgba(59, 130, 246, 0.15);
  color: #3b82f6;
  border-right: 2px solid #3b82f6;
}

.nav-icon {
  width: 1.5rem;
  height: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 0.75rem;
  font-size: 0.875rem;
}

.nav-text {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.nav-title {
  font-weight: 500;
  font-size: 0.875rem;
}

.service-subtitle {
  font-size: 0.75rem;
  color: #64748b;
  margin-top: 0.125rem;
}

.submenu-icon {
  font-size: 0.75rem;
  transition: transform 0.2s;
}

.submenu {
  list-style: none;
  padding-left: 2.5rem;
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.3s ease;
}

.submenu.show {
  max-height: 200px;
}

/* Main Content */
.canonika-main {
  flex: 1;
  padding: 2rem;
  transition: all 0.3s ease;
}

.canonika-main.sidebar-collapsed {
  margin-left: 0;
}

/* Login Container */
.login-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: calc(100vh - 4rem);
  padding: 2rem;
}

.login-card {
  background: rgba(15, 23, 42, 0.8);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 12px;
  padding: 2.5rem;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
}

.login-header {
  text-align: center;
  margin-bottom: 2rem;
}

.login-logo {
  position: relative;
  width: 4rem;
  height: 4rem;
  margin: 0 auto 1rem;
}

.logo-hexagon-large {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
  position: relative;
}

.logo-pulse-large {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 0.5rem;
  height: 0.5rem;
  background: #ffffff;
  border-radius: 50%;
  z-index: 2;
  box-shadow: 0 0 8px rgba(255, 255, 255, 0.8);
  animation: pulse-glow 2s ease-in-out infinite;
}

@keyframes pulse-glow {
  0%, 100% { 
    opacity: 1; 
    transform: translate(-50%, -50%) scale(1);
    box-shadow: 0 0 8px rgba(255, 255, 255, 0.8);
  }
  50% { 
    opacity: 0.7; 
    transform: translate(-50%, -50%) scale(1.2);
    box-shadow: 0 0 16px rgba(255, 255, 255, 1);
  }
}

.login-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #e2e8f0;
  margin-bottom: 0.5rem;
}

.login-subtitle {
  color: #94a3b8;
  font-size: 0.875rem;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.input-container {
  position: relative;
  display: flex;
  align-items: center;
}

.input-icon {
  position: absolute;
  left: 1rem;
  color: #94a3b8;
  font-size: 1rem;
}

.form-input {
  width: 100%;
  padding: 0.75rem 1rem 0.75rem 2.5rem;
  background: rgba(30, 41, 59, 0.8);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 8px;
  color: #e2e8f0;
  font-size: 0.875rem;
  transition: all 0.2s;
}

.form-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.form-input::placeholder {
  color: #64748b;
}

.login-btn {
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  color: white;
  border: none;
  padding: 0.875rem 1.5rem;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.login-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 10px 25px -5px rgba(59, 130, 246, 0.4);
}

/* Service Content */
.service-content {
  width: 100%;
}
</style> 