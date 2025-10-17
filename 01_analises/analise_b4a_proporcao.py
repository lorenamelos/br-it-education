"""
ANÁLISE ABA B4A - PROPORÇÃO ALUNOS POR COMPUTADOR
TIC Educação 2024
"""

import pandas as pd
import json
from pathlib import Path


def analisar_b4a_proporcao(arquivo_path, aba_nome='B4A'):
    """
    Analisa a aba B4A - Proporção alunos por computador disponível
    """
    print(f"\n{'='*80}")
    print(f"ANÁLISE ABA {aba_nome} - PROPORÇÃO ALUNOS/COMPUTADOR")
    print(f"{'='*80}\n")
    
    # Carregar dados
    print(f"📂 Carregando aba {aba_nome}...")
    df = pd.read_excel(
        arquivo_path, 
        sheet_name=aba_nome,
        skiprows=3,
        header=None
    )
    
    # Definir nomes das colunas
    colunas = [
        'categoria',
        'subcategoria',
        'ate_5_alunos',
        'de_5_1_a_10',
        'de_10_1_a_15',
        'de_15_1_a_20',
        'de_20_1_a_30',
        'de_30_1_a_40',
        'de_40_1_a_50',
        'de_50_1_a_100',
        '100_alunos_ou_mais',
        'nao_possuem_computador_mesa',
        'sem_informacao_numero_alunos'
    ]
    
    df = df.iloc[:, :len(colunas)]
    df.columns = colunas
    
    # Limpar dados
    df = df.dropna(subset=['categoria'])
    df = df[~df['categoria'].astype(str).str.contains('Fonte:', na=False)]
    
    print(f"✅ {len(df)} linhas carregadas\n")
    
    # TOTAL BRASIL
    print(f"🔍 Debug - Primeiras categorias: {df['categoria'].head().tolist()}\n")
    linha_brasil = df[df['categoria'].astype(str).str.strip() == 'TOTAL'].iloc[0]
    
    # Definir faixas adequadas e inadequadas
    # Adequada: até 20 alunos por computador
    faixas_adequadas = ['ate_5_alunos', 'de_5_1_a_10', 'de_10_1_a_15', 'de_15_1_a_20']
    faixas_inadequadas = ['de_20_1_a_30', 'de_30_1_a_40', 'de_40_1_a_50', 
                          'de_50_1_a_100', '100_alunos_ou_mais']
    
    # Calcular totais
    total_adequadas = sum([linha_brasil[col] for col in faixas_adequadas if pd.notna(linha_brasil[col])])
    total_inadequadas = sum([linha_brasil[col] for col in faixas_inadequadas if pd.notna(linha_brasil[col])])
    sem_computador = linha_brasil['nao_possuem_computador_mesa'] if pd.notna(linha_brasil['nao_possuem_computador_mesa']) else 0
    
    total = total_adequadas + total_inadequadas + sem_computador
    
    pct_adequadas = (total_adequadas / total) * 100 if total > 0 else 0
    pct_inadequadas = (total_inadequadas / total) * 100 if total > 0 else 0
    pct_sem = (sem_computador / total) * 100 if total > 0 else 0
    
    print(f"🇧🇷 BRASIL:")
    print(f"  Total de escolas: {total:,.0f}")
    print(f"\n  📊 PROPORÇÃO ALUNOS/COMPUTADOR:")
    print(f"  ✅ ADEQUADA (≤20 alunos/PC): {total_adequadas:,.0f} ({pct_adequadas:.1f}%)")
    print(f"  ⚠️  INADEQUADA (>20 alunos/PC): {total_inadequadas:,.0f} ({pct_inadequadas:.1f}%)")
    print(f"  ❌ SEM computador: {sem_computador:,.0f} ({pct_sem:.1f}%)")
    
    # REGIÕES
    regioes = df[df['categoria'].astype(str).str.strip() == 'REGIÃO'].copy()
    regioes_data = []
    
    if len(regioes) > 0:
        print(f"\n📍 POR REGIÃO:")
        for _, regiao in regioes.iterrows():
            nome = regiao['subcategoria']
            
            adequadas = sum([regiao[col] for col in faixas_adequadas if pd.notna(regiao[col])])
            inadequadas = sum([regiao[col] for col in faixas_inadequadas if pd.notna(regiao[col])])
            sem_pc = regiao['nao_possuem_computador_mesa'] if pd.notna(regiao['nao_possuem_computador_mesa']) else 0
            
            total_reg = adequadas + inadequadas + sem_pc
            pct_adequada = (adequadas / total_reg) * 100 if total_reg > 0 else 0
            
            print(f"  {nome}: {pct_adequada:.1f}% com proporção adequada")
            
            regioes_data.append({
                'regiao': nome,
                'total': int(total_reg),
                'proporcao_adequada': int(adequadas),
                'proporcao_inadequada': int(inadequadas),
                'sem_computador': int(sem_pc),
                'percentual_adequada': round(pct_adequada, 1)
            })
    
    # ÁREAS
    areas = df[df['categoria'].astype(str).str.strip() == 'ÁREA'].copy()
    areas_data = []
    
    if len(areas) > 0:
        print(f"\n🏙️  POR ÁREA:")
        for _, area in areas.iterrows():
            nome = area['subcategoria']
            
            adequadas = sum([area[col] for col in faixas_adequadas if pd.notna(area[col])])
            inadequadas = sum([area[col] for col in faixas_inadequadas if pd.notna(area[col])])
            sem_pc = area['nao_possuem_computador_mesa'] if pd.notna(area['nao_possuem_computador_mesa']) else 0
            
            total_area = adequadas + inadequadas + sem_pc
            pct_adequada = (adequadas / total_area) * 100 if total_area > 0 else 0
            
            print(f"  {nome}: {pct_adequada:.1f}% com proporção adequada")
            
            areas_data.append({
                'area': nome,
                'total': int(total_area),
                'proporcao_adequada': int(adequadas),
                'proporcao_inadequada': int(inadequadas),
                'sem_computador': int(sem_pc),
                'percentual_adequada': round(pct_adequada, 1)
            })
    
    # Consolidar resultados
    resultados = {
        'aba': aba_nome,
        'indicador': 'Proporção Alunos por Computador Disponível',
        'fonte': 'TIC Educação 2024 - Escolas',
        'brasil': {
            'total_escolas': int(total),
            'proporcao_adequada': int(total_adequadas),
            'proporcao_inadequada': int(total_inadequadas),
            'sem_computador': int(sem_computador),
            'pct_adequada': round(pct_adequadas, 1),
            'pct_inadequada': round(pct_inadequadas, 1),
            'pct_sem': round(pct_sem, 1)
        },
        'regioes': regioes_data,
        'areas': areas_data
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
    json_path = f"{output_dir}/b4a_proporcao_completo.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(resultados, f, ensure_ascii=False, indent=2)
    print(f"✅ JSON completo salvo: {json_path}")
    
    # CSV do Brasil
    df_brasil = pd.DataFrame([resultados['brasil']])
    csv_brasil_path = f"{output_dir}/b4a_brasil.csv"
    df_brasil.to_csv(csv_brasil_path, index=False, encoding='utf-8-sig')
    print(f"✅ CSV Brasil salvo: {csv_brasil_path}")
    
    # CSV das regiões
    if resultados['regioes']:
        df_regioes = pd.DataFrame(resultados['regioes'])
        csv_regioes_path = f"{output_dir}/b4a_regioes.csv"
        df_regioes.to_csv(csv_regioes_path, index=False, encoding='utf-8-sig')
        print(f"✅ CSV Regiões salvo: {csv_regioes_path}")
    
    # CSV das áreas
    if resultados['areas']:
        df_areas = pd.DataFrame(resultados['areas'])
        csv_areas_path = f"{output_dir}/b4a_areas.csv"
        df_areas.to_csv(csv_areas_path, index=False, encoding='utf-8-sig')
        print(f"✅ CSV Áreas salvo: {csv_areas_path}")
    
    return {
        'json': json_path,
        'csv_brasil': csv_brasil_path,
        'csv_regioes': csv_regioes_path if resultados['regioes'] else None,
        'csv_areas': csv_areas_path if resultados['areas'] else None
    }


if __name__ == "__main__":
    arquivo = 'tic_educacao_2024_escolas_tabela_total_v1.0.xlsx'
    
    try:
        # Executar análise
        resultados = analisar_b4a_proporcao(arquivo, aba_nome='B4A')
        
        # SALVAR RESULTADOS
        arquivos_gerados = salvar_resultados(resultados)
        
        print(f"\n{'='*80}")
        print("✅ ANÁLISE B4A CONCLUÍDA!")
        print(f"{'='*80}")
        print(f"\n📊 Resultado principal:")
        print(f"  • {resultados['brasil']['pct_adequada']:.1f}% das escolas têm proporção ADEQUADA (≤20 alunos/PC)")
        print(f"  • {resultados['brasil']['pct_inadequada']:.1f}% têm proporção INADEQUADA (>20 alunos/PC)")
        print(f"  • {resultados['brasil']['pct_sem']:.1f}% NÃO têm computador")
        
        if resultados['regioes']:
            print(f"\n📍 Por região:")
            for regiao in resultados['regioes']:
                print(f"  • {regiao['regiao']}: {regiao['percentual_adequada']:.1f}%")
        
        print(f"\n📁 Arquivos gerados:")
        for tipo, caminho in arquivos_gerados.items():
            if caminho:
                print(f"  • {tipo}: {caminho}")
                
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()