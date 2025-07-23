from flask import Blueprint, request, jsonify, send_file
import pandas as pd
import os
import tempfile
from werkzeug.utils import secure_filename

mercos_bp = Blueprint('mercos', __name__)

@mercos_bp.route('/automatizar', methods=['POST'])
def automatizar_mercos():
    try:
        # Verificar se os arquivos foram enviados
        if 'orcamento' not in request.files or 'exportacao' not in request.files:
            return jsonify({'error': 'Arquivos de orçamento e exportação são obrigatórios'}), 400
        
        orcamento_file = request.files['orcamento']
        exportacao_file = request.files['exportacao']
        
        if orcamento_file.filename == '' or exportacao_file.filename == '':
            return jsonify({'error': 'Nenhum arquivo foi selecionado'}), 400
        
        # Criar diretório temporário para processar os arquivos
        with tempfile.TemporaryDirectory() as temp_dir:
            # Salvar arquivos temporariamente
            orcamento_path = os.path.join(temp_dir, secure_filename(orcamento_file.filename))
            exportacao_path = os.path.join(temp_dir, secure_filename(exportacao_file.filename))
            saida_path = os.path.join(temp_dir, 'resultado_automatizado.xlsx')
            
            orcamento_file.save(orcamento_path)
            exportacao_file.save(exportacao_path)
            
            # Processar as planilhas
            # Carregar o orçamento (pular as primeiras 4 linhas para começar da linha 5)
            df_orcamento = pd.read_excel(orcamento_path, header=None, skiprows=4)
            
            # Renomear as colunas: B=1, D=3, H=7
            df_orcamento.rename(columns={1: 'CODIGO_BARRAS', 3: 'QUANTIDADE', 7: 'PRECO'}, inplace=True)
            
            # Filtrar apenas as colunas relevantes e remover linhas vazias
            df_orcamento = df_orcamento[['CODIGO_BARRAS', 'QUANTIDADE', 'PRECO']].dropna(subset=['CODIGO_BARRAS'])
            
            # Carregar a planilha de exportação (mapeamento)
            df_exportacao = pd.read_excel(exportacao_path, header=None)
            
            # Renomear as colunas: A=0 (CODIGO_OMMIE), B=1 (CODIGO_BARRAS)
            df_exportacao.rename(columns={0: 'CODIGO_OMMIE', 1: 'CODIGO_BARRAS'}, inplace=True)
            
            # Remover a primeira linha (cabeçalhos) e linhas vazias
            df_exportacao = df_exportacao.iloc[1:].copy()
            df_exportacao.dropna(subset=['CODIGO_BARRAS', 'CODIGO_OMMIE'], inplace=True)
            
            # Criar dicionário de mapeamento
            mapeamento_omnie = dict(zip(df_exportacao['CODIGO_BARRAS'], df_exportacao['CODIGO_OMMIE']))
            
            # Mapear códigos de barra para códigos Ommie
            df_orcamento['CODIGO_OMMIE'] = df_orcamento['CODIGO_BARRAS'].map(mapeamento_omnie)
            
            # Criar planilha final
            df_final = df_orcamento[['CODIGO_OMMIE', 'QUANTIDADE', 'PRECO']]
            
            # Salvar resultado
            df_final.to_excel(saida_path, index=False)
            
            # Retornar o arquivo para download
            return send_file(saida_path, as_attachment=True, download_name='resultado_automatizado.xlsx')
            
    except Exception as e:
        return jsonify({'error': f'Erro ao processar arquivos: {str(e)}'}), 500

@mercos_bp.route('/status', methods=['GET'])
def status():
    return jsonify({'status': 'Automação Mercos funcionando!'})

