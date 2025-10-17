"""
ANÁLISE ABA H4D - ORIENTAÇÃO DOS PROFESSORES SOBRE USO DE IA
TIC Educação 2024
"""

import pandas as pd
import json
from pathlib import Path


def analisar_h4d_orientacao_ia(arquivo_path, aba_nome='H4D'):
    """
    Analisa a aba H4D - Professores que orientaram alunos sobre uso de IA
    nos últimos 3 meses
    """
    print(f"\n{'='*80}")
    print(f"ANÁLISE ABA {aba_nome} - ORIENTAÇÃO DE PROFESSORES SOBRE USO DE IA")
    print(f"{'='*80}\n")
    
    # Carregar dados
    print(f"📂 Carregando aba {aba_nome}...")
    df_raw = pd.read_excel(arquivo_path, sheet_name=aba_nome, header=None)
    
    print(f"✅ Arquivo carregado: {df_raw.shape[0]} linhas x {df_raw.shape[1]} colunas\n")
    
    # A estrutura tem 3 blocos de perguntas sobre IA
    # Vamos focar no primeiro: "Como usar aplicações de IA"
    # Colunas: Sim (C), Não (D), Não sabe (E), Não respondeu (F)
    
    # Criar DataFrame de dados (pulando cabeçalhos)
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
    df = df[~df['categoria'].astype(str).str.contains('Fonte:', na=False)]
    
    print(f"✅ {len(df)} linhas de dados carregadas\n")
    
    # TOTAL BRASIL
    # Coluna 2 (índice 2) = Sim para "Como usar aplicações de IA"
    # Coluna 3 (índice 3) = Não
    linha_total = df[df['categoria'].astype(str).str.strip() == 'TOTAL'].iloc[0]
    
    orientaram = linha_total[2]  # Sim
    nao_orientaram = linha_total[3]  # Não
    total = orientaram + nao_orientaram
    
    pct_orientaram = (orientaram / total) * 100 if total > 0 else 0
    pct_nao_orientaram = (nao_orientaram / total) * 100 if total > 0 else 0
    
    print(f"🇧🇷 BRASIL - ORIENTAÇÃO SOBRE USO DE IA:")
    print(f"  Total de alunos: {total:,.0f}")
    print(f"  ✅ RECEBERAM orientação: {orientaram:,.0f} ({pct_orientaram:.1f}%)")
    print(f"  ❌ NÃO receberam orientação: {nao_orientaram:,.0f} ({pct_nao_orientaram:.1f}%)")
    
    # REGIÕES
    regiao = df[df['categoria'].astype(str).str.strip() == 'REGIÃO'].copy()
    regiao_data = []
    
    if len(regiao) > 0:
        print(f"\n📍 POR REGIÃO:")
        for _, row in regiao.iterrows():
            nome = row['subcategoria']
            orientou = row[2]
            nao_orientou = row[3]
            total_grupo = orientou + nao_orientou
            pct = (orientou / total_grupo * 100) if total_grupo > 0 else 0
            
            print(f"  {nome}: {orientou:,.0f} receberam ({pct:.1f}%)")
            
            regiao_data.append({
                'regiao': nome,
                'orientaram': int(orientou),
                'nao_orientaram': int(nao_orientou),
                'total': int(total_grupo),
                'percentual': round(pct, 1)
            })
    
    # ETAPA DE ENSINO
    etapa = df[df['categoria'].astype(str).str.strip() == 'ETAPA DE ENSINO'].copy()
    etapa_data = []
    
    if len(etapa) > 0:
        print(f"\n📚 POR ETAPA DE ENSINO:")
        for _, row in etapa.iterrows():
            nome = row['subcategoria']
            orientou = row[2]
            nao_orientou = row[3]
            total_grupo = orientou + nao_orientou
            pct = (orientou / total_grupo * 100) if total_grupo > 0 else 0
            
            print(f"  {nome}: {orientou:,.0f} receberam ({pct:.1f}%)")
            
            etapa_data.append({
                'etapa': nome,
                'orientaram': int(orientou),
                'nao_orientaram': int(nao_orientou),
                'total': int(total_grupo),
                'percentual': round(pct, 1)
            })
    
    # ÁREA
    area = df[df['categoria'].astype(str).str.strip() == 'ÁREA'].copy()
    area_data = []
    
    if len(area) > 0:
        print(f"\n🏙️  POR ÁREA:")
        for _, row in area.iterrows():
            nome = row['subcategoria']
            orientou = row[2]
            nao_orientou = row[3]
            total_grupo = orientou + nao_orientou
            pct = (orientou / total_grupo * 100) if total_grupo > 0 else 0
            
            print(f"  {nome}: {orientou:,.0f} receberam ({pct:.1f}%)")
            
            area_data.append({
                'area': nome,
                'orientaram': int(orientou),
                'nao_orientaram': int(nao_orientou),
                'total': int(total_grupo),
                'percentual': round(pct, 1)
            })
    
    # DEPENDÊNCIA ADMINISTRATIVA
    dep = df[df['categoria'].astype(str).str.strip() == 'DEPENDÊNCIA ADMINISTRATIVA'].copy()
    dep_data = []
    
    if len(dep) > 0:
        print(f"\n🏫 POR DEPENDÊNCIA ADMINISTRATIVA:")
        for _, row in dep.iterrows():
            nome = row['subcategoria']
            orientou = row[2]
            nao_orientou = row[3]
            total_grupo = orientou + nao_orientou
            pct = (orientou / total_grupo * 100) if total_grupo > 0 else 0
            
            print(f"  {nome}: {orientou:,.0f} receberam ({pct:.1f}%)")
            
            dep_data.append({
                'dependencia': nome,
                'orientaram': int(orientou),
                'nao_orientaram': int(nao_orientou),
                'total': int(total_grupo),
                'percentual': round(pct, 1)
            })
    
    # Consolidar resultados
    resultados = {
        'aba': aba_nome,
        'indicador': 'Alunos que receberam orientação de professores sobre uso de IA (últimos 3 meses)',
        'fonte': 'TIC Educação 2024 - Alunos',
        'brasil': {
            'total_alunos': int(total),
            'receberam_orientacao': int(orientaram),
            'nao_receberam': int(nao_orientaram),
            'percentual': round(pct_orientaram, 1)
        },
        'regioes': regiao_data,
        'etapas': etapa_data,
        'areas': area_data,
        'dependencias': dep_data
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
    json_path = f"{output_dir}/h4d_orientacao_ia_completo.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(resultados, f, ensure_ascii=False, indent=2)
    print(f"✅ JSON completo salvo: {json_path}")
    
    # CSV do Brasil
    df_brasil = pd.DataFrame([resultados['brasil']])
    csv_brasil_path = f"{output_dir}/h4d_brasil.csv"
    df_brasil.to_csv(csv_brasil_path, index=False, encoding='utf-8-sig')
    print(f"✅ CSV Brasil salvo: {csv_brasil_path}")
    
    # CSV das regiões
    if resultados['regioes']:
        df_regioes = pd.DataFrame(resultados['regioes'])
        csv_regioes_path = f"{output_dir}/h4d_regioes.csv"
        df_regioes.to_csv(csv_regioes_path, index=False, encoding='utf-8-sig')
        print(f"✅ CSV Regiões salvo: {csv_regioes_path}")
    
    # CSV etapas
    if resultados['etapas']:
        df_etapas = pd.DataFrame(resultados['etapas'])
        csv_etapas_path = f"{output_dir}/h4d_etapas.csv"
        df_etapas.to_csv(csv_etapas_path, index=False, encoding='utf-8-sig')
        print(f"✅ CSV Etapas salvo: {csv_etapas_path}")
    
    # CSV áreas
    if resultados['areas']:
        df_areas = pd.DataFrame(resultados['areas'])
        csv_areas_path = f"{output_dir}/h4d_areas.csv"
        df_areas.to_csv(csv_areas_path, index=False, encoding='utf-8-sig')
        print(f"✅ CSV Áreas salvo: {csv_areas_path}")
    
    # CSV dependências
    if resultados['dependencias']:
        df_deps = pd.DataFrame(resultados['dependencias'])
        csv_deps_path = f"{output_dir}/h4d_dependencias.csv"
        df_deps.to_csv(csv_deps_path, index=False, encoding='utf-8-sig')
        print(f"✅ CSV Dependências salvo: {csv_deps_path}")
    
    return {
        'json': json_path,
        'csv_brasil': csv_brasil_path,
        'csv_regioes': csv_regioes_path if resultados['regioes'] else None,
        'csv_etapas': csv_etapas_path if resultados['etapas'] else None,
        'csv_areas': csv_areas_path if resultados['areas'] else None,
        'csv_dependencias': csv_deps_path if resultados['dependencias'] else None
    }


if __name__ == "__main__":
    arquivo = 'tic_educacao_2024_alunos_tabela_total_v1.0.xlsx'
    
    try:
        # Executar análise
        resultados = analisar_h4d_orientacao_ia(arquivo, aba_nome='H4D')
        
        # SALVAR RESULTADOS
        arquivos_gerados = salvar_resultados(resultados)
        
        print(f"\n{'='*80}")
        print("✅ ANÁLISE H4D CONCLUÍDA!")
        print(f"{'='*80}")
        print(f"\n📊 Resultado principal:")
        print(f"  • {resultados['brasil']['percentual']:.1f}% dos alunos RECEBERAM orientação sobre IA")
        
        if resultados['etapas']:
            print(f"\n📚 Por etapa de ensino:")
            for etapa in resultados['etapas']:
                print(f"  • {etapa['etapa']}: {etapa['percentual']:.1f}%")
        
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