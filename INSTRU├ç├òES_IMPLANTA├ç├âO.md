# 🚀 Instruções para Implantação Permanente - Automação Mercos Planilha peqpaper

## 📋 Visão Geral

Esta aplicação automatiza o processo de conversão de planilhas de orçamento do Mercos para a Planilha peqpaper, realizando automaticamente:

- Conversão de códigos de barra para códigos Ommie
- Preenchimento automático de quantidades e preços
- Extração e inserção automática do CNPJ
- Geração da Planilha peqpaper no formato correto

## 📦 Conteúdo do Pacote

```
pacote_implantacao/
├── src/                          # Código-fonte da aplicação
│   ├── main.py                   # Arquivo principal da aplicação Flask
│   ├── routes/                   # Rotas da API
│   │   └── mercos_v3.py         # Lógica principal de automação
│   └── static/                   # Interface web
│       └── index.html           # Página principal
├── requirements.txt              # Dependências Python
├── Procfile                     # Configuração para Heroku
├── runtime.txt                  # Versão do Python
├── 16249.xlsx                   # Template da Planilha peqpaper
├── RELAÇÃODEPRODUTOSMAG.xlsx    # Base de dados de produtos
└── INSTRUÇÕES_IMPLANTAÇÃO.md    # Este arquivo
```

## 🛠️ Opções de Hospedagem

### Opção 1: Heroku (Recomendado para iniciantes)

**Vantagens:**
- Gratuito (com limitações)
- Fácil de configurar
- Não requer servidor próprio

**Passos:**

1. **Criar conta no Heroku:**
   - Acesse: https://heroku.com
   - Crie uma conta gratuita

2. **Instalar Heroku CLI:**
   - Windows: Baixe em https://devcenter.heroku.com/articles/heroku-cli
   - Mac: `brew install heroku/brew/heroku`
   - Linux: `curl https://cli-assets.heroku.com/install.sh | sh`

3. **Fazer login:**
   ```bash
   heroku login
   ```

4. **Navegar até o diretório do projeto:**
   ```bash
   cd caminho/para/pacote_implantacao
   ```

5. **Inicializar repositório Git:**
   ```bash
   git init
   git add .
   git commit -m "Aplicação Mercos Automator"
   ```

6. **Criar aplicação no Heroku:**
   ```bash
   heroku create nome-da-sua-aplicacao
   ```

7. **Fazer deploy:**
   ```bash
   git push heroku main
   ```

8. **Abrir aplicação:**
   ```bash
   heroku open
   ```

### Opção 2: VPS/Servidor Próprio

**Vantagens:**
- Controle total
- Sem limitações de uso
- Mais estável

**Requisitos:**
- Servidor com Ubuntu/Debian
- Python 3.8+
- Acesso SSH

**Passos:**

1. **Conectar ao servidor:**
   ```bash
   ssh usuario@ip-do-servidor
   ```

2. **Instalar dependências do sistema:**
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip python3-venv nginx
   ```

3. **Enviar arquivos para o servidor:**
   ```bash
   scp -r pacote_implantacao/ usuario@ip-do-servidor:/home/usuario/
   ```

4. **No servidor, navegar até o diretório:**
   ```bash
   cd /home/usuario/pacote_implantacao
   ```

5. **Criar ambiente virtual:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

6. **Instalar dependências:**
   ```bash
   pip install -r requirements.txt
   pip install gunicorn
   ```

7. **Testar aplicação:**
   ```bash
   python src/main.py
   ```

8. **Configurar Gunicorn (para produção):**
   ```bash
   gunicorn --bind 0.0.0.0:5000 src.main:app
   ```

9. **Configurar Nginx (opcional, para domínio próprio):**
   - Criar arquivo `/etc/nginx/sites-available/mercos-automator`
   - Configurar proxy reverso para porta 5000

### Opção 3: Serviços de Nuvem (AWS, Google Cloud, Azure)

**Para usuários avançados:**
- AWS Elastic Beanstalk
- Google App Engine
- Azure App Service

## 🔧 Configuração Local para Desenvolvimento

1. **Instalar Python 3.8+:**
   - Windows: https://python.org/downloads
   - Mac: `brew install python`
   - Linux: `sudo apt install python3`

2. **Navegar até o diretório:**
   ```bash
   cd pacote_implantacao
   ```

3. **Criar ambiente virtual:**
   ```bash
   python -m venv venv
   ```

4. **Ativar ambiente virtual:**
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`

5. **Instalar dependências:**
   ```bash
   pip install -r requirements.txt
   ```

6. **Executar aplicação:**
   ```bash
   python src/main.py
   ```

7. **Acessar no navegador:**
   ```
   http://localhost:5000
   ```

## 📁 Estrutura dos Arquivos de Dados

### Template da Planilha peqpaper (16249.xlsx)
- **Localização:** Raiz do projeto
- **Função:** Template base para geração das planilhas preenchidas
- **Posições importantes:**
  - D7: CNPJ (preenchido automaticamente)
  - D22 para baixo: Códigos Ommie
  - F22 para baixo: Quantidades
  - G22 para baixo: Preços

### Base de Dados de Produtos (RELAÇÃODEPRODUTOSMAG.xlsx)
- **Localização:** Raiz do projeto
- **Função:** Mapeamento de códigos de barra para códigos Ommie
- **Estrutura:**
  - Coluna A: Código do Produto (Ommie)
  - Coluna E: Código EAN (GTIN) - Código de barras

## 🔄 Como Atualizar a Base de Dados

Para adicionar novos produtos ou atualizar códigos:

1. **Editar o arquivo `RELAÇÃODEPRODUTOSMAG.xlsx`**
2. **Manter a estrutura:**
   - Linha 1: Cabeçalhos
   - Linha 2 em diante: Dados dos produtos
3. **Reiniciar a aplicação** para carregar as alterações

## 🚨 Solução de Problemas

### Erro: "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### Erro: "Permission denied"
```bash
chmod +x src/main.py
```

### Aplicação não carrega
1. Verificar se todas as dependências estão instaladas
2. Verificar se os arquivos de dados estão no local correto
3. Verificar logs de erro

### Problemas com pandas/numpy
Se houver problemas com essas bibliotecas:
```bash
pip uninstall pandas numpy
pip install pandas==2.0.3 numpy==1.24.3
```

## 📞 Suporte

Para problemas técnicos:
1. Verificar logs de erro da aplicação
2. Confirmar que todos os arquivos estão no local correto
3. Testar localmente antes de fazer deploy

## 🔒 Segurança

**Recomendações:**
- Usar HTTPS em produção
- Configurar firewall adequadamente
- Manter dependências atualizadas
- Fazer backup regular dos dados

## 📈 Monitoramento

**Métricas importantes:**
- Tempo de resposta da aplicação
- Taxa de sucesso no processamento
- Uso de recursos (CPU/memória)

## 🔄 Atualizações Futuras

Para atualizar a aplicação:
1. Substituir arquivos do código-fonte
2. Atualizar requirements.txt se necessário
3. Reiniciar aplicação
4. Testar funcionalidade

---

**Desenvolvido por:** Manus AI  
**Versão:** 1.0  
**Data:** Julho 2025

