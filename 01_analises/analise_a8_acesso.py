"""
ANÁLISE ABA A8 - ESCOLAS COM COMPUTADOR E INTERNET PARA ALUNOS
TIC Educação 2024
"""

import pandas as pd
import json
from pathlib import Path

def analisar_a8(arquivo_path, aba_nome='A8'):
    """
    Analisa a aba A8 - Acesso a computador + internet
    
    Retorna:
    --------
    dict com os resultados da análise
    """
    print(f"\n{'='*80}")
    print(f"ANÁLISE ABA {aba_nome} - ACESSO A COMPUTADOR + INTERNET")
    print(f"{'='*80}\n")
    
    # Carregar dados
    print(f"📂 Carregando aba {aba_nome}...")
    df = pd.read_excel(
        arquivo_path, 
        sheet_name=aba_nome,
        skiprows=3,  # Pula título e cabeçalhos
        usecols=[0, 1, 2, 3],
        names=['categoria', 'subcategoria', 'sim', 'nao']
    )
    
    # Limpar dados
    df = df.dropna(subset=['categoria'])
    df = df[~df['categoria'].str.contains('Fonte:', na=False)]
    
    print(f"✅ {len(df)} linhas carregadas\n")
    
    # TOTAL BRASIL
    linha_brasil = df[df['categoria'] == 'TOTAL'].iloc[0]
    
    com_acesso = linha_brasil['sim']
    sem_acesso = linha_brasil['nao']
    total = com_acesso + sem_acesso
    pct_com_acesso = (com_acesso / total) * 100
    pct_sem_acesso = (sem_acesso / total) * 100
    
    print(f"🇧🇷 BRASIL:")
    print(f"  Total de escolas: {total:,.0f}")
    print(f"  ✅ COM acesso (PC+Internet): {com_acesso:,.0f} ({pct_com_acesso:.1f}%)")
    print(f"  ❌ SEM acesso: {sem_acesso:,.0f} ({pct_sem_acesso:.1f}%)")
    
    # REGIÕES
    regioes = df[df['categoria'] == 'REGIÃO'].copy()
    regioes_data = []
    
    print(f"\n📍 POR REGIÃO:")
    for _, regiao in regioes.iterrows():
        nome = regiao['subcategoria']
        com = regiao['sim']
        sem = regiao['nao']
        total_reg = com + sem
        pct = (com / total_reg) * 100
        
        print(f"  {nome}: {com:,.0f} COM ({pct:.1f}%) | {sem:,.0f} SEM ({100-pct:.1f}%)")
        
        regioes_data.append({
            'regiao': nome,
            'com_acesso': int(com),
            'sem_acesso': int(sem),
            'total': int(total_reg),
            'percentual': round(pct, 1)
        })
    
    # ÁREAS
    areas = df[df['categoria'] == 'ÁREA'].copy()
    areas_data = []
    
    if len(areas) > 0:
        print(f"\n🏙️  POR ÁREA:")
        for _, area in areas.iterrows():
            nome = area['subcategoria']
            com = area['sim']
            sem = area['nao']
            total_area = com + sem
            pct = (com / total_area) * 100
            
            print(f"  {nome}: {com:,.0f} COM ({pct:.1f}%)")
            
            areas_data.append({
                'area': nome,
                'com_acesso': int(com),
                'sem_acesso': int(sem),
                'total': int(total_area),
                'percentual': round(pct, 1)
            })
    
    # Consolidar resultados
    resultados = {
        'aba': aba_nome,
        'indicador': 'Acesso a Computador + Internet para Alunos',
        'fonte': 'TIC Educação 2024 - Escolas',
        'brasil': {
            'total_escolas': int(total),
            'com_acesso': int(com_acesso),
            'sem_acesso': int(sem_acesso),
            'pct_com_acesso': round(pct_com_acesso, 1),
            'pct_sem_acesso': round(pct_sem_acesso, 1)
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
    json_path = f"{output_dir}/a8_acesso_completo.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(resultados, f, ensure_ascii=False, indent=2)
    print(f"✅ JSON completo salvo: {json_path}")
    
    # CSV do Brasil
    df_brasil = pd.DataFrame([resultados['brasil']])
    csv_brasil_path = f"{output_dir}/a8_brasil.csv"
    df_brasil.to_csv(csv_brasil_path, index=False, encoding='utf-8-sig')
    print(f"✅ CSV Brasil salvo: {csv_brasil_path}")
    
    # CSV das regiões
    if resultados['regioes']:
        df_regioes = pd.DataFrame(resultados['regioes'])
        csv_regioes_path = f"{output_dir}/a8_regioes.csv"
        df_regioes.to_csv(csv_regioes_path, index=False, encoding='utf-8-sig')
        print(f"✅ CSV Regiões salvo: {csv_regioes_path}")
    
    # CSV das áreas
    if resultados['areas']:
        df_areas = pd.DataFrame(resultados['areas'])
        csv_areas_path = f"{output_dir}/a8_areas.csv"
        df_areas.to_csv(csv_areas_path, index=False, encoding='utf-8-sig')
        print(f"✅ CSV Áreas salvo: {csv_areas_path}")
    
    return {
        'json': json_path,
        'csv_brasil': csv_brasil_path,
        'csv_regioes': csv_regioes_path if resultados['regioes'] else None,
        'csv_areas': csv_areas_path if resultados['areas'] else None
    }


if __name__ == "__main__":
    # Configuração
    arquivo = 'tic_educacao_2024_escolas_tabela_total_v1.0.xlsx'
    
    try:
        # Executar análise
        resultados = analisar_a8(arquivo, aba_nome='A8')
        
        # SALVAR RESULTADOS (esta linha é ESSENCIAL!)
        arquivos_gerados = salvar_resultados(resultados)
        
        print(f"\n{'='*80}")
        print("✅ ANÁLISE A8 CONCLUÍDA!")
        print(f"{'='*80}")
        print(f"\n📊 Resultado principal:")
        print(f"  • {resultados['brasil']['pct_com_acesso']:.1f}% das escolas TÊM acesso")
        print(f"  • {resultados['brasil']['pct_sem_acesso']:.1f}% das escolas NÃO têm acesso")
        
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