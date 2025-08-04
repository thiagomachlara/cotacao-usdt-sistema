# 🚀 Guia Completo: cotacao.1a1cripto.com no AWS

Este guia te levará do zero até ter seu sistema rodando em `cotacao.1a1cripto.com` de forma profissional.

## 📋 Pré-requisitos

✅ Domínio 1a1cripto.com gerenciado no Route 53  
✅ Instância EC2 com IP Elástico  
✅ Conta GitHub  
✅ Acesso SSH à instância  

---

## 🎯 ETAPA 1: Preparar GitHub

### 1.1 Criar Repositório
1. Acesse [github.com](https://github.com)
2. Clique em **"New repository"**
3. Nome: `cotacao-usdt-sistema`
4. Descrição: `Sistema de Cotação USDT/BRL com Billboard Público`
5. ✅ Marque **"Add a README file"**
6. Clique **"Create repository"**

### 1.2 Upload dos Arquivos
1. Na página do repositório, clique **"uploading an existing file"**
2. Arraste o arquivo ZIP que vou te enviar
3. Commit message: `Sistema inicial de cotação`
4. Clique **"Commit changes"**

---

## ⚙️ ETAPA 2: Configurar AWS Route 53

### 2.1 Criar Subdomínio
1. Acesse **Route 53** no console AWS
2. Clique em **"Hosted zones"**
3. Clique no domínio **1a1cripto.com**
4. Clique **"Create record"**
5. Configure:
   - **Record name**: `cotacao`
   - **Record type**: `A`
   - **Value**: `SEU-IP-ELASTICO`
   - **TTL**: `300`
6. Clique **"Create records"**

### 2.2 Verificar DNS
```bash
# Teste no terminal (pode demorar alguns minutos)
nslookup cotacao.1a1cripto.com
```

---

## 🔒 ETAPA 3: Security Groups

### 3.1 Liberar Portas
1. Acesse **EC2** → **Security Groups**
2. Selecione o Security Group da sua instância
3. Clique **"Edit inbound rules"**
4. Adicione as regras:

| Type | Protocol | Port Range | Source | Description |
|------|----------|------------|--------|-------------|
| HTTP | TCP | 80 | 0.0.0.0/0 | Web HTTP |
| HTTPS | TCP | 443 | 0.0.0.0/0 | Web HTTPS |
| Custom TCP | TCP | 5001 | 0.0.0.0/0 | Flask App |

5. Clique **"Save rules"**

---

## 🖥️ ETAPA 4: Configurar Instância EC2

### 4.1 Conectar na Instância
```bash
ssh -i sua-chave.pem ubuntu@SEU-IP-ELASTICO
```

### 4.2 Atualizar Sistema
```bash
sudo apt update && sudo apt upgrade -y
```

### 4.3 Instalar Dependências
```bash
# Python e pip
sudo apt install python3 python3-pip python3-venv -y

# Nginx
sudo apt install nginx -y

# Git
sudo apt install git -y

# Certbot para SSL
sudo apt install certbot python3-certbot-nginx -y
```

---

## 📦 ETAPA 5: Deploy da Aplicação

### 5.1 Clonar Repositório
```bash
cd /home/ubuntu
git clone https://github.com/SEU-USUARIO/cotacao-usdt-sistema.git
cd cotacao-usdt-sistema
```

### 5.2 Configurar Ambiente Python
```bash
# Criar ambiente virtual
python3 -m venv venv

# Ativar ambiente
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

### 5.3 Testar Aplicação
```bash
# Executar em modo teste
python src/main.py

# Em outro terminal, teste:
curl http://localhost:5001/api/cotacoes-rapidas
```

Se retornar JSON com cotações, está funcionando! ✅

---

## 🌐 ETAPA 6: Configurar Nginx

### 6.1 Criar Configuração
```bash
sudo nano /etc/nginx/sites-available/cotacao.1a1cripto.com
```

### 6.2 Adicionar Conteúdo
```nginx
server {
    listen 80;
    server_name cotacao.1a1cripto.com;

    location / {
        proxy_pass http://127.0.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support (se necessário no futuro)
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

### 6.3 Ativar Site
```bash
# Criar link simbólico
sudo ln -s /etc/nginx/sites-available/cotacao.1a1cripto.com /etc/nginx/sites-enabled/

# Testar configuração
sudo nginx -t

# Reiniciar nginx
sudo systemctl restart nginx
```

---

## 🔐 ETAPA 7: SSL/HTTPS

### 7.1 Obter Certificado
```bash
sudo certbot --nginx -d cotacao.1a1cripto.com
```

### 7.2 Configurar Renovação Automática
```bash
# Testar renovação
sudo certbot renew --dry-run

# Adicionar ao crontab
sudo crontab -e

# Adicionar linha:
0 12 * * * /usr/bin/certbot renew --quiet
```

---

## 🔄 ETAPA 8: Processo em Background

### 8.1 Criar Serviço Systemd
```bash
sudo nano /etc/systemd/system/cotacao-usdt.service
```

### 8.2 Conteúdo do Serviço
```ini
[Unit]
Description=Sistema de Cotacao USDT/BRL
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/cotacao-usdt-sistema
Environment=PATH=/home/ubuntu/cotacao-usdt-sistema/venv/bin
ExecStart=/home/ubuntu/cotacao-usdt-sistema/venv/bin/python src/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 8.3 Ativar Serviço
```bash
# Recarregar systemd
sudo systemctl daemon-reload

# Ativar serviço
sudo systemctl enable cotacao-usdt

# Iniciar serviço
sudo systemctl start cotacao-usdt

# Verificar status
sudo systemctl status cotacao-usdt
```

---

## 🎉 ETAPA 9: Testar Tudo

### 9.1 URLs para Testar
- ✅ https://cotacao.1a1cripto.com/
- ✅ https://cotacao.1a1cripto.com/billboard
- ✅ https://cotacao.1a1cripto.com/billboard?spread=1.007

### 9.2 Comandos de Monitoramento
```bash
# Ver logs da aplicação
sudo journalctl -u cotacao-usdt -f

# Status do nginx
sudo systemctl status nginx

# Status da aplicação
sudo systemctl status cotacao-usdt

# Verificar portas abertas
sudo netstat -tlnp | grep :80
sudo netstat -tlnp | grep :5001
```

---

## 🔧 ETAPA 10: Manutenção

### 10.1 Atualizar Sistema
```bash
cd /home/ubuntu/cotacao-usdt-sistema
git pull origin main
sudo systemctl restart cotacao-usdt
```

### 10.2 Backup
```bash
# Backup do código
tar -czf backup-cotacao-$(date +%Y%m%d).tar.gz cotacao-usdt-sistema/

# Backup do banco (se necessário)
cp cotacao-usdt-sistema/src/database/app.db backup-db-$(date +%Y%m%d).db
```

### 10.3 Logs Importantes
```bash
# Logs da aplicação
sudo journalctl -u cotacao-usdt --since "1 hour ago"

# Logs do nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

---

## ⚠️ Troubleshooting

### Problema: Site não carrega
```bash
# Verificar se aplicação está rodando
sudo systemctl status cotacao-usdt

# Verificar nginx
sudo systemctl status nginx

# Testar aplicação diretamente
curl http://localhost:5001/api/cotacoes-rapidas
```

### Problema: SSL não funciona
```bash
# Renovar certificado
sudo certbot renew

# Verificar configuração nginx
sudo nginx -t
```

### Problema: DNS não resolve
```bash
# Verificar configuração Route 53
nslookup cotacao.1a1cripto.com

# Aguardar propagação (até 48h)
```

---

## 🎯 Resultado Final

Após seguir todos os passos, você terá:

✅ **https://cotacao.1a1cripto.com/** - Sistema principal  
✅ **https://cotacao.1a1cripto.com/billboard** - Billboard público  
✅ **https://cotacao.1a1cripto.com/billboard?spread=1.007** - Com spread  
✅ **SSL/HTTPS** automático  
✅ **Renovação automática** de certificados  
✅ **Processo em background** com restart automático  
✅ **Logs** organizados  
✅ **Backup** configurado  

**Tempo estimado total: 30-45 minutos** ⏱️

---

## 📞 Suporte

Se algo der errado, me mande:
1. Output dos comandos de status
2. Logs de erro
3. Screenshot do problema

**Vamos fazer funcionar!** 🚀

