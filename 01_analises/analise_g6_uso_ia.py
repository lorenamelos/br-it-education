"""
ANÁLISE ABA G6 - USO DE IA GENERATIVA POR ALUNOS
TIC Educação 2024
"""

import pandas as pd
import numpy as np
import json
from pathlib import Path


def analisar_g6_uso_ia(arquivo, aba_nome='G6'):
    """
    Analisa a aba G6 - Uso de IA Generativa por alunos
    """
    print(f"\n{'='*80}")
    print(f"ANÁLISE ABA {aba_nome} - USO DE IA GENERATIVA POR ALUNOS")
    print(f"{'='*80}\n")
    
    # Carregar TODA a planilha
    print(f"📂 Carregando aba {aba_nome}...")
    df_raw = pd.read_excel(arquivo, sheet_name=aba_nome, header=None)
    
    print(f"✅ Arquivo carregado: {df_raw.shape[0]} linhas x {df_raw.shape[1]} colunas\n")
    
    # Encontrar colunas de IA
    linha_cabecalho = df_raw.iloc[2]
    colunas_ia = []
    for i, valor in enumerate(linha_cabecalho):
        if pd.notna(valor) and 'Inteligência Artificial' in str(valor):
            colunas_ia.append(i)
    
    if len(colunas_ia) == 0:
        raise ValueError("Colunas de IA não encontradas!")
    
    col_sim = colunas_ia[0]
    col_nao = colunas_ia[1]
    
    print(f"🔍 Colunas de IA encontradas:")
    print(f"  • Coluna {col_sim}: Usam IA (Sim)")
    print(f"  • Coluna {col_nao}: Não usam IA (Não)\n")
    
    # Criar DataFrame de dados
    df = df_raw.iloc[4:].copy()
    df.columns = range(len(df.columns))
    df = df.reset_index(drop=True)
    df = df.rename(columns={0: 'categoria', 1: 'subcategoria'})
    
    # Converter colunas numéricas
    for col in df.columns[2:]:
        df[col] = pd.to_numeric(
            df[col].astype(str).str.replace(',', '').str.replace('-', ''), 
            errors='coerce'
        )
    
    # Limpar
    df = df.dropna(subset=['categoria'])
    df = df[~df['categoria'].str.contains('Fonte:', na=False)]
    
    print(f"✅ {len(df)} linhas de dados carregadas\n")
    
    # TOTAL BRASIL
    linha_total = df[df['categoria'] == 'TOTAL'].iloc[0]
    
    usam_ia = linha_total[col_sim]
    nao_usam_ia = linha_total[col_nao]
    total = usam_ia + nao_usam_ia
    pct_usam = (usam_ia / total) * 100
    pct_nao_usam = (nao_usam_ia / total) * 100
    
    print(f"🇧🇷 BRASIL - USO DE IA GENERATIVA:")
    print(f"  Total de alunos: {total:,.0f}")
    print(f"  ✅ USAM IA: {usam_ia:,.0f} ({pct_usam:.1f}%)")
    print(f"  ❌ NÃO USAM IA: {nao_usam_ia:,.0f} ({pct_nao_usam:.1f}%)")
    
    # REGIÕES
    regiao = df[df['categoria'] == 'REGIÃO'].copy()
    regiao_data = []
    
    if len(regiao) > 0:
        print(f"\n📍 POR REGIÃO:")
        for _, row in regiao.iterrows():
            nome = row['subcategoria']
            usam = row[col_sim]
            nao_usam = row[col_nao]
            total_grupo = usam + nao_usam
            pct = (usam / total_grupo * 100) if total_grupo > 0 else 0
            
            print(f"  {nome}: {usam:,.0f} usam ({pct:.1f}%)")
            
            regiao_data.append({
                'regiao': nome,
                'usam_ia': int(usam),
                'nao_usam': int(nao_usam),
                'total': int(total_grupo),
                'percentual': round(pct, 1)
            })
    
    # ETAPA DE ENSINO
    etapa = df[df['categoria'] == 'ETAPA DE ENSINO'].copy()
    etapa_data = []
    
    if len(etapa) > 0:
        print(f"\n📚 POR ETAPA DE ENSINO:")
        for _, row in etapa.iterrows():
            nome = row['subcategoria']
            usam = row[col_sim]
            nao_usam = row[col_nao]
            total_grupo = usam + nao_usam
            pct = (usam / total_grupo * 100) if total_grupo > 0 else 0
            
            print(f"  {nome}: {usam:,.0f} usam ({pct:.1f}%)")
            
            etapa_data.append({
                'etapa': nome,
                'usam_ia': int(usam),
                'nao_usam': int(nao_usam),
                'total': int(total_grupo),
                'percentual': round(pct, 1)
            })
    
    # FAIXA ETÁRIA
    faixa_etaria = df[df['categoria'] == 'FAIXA ETÁRIA'].copy()
    faixa_etaria_data = []
    
    if len(faixa_etaria) > 0:
        print(f"\n📅 POR FAIXA ETÁRIA:")
        for _, row in faixa_etaria.iterrows():
            nome = row['subcategoria']
            usam = row[col_sim]
            nao_usam = row[col_nao]
            total_grupo = usam + nao_usam
            pct = (usam / total_grupo * 100) if total_grupo > 0 else 0
            
            print(f"  {nome}: {usam:,.0f} usam ({pct:.1f}%)")
            
            faixa_etaria_data.append({
                'faixa_etaria': nome,
                'usam_ia': int(usam),
                'nao_usam': int(nao_usam),
                'total': int(total_grupo),
                'percentual': round(pct, 1)
            })
    
    # SEXO
    sexo = df[df['categoria'] == 'SEXO'].copy()
    sexo_data = []
    
    if len(sexo) > 0:
        print(f"\n👥 POR SEXO:")
        for _, row in sexo.iterrows():
            nome = row['subcategoria']
            usam = row[col_sim]
            nao_usam = row[col_nao]
            total_grupo = usam + nao_usam
            pct = (usam / total_grupo * 100) if total_grupo > 0 else 0
            
            print(f"  {nome}: {usam:,.0f} usam ({pct:.1f}%)")
            
            sexo_data.append({
                'sexo': nome,
                'usam_ia': int(usam),
                'nao_usam': int(nao_usam),
                'total': int(total_grupo),
                'percentual': round(pct, 1)
            })
    
    # Consolidar resultados
    resultados = {
        'aba': aba_nome,
        'indicador': 'Uso de IA Generativa (ChatGPT, Copilot, Gemini) em Pesquisas Escolares',
        'fonte': 'TIC Educação 2024 - Alunos',
        'brasil': {
            'total_alunos': int(total),
            'usam_ia': int(usam_ia),
            'nao_usam': int(nao_usam_ia),
            'percentual': round(pct_usam, 1)
        },
        'etapas': etapa_data,
        'regioes': regiao_data,
        'faixa_etaria': faixa_etaria_data,
        'sexo': sexo_data
    }
    
    return resultados


