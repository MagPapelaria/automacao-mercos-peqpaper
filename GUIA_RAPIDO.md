# ⚡ Guia Rápido - Implantação em 10 Minutos

## 🎯 Para quem tem pressa

### Opção Mais Rápida: Heroku

1. **Criar conta:** https://heroku.com (gratuito)

2. **Baixar Heroku CLI:** https://devcenter.heroku.com/articles/heroku-cli

3. **Abrir terminal/prompt de comando no diretório do projeto**

4. **Executar comandos:**
   ```bash
   heroku login
   git init
   git add .
   git commit -m "Deploy inicial"
   heroku create sua-aplicacao-mercos
   git push heroku main
   heroku open
   ```

5. **Pronto!** Sua aplicação estará online

### Opção Mais Simples: Servidor Local

1. **Instalar Python:** https://python.org/downloads

2. **Abrir terminal no diretório do projeto**

3. **Executar:**
   ```bash
   pip install -r requirements.txt
   python src/main.py
   ```

4. **Acessar:** http://localhost:5000

## 🆘 Problemas Comuns

**Erro de dependências:**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Aplicação não abre:**
- Verificar se Python está instalado
- Verificar se está no diretório correto
- Verificar se os arquivos .xlsx estão presentes

## 📞 Precisa de Ajuda?

1. Ler `INSTRUÇÕES_IMPLANTAÇÃO.md` (completo)
2. Verificar se todos os arquivos estão presentes
3. Testar localmente primeiro

---

**⏱️ Tempo estimado:** 5-15 minutos  
**💰 Custo:** Gratuito (Heroku) ou R$ 20-50/mês (servidor próprio)

