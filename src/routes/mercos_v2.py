from flask import Blueprint, request, jsonify, send_file
import pandas as pd
import os
import tempfile
from werkzeug.utils import secure_filename

mercos_v2_bp = Blueprint('mercos_v2', __name__)

# Carregar a base de dados de produtos uma vez quando o módulo é importado
BASE_PRODUTOS_PATH = "RELACAODEPRODUTOSMAG.xlsx"

def carregar_base_produtos():
    """Carrega a base de dados de produtos e cria o mapeamento EAN -> Código Ommie"""
    try:
        df_produtos = pd.read_excel(BASE_PRODUTOS_PATH, header=1)
        
        # Limpar dados nulos e criar mapeamento
        df_produtos = df_produtos.dropna(subset=['Código EAN (GTIN)', 'Código do Produto'])
        
        # Converter códigos EAN para string para evitar problemas de tipo
        df_produtos['Código EAN (GTIN)'] = df_produtos['Código EAN (GTIN)'].astype(str)
        df_produtos['Código do Produto'] = df_produtos['Código do Produto'].astype(str)
        
        # Criar dicionário de mapeamento: EAN -> Código Ommie
        mapeamento = dict(zip(df_produtos['Código EAN (GTIN)'], df_produtos['Código do Produto']))
        
        return mapeamento, len(df_produtos)
    except Exception as e:
        print(f"Erro ao carregar base de produtos: {e}")
        return {}, 0

# Carregar a base de produtos na inicialização
MAPEAMENTO_EAN_OMMIE, TOTAL_PRODUTOS = carregar_base_produtos()

@mercos_v2_bp.route('/automatizar-completo', methods=['POST'])
def automatizar_mercos_completo():
    try:
        # Verificar se o arquivo foi enviado
        if 'orcamento' not in request.files:
            return jsonify({'error': 'Arquivo de orçamento é obrigatório'}), 400
        
        orcamento_file = request.files['orcamento']
        
        if orcamento_file.filename == '':
            return jsonify({'error': 'Nenhum arquivo foi selecionado'}), 400
        
        # Verificar se a base de produtos foi carregada
        if not MAPEAMENTO_EAN_OMMIE:
            return jsonify({'error': 'Base de dados de produtos não encontrada'}), 500
        
        # Criar diretório temporário para processar os arquivos
        with tempfile.TemporaryDirectory() as temp_dir:
            # Salvar arquivo temporariamente
            orcamento_path = os.path.join(temp_dir, secure_filename(orcamento_file.filename))
            saida_path = os.path.join(temp_dir, 'planilha_16249_automatizada.xlsx')
            
            orcamento_file.save(orcamento_path)
            
            # Processar a planilha de orçamento
            # Carregar o orçamento (pular as primeiras 4 linhas para começar da linha 5)
            df_orcamento = pd.read_excel(orcamento_path, header=None, skiprows=4)
            
            # Renomear as colunas: B=1, D=3, H=7
            df_orcamento.rename(columns={1: 'CODIGO_BARRAS', 3: 'QUANTIDADE', 7: 'PRECO'}, inplace=True)
            
            # Filtrar apenas as colunas relevantes e remover linhas vazias
            df_orcamento = df_orcamento[['CODIGO_BARRAS', 'QUANTIDADE', 'PRECO']].dropna(subset=['CODIGO_BARRAS'])
            
            # Converter códigos de barra para string para garantir compatibilidade
            # CORREÇÃO: Primeiro converter para int64 para remover decimais, depois para string
            df_orcamento['CODIGO_BARRAS'] = df_orcamento['CODIGO_BARRAS'].astype('int64').astype(str)
            
            # Mapear códigos de barra para códigos Ommie usando a base de dados
            df_orcamento['CODIGO_OMMIE'] = df_orcamento['CODIGO_BARRAS'].map(MAPEAMENTO_EAN_OMMIE)
            
            # Verificar quantos produtos foram encontrados
            produtos_encontrados = df_orcamento['CODIGO_OMMIE'].notna().sum()
            total_produtos_orcamento = len(df_orcamento)
            produtos_nao_encontrados = df_orcamento[df_orcamento['CODIGO_OMMIE'].isna()]
            
            # Criar planilha final com as colunas na ordem correta
            df_final = df_orcamento[['CODIGO_OMMIE', 'QUANTIDADE', 'PRECO']].copy()
            
            # Renomear colunas para ficar mais claro
            df_final.columns = ['Código Ommie', 'Quantidade', 'Preço']
            
            # Salvar resultado
            df_final.to_excel(saida_path, index=False)
            
            # Preparar informações de retorno
            info_processamento = {
                'total_produtos_orcamento': total_produtos_orcamento,
                'produtos_encontrados': produtos_encontrados,
                'produtos_nao_encontrados': total_produtos_orcamento - produtos_encontrados,
                'taxa_sucesso': f"{(produtos_encontrados/total_produtos_orcamento)*100:.1f}%",
                'base_produtos_total': TOTAL_PRODUTOS
            }
            
            # Se houver produtos não encontrados, incluir a lista
            if len(produtos_nao_encontrados) > 0:
                codigos_nao_encontrados = produtos_nao_encontrados['CODIGO_BARRAS'].tolist()
                info_processamento['codigos_nao_encontrados'] = codigos_nao_encontrados[:10]  # Limitar a 10 para não sobrecarregar
            
            # Adicionar informações como comentário no cabeçalho da resposta
            response = send_file(saida_path, as_attachment=True, download_name='planilha_16249_automatizada.xlsx')
            response.headers['X-Processing-Info'] = str(info_processamento)
            
            return response
            
    except Exception as e:
        return jsonify({'error': f'Erro ao processar arquivo: {str(e)}'}), 500

@mercos_v2_bp.route('/status-base', methods=['GET'])
def status_base():
    """Retorna informações sobre a base de dados de produtos"""
    return jsonify({
        'status': 'Base de dados carregada',
        'total_produtos': TOTAL_PRODUTOS,
        'base_carregada': len(MAPEAMENTO_EAN_OMMIE) > 0
    })

@mercos_v2_bp.route('/verificar-codigo', methods=['POST'])
def verificar_codigo():
    """Verifica se um código de barras específico existe na base"""
    data = request.get_json()
    codigo_barras = str(data.get('codigo_barras', ''))
    
    if codigo_barras in MAPEAMENTO_EAN_OMMIE:
        return jsonify({
            'encontrado': True,
            'codigo_ommie': MAPEAMENTO_EAN_OMMIE[codigo_barras]
        })
    else:
        return jsonify({
            'encontrado': False,
            'codigo_ommie': None
        })

