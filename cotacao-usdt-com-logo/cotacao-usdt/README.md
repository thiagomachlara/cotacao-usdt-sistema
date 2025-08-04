# Sistema de Cotação USDT/BRL

Sistema completo de cotação USDT/BRL com billboard público e calculadora de volume.

## 🚀 Funcionalidades

### 📊 Sistema Principal
- Cotações em tempo real (atualização a cada 5 segundos)
- Clientes pré-cadastrados: Brasil OTC (0.5%) e Cliente Feitosa (0.65%)
- Calculadora de volume automática
- Considera custo real de 0.25%

### 🎯 Billboard Público
- URL controlável via parâmetro `?spread=X.XXX`
- Design responsivo e profissional
- Atualização automática
- Ideal para compartilhar com clientes

## 📋 Requisitos

- Python 3.11+
- Flask
- SQLAlchemy
- Requests

## 🛠️ Instalação

### Opção 1: Desenvolvimento Local
```bash
# 1. Clonar repositório
git clone <seu-repo>
cd cotacao-usdt

# 2. Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Executar
python src/main.py
```

### Opção 2: Docker
```bash
# 1. Build da imagem
docker build -t cotacao-usdt .

# 2. Executar container
docker run -p 80:5001 cotacao-usdt
```

### Opção 3: AWS EC2
```bash
# 1. Conectar na instância
ssh -i sua-chave.pem ubuntu@seu-ip

# 2. Instalar dependências
sudo apt update
sudo apt install python3 python3-pip nginx -y

# 3. Clonar e configurar
git clone <seu-repo>
cd cotacao-usdt
pip3 install -r requirements.txt

# 4. Configurar nginx (ver guia completo)
```

## 🌐 URLs de Exemplo

### Sistema Principal
- http://localhost:5001/

### Billboard Público
- http://localhost:5001/billboard (sem spread)
- http://localhost:5001/billboard?spread=1.005 (0.5%)
- http://localhost:5001/billboard?spread=1.007 (0.7%)
- http://localhost:5001/billboard?spread=1.015 (1.5%)

## 🔧 Configuração

### API Externa
O sistema utiliza a API da Laas:
```
https://laas.azify.tech/api/v2.0/market/price?pair=USDT_BRL
```

### Banco de Dados
SQLite local com dados pré-configurados:
- Percentuais padrão: 0.5% e 0.65%
- Clientes: Brasil OTC e Cliente Feitosa

## 📱 Responsividade

O sistema é totalmente responsivo e funciona em:
- Desktop
- Tablet
- Mobile

## 🔒 Segurança

- CORS habilitado
- Validação de parâmetros
- Sanitização de inputs
- Rate limiting recomendado para produção

## 📈 Performance

- Atualização otimizada (5 segundos)
- Cache de cotações
- Requests assíncronos
- Fallback para indisponibilidade da API

## 🚀 Deploy em Produção

Para deploy em produção, recomenda-se:
- Usar Gunicorn como WSGI server
- Nginx como proxy reverso
- SSL/TLS (Let's Encrypt)
- Monitoramento (PM2 ou systemd)

## 📞 Suporte

Sistema desenvolvido para 1A1 Cripto
- Domínio: 1a1cripto.com
- Subdomínio planejado: cotacao.1a1cripto.com

