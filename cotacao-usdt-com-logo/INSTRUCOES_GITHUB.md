# 📋 Instruções para GitHub - cotacao.1a1cripto.com

## 🎯 Passo 1: Criar Repositório

1. Acesse [github.com](https://github.com) e faça login
2. Clique no botão **"New"** (verde) ou **"+"** no canto superior direito
3. Selecione **"New repository"**

## ⚙️ Passo 2: Configurar Repositório

**Preencha os campos:**
- **Repository name**: `cotacao-usdt-sistema`
- **Description**: `Sistema de Cotação USDT/BRL com Billboard Público para 1A1 Cripto`
- ✅ **Public** (deixe marcado)
- ✅ **Add a README file** (marque esta opção)
- **Add .gitignore**: `Python` (selecione na lista)
- **Choose a license**: `MIT License` (opcional)

Clique **"Create repository"**

## 📦 Passo 3: Upload dos Arquivos

### Opção A: Via Interface Web (Mais Fácil)
1. Na página do seu repositório, clique **"uploading an existing file"**
2. Arraste o arquivo `cotacao-usdt-completo.zip` que te enviei
3. **OU** clique "choose your files" e selecione o ZIP
4. Na caixa de commit:
   - **Commit message**: `Sistema inicial de cotação USDT/BRL`
   - **Description**: `Inclui billboard público, API, documentação e guia AWS`
5. Clique **"Commit changes"**

### Opção B: Via Git (Se souber usar)
```bash
# Clonar seu repositório
git clone https://github.com/SEU-USUARIO/cotacao-usdt-sistema.git
cd cotacao-usdt-sistema

# Extrair arquivos do ZIP
unzip ../cotacao-usdt-completo.zip

# Adicionar arquivos
git add .
git commit -m "Sistema inicial de cotação USDT/BRL"
git push origin main
```

## 🔗 Passo 4: Obter Link do Repositório

Após criar, você terá um link como:
`https://github.com/SEU-USUARIO/cotacao-usdt-sistema`

**Guarde este link!** Você usará no AWS.

## 📝 Passo 5: Editar README (Opcional)

1. Clique no arquivo `README.md` no seu repositório
2. Clique no ícone de lápis (Edit)
3. Adicione informações personalizadas:

```markdown
# Sistema de Cotação USDT/BRL - 1A1 Cripto

Sistema profissional de cotação com billboard público.

## 🌐 URLs de Produção
- Sistema: https://cotacao.1a1cripto.com/
- Billboard: https://cotacao.1a1cripto.com/billboard

## 🚀 Funcionalidades
- Cotações em tempo real (5 segundos)
- Billboard público controlável via URL
- Clientes pré-cadastrados
- Design responsivo

## 📊 Exemplos de Billboard
- Sem spread: https://cotacao.1a1cripto.com/billboard
- Com 0.7%: https://cotacao.1a1cripto.com/billboard?spread=1.007
- Com 1.5%: https://cotacao.1a1cripto.com/billboard?spread=1.015
```

4. Clique **"Commit changes"**

## ✅ Verificação

Seu repositório deve ter:
- ✅ Código fonte completo
- ✅ Dockerfile
- ✅ requirements.txt
- ✅ README.md
- ✅ Guia AWS completo
- ✅ .gitignore configurado

## 🔄 Próximos Passos

Após criar o repositório:
1. **Copie o link** do repositório
2. **Substitua** `SEU-USUARIO` no guia AWS pelo seu username
3. **Siga o guia AWS** que te enviei

## 📞 Dúvidas?

Se tiver problemas:
1. Tire screenshot da tela
2. Me mande o link do repositório
3. Descreva o erro

**Vamos fazer funcionar!** 🚀

---

**Próximo passo**: Seguir o `GUIA_AWS_COMPLETO.md` para configurar o servidor.