def salvar_resultados(resultados, output_dir='./resultados'):
    """
    Salva resultados em JSON e CSV
    """
    Path(output_dir).mkdir(exist_ok=True)
    
    print(f"\n{'='*80}")
    print("SALVANDO RESULTADOS")
    print(f"{'='*80}\n")
    
    # JSON completo
    json_path = f"{output_dir}/g6_uso_ia_completo.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(resultados, f, ensure_ascii=False, indent=2)
    print(f"✅ JSON completo salvo: {json_path}")
    
    # CSV do Brasil
    df_brasil = pd.DataFrame([resultados['brasil']])
    csv_brasil_path = f"{output_dir}/g6_brasil.csv"
    df_brasil.to_csv(csv_brasil_path, index=False, encoding='utf-8-sig')
    print(f"✅ CSV Brasil salvo: {csv_brasil_path}")
    
    # CSV das regiões
    if resultados['regioes']:
        df_regioes = pd.DataFrame(resultados['regioes'])
        csv_regioes_path = f"{output_dir}/g6_regioes.csv"
        df_regioes.to_csv(csv_regioes_path, index=False, encoding='utf-8-sig')
        print(f"✅ CSV Regiões salvo: {csv_regioes_path}")
    
    # CSV etapas de ensino
    if resultados['etapas']:
        df_etapas = pd.DataFrame(resultados['etapas'])
        csv_etapas_path = f"{output_dir}/g6_etapas.csv"
        df_etapas.to_csv(csv_etapas_path, index=False, encoding='utf-8-sig')
        print(f"✅ CSV Etapas salvo: {csv_etapas_path}")
    
    # CSV faixa etária
    if resultados['faixa_etaria']:
        df_faixa = pd.DataFrame(resultados['faixa_etaria'])
        csv_faixa_path = f"{output_dir}/g6_faixa_etaria.csv"
        df_faixa.to_csv(csv_faixa_path, index=False, encoding='utf-8-sig')
        print(f"✅ CSV Faixa Etária salvo: {csv_faixa_path}")
    
    # CSV sexo
    if resultados['sexo']:
        df_sexo = pd.DataFrame(resultados['sexo'])
        csv_sexo_path = f"{output_dir}/g6_sexo.csv"
        df_sexo.to_csv(csv_sexo_path, index=False, encoding='utf-8-sig')
        print(f"✅ CSV Sexo salvo: {csv_sexo_path}")
    
    return {
        'json': json_path,
        'csv_brasil': csv_brasil_path,
        'csv_etapas': csv_etapas_path if resultados['etapas'] else None,
        'csv_regioes': csv_regioes_path if resultados['regioes'] else None,
        'csv_faixa_etaria': csv_faixa_path if resultados['faixa_etaria'] else None,
        'csv_sexo': csv_sexo_path if resultados['sexo'] else None
    }


if __name__ == "__main__":
    arquivo = 'tic_educacao_2024_alunos_tabela_total_v1.0.xlsx'
    
    try:
        # Executar análise
        resultados = analisar_g6_uso_ia(arquivo, aba_nome='G6')
        
        # SALVAR RESULTADOS (esta linha é ESSENCIAL!)
        arquivos_gerados = salvar_resultados(resultados)
        
        print(f"\n{'='*80}")
        print("✅ ANÁLISE G6 CONCLUÍDA!")
        print(f"{'='*80}")
        print(f"\n📊 Resultado principal:")
        print(f"  • {resultados['brasil']['percentual']:.1f}% dos alunos USAM IA generativa")
        
        if resultados['etapas']:
            print(f"\n📚 Por etapa de ensino:")
            for etapa in resultados['etapas']:
                print(f"  • {etapa['etapa']}: {etapa['percentual']:.1f}%")
        
        if resultados['faixa_etaria']:
            print(f"\n📅 Por faixa etária:")
            for faixa in resultados['faixa_etaria']:
                print(f"  • {faixa['faixa_etaria']}: {faixa['percentual']:.1f}%")
        
        if resultados['regioes']:
            print(f"\n📍 Por região:")
            for regiao in resultados['regioes']:
                print(f"  • {regiao['regiao']}: {regiao['percentual']:.1f}%")
        
        print(f"\n📁 Arquivos gerados:")
        for tipo, caminho in arquivos_gerados.items():
            if caminho:
                print(f"  • {tipo}: {caminho}")
                
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()