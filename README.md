# Guardian - Microserviço de Segurança Canonika

## Descrição

O Guardian é o sistema de segurança e compliance do Canonika, responsável pela gestão de identidades, autenticação, autorização e auditoria.

## Funcionalidades

- **Gestão de Identidades**: Integração com Keycloak para usuários e roles
- **Autenticação**: SSO, MFA, OAuth/OIDC
- **Autorização**: Políticas OPA (ABAC/ReBAC)
- **Auditoria**: Logs de segurança e compliance
- **Monitoramento**: Dashboard de segurança em tempo real

## Tecnologias

- **Frontend**: Vue.js 3 + Vite
- **Backend**: FastAPI (Python)
- **Identity Provider**: Keycloak
- **Authorization**: OPA (Open Policy Agent)
- **Database**: PostgreSQL + ClickHouse
- **Cache**: Redis
- **Containerização**: Docker

## Estrutura do Projeto

```
guardian/
├── api/                 # Backend FastAPI
│   ├── main.py         # API principal
│   └── requirements.txt # Dependências Python
├── web/                # Frontend Vue.js
│   ├── src/
│   │   └── App.vue     # Componente principal
│   ├── tests/          # Testes unitários
│   ├── cypress/        # Testes e2e
│   └── package.json    # Dependências Node.js
├── nginx/              # Configuração do proxy
│   └── nginx.conf
├── Dockerfile          # Container principal
└── README.md           # Esta documentação
```

## Portas

- **3705**: Interface web (Nginx)
- **8005**: API FastAPI
- **5175**: Hot reload (desenvolvimento)

## Integração com Keycloak

O Guardian integra-se com Keycloak para:

- **Realm**: `canonika`
- **Client**: `guardian-client`
- **Users**: Gestão de usuários e roles
- **Admin Console**: `http://localhost:8080/admin`
- **Account Console**: `http://localhost:8080/realms/canonika/account`

## Desenvolvimento

### Pré-requisitos

- Docker e Docker Compose
- Node.js 18+
- Python 3.9+
- Keycloak rodando na porta 8080

### Execução Local

```bash
# Instalar dependências
cd web && npm install

# Executar frontend (hot reload)
npm run dev

# Executar backend
cd ../api && python -m uvicorn main:app --reload --port 8005

# Executar testes
npm run test          # Unit tests
npm run test:e2e      # End-to-end tests
```

### Execução com Docker

```bash
# Build e execução
docker-compose up guardian

# Apenas build
docker build -t guardian .
```

## Testes

### Unit Tests (TDD)

```bash
npm run test
npm run test:coverage
```

### End-to-End Tests (BDD)

```bash
npm run test:e2e
npm run test:e2e:open
```

## Configuração

### Variáveis de Ambiente

- `DEV_MODE`: Habilita hot reload (true/false)
- `KEYCLOAK_URL`: URL do Keycloak (http://localhost:8080)
- `KEYCLOAK_REALM`: Realm do Keycloak (canonika)
- `KEYCLOAK_CLIENT_ID`: Client ID (guardian-client)
- `KEYCLOAK_CLIENT_SECRET`: Client Secret
- `OPA_URL`: URL do OPA (http://localhost:8181)
- `DATABASE_URL`: URL do PostgreSQL
- `REDIS_URL`: URL do Redis
- `CLICKHOUSE_URL`: URL do ClickHouse

## Funcionalidades de Segurança

### Autenticação

- **SSO**: Single Sign-On com Keycloak
- **MFA**: Multi-Factor Authentication
- **OAuth 2.0**: Authorization Code Flow
- **OIDC**: OpenID Connect
- **SAML**: Integração SAML (futuro)

### Autorização

- **ABAC**: Attribute-Based Access Control
- **ReBAC**: Relationship-Based Access Control
- **OPA**: Políticas declarativas
- **RBAC**: Role-Based Access Control

### Auditoria

- **Logs de Segurança**: Todas as ações de segurança
- **Logs de Compliance**: Conformidade regulatória
- **Métricas**: KPIs de segurança
- **Alertas**: Notificações em tempo real

## Status

✅ **Implementado**:
- Interface de gestão de segurança
- Integração com Keycloak
- Dashboard de monitoramento
- Hot reload em desenvolvimento
- Testes unitários e e2e
- Containerização Docker

🔄 **Em Desenvolvimento**:
- Políticas OPA avançadas
- Logs de auditoria detalhados
- Métricas de segurança
- Alertas automáticos

📋 **Planejado**:
- Integração com SIEM
- Compliance automático
- Threat Intelligence
- Incident Response 