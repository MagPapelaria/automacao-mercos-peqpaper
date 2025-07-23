# 📖 Manual de Uso - Automação Mercos Planilha peqpaper

## 🎯 Como Usar a Aplicação

### Passo a Passo

1. **Acessar a aplicação** no navegador (URL fornecida após implantação)

2. **Fazer upload da planilha de orçamento do Mercos:**
   - Clicar em "Escolher arquivo" ou arrastar o arquivo para a área indicada
   - Selecionar o arquivo .xlsx exportado do Mercos

3. **Clicar em "Gerar Planilha peqpaper"**

4. **Aguardar o processamento** (alguns segundos)

5. **Download automático** da Planilha peqpaper preenchida

### 📊 O que a Aplicação Faz

**Entrada:**
- Planilha de orçamento exportada do Mercos (.xlsx)

**Processamento:**
- Extrai códigos de barra, quantidades e preços da planilha do Mercos
- Converte códigos de barra em códigos Ommie usando a base de dados
- Extrai o CNPJ da planilha de orçamento
- Preenche o template da Planilha peqpaper nas posições corretas

**Saída:**
- Planilha peqpaper completamente preenchida (.xlsx)
- Relatório de processamento (quantos produtos foram encontrados)

### 📍 Posições na Planilha peqpaper

- **D7:** CNPJ (extraído automaticamente do orçamento)
- **D22 para baixo:** Códigos Ommie
- **F22 para baixo:** Quantidades
- **G22 para baixo:** Preços

### ✅ Relatório de Processamento

Após o processamento, a aplicação mostra:
- Total de produtos no orçamento
- Produtos encontrados na base de dados
- Taxa de sucesso
- Lista de produtos não encontrados (se houver)

### 🔄 Atualizando a Base de Dados

Para adicionar novos produtos:

1. **Editar o arquivo `RELAÇÃODEPRODUTOSMAG.xlsx`**
2. **Adicionar novos produtos:**
   - Coluna A: Código Ommie
   - Coluna E: Código de barras (EAN/GTIN)
3. **Reiniciar a aplicação** para carregar as alterações

### 🚨 Problemas e Soluções

**Produto não encontrado:**
- Verificar se o código de barras está na base de dados
- Adicionar o produto na planilha `RELAÇÃODEPRODUTOSMAG.xlsx`

**Erro no upload:**
- Verificar se o arquivo é .xlsx
- Verificar se o arquivo não está corrompido
- Tentar novamente

**CNPJ não preenchido:**
- Verificar se o CNPJ está presente na planilha de orçamento do Mercos
- O CNPJ deve estar em formato numérico (apenas números)

### 📋 Formato da Planilha de Orçamento do Mercos

A aplicação espera que a planilha do Mercos tenha:
- **Linha 5 em diante:** Dados dos produtos
- **Coluna B:** Códigos de barra
- **Coluna D:** Quantidades
- **Coluna HI:** Preços
- **CNPJ:** Em qualquer lugar da planilha (formato numérico)

### 💡 Dicas de Uso

1. **Mantenha a base de dados atualizada** com novos produtos
2. **Faça backup** da base de dados regularmente
3. **Teste com uma planilha pequena** primeiro
4. **Verifique o relatório** de processamento para identificar produtos não encontrados

### 🔒 Segurança dos Dados

- Os arquivos são processados temporariamente
- Nenhum dado é armazenado permanentemente no servidor
- Os arquivos são deletados após o processamento

---

**📞 Suporte:** Em caso de dúvidas, consulte as instruções técnicas ou entre em contato com o responsável pela implantação.

