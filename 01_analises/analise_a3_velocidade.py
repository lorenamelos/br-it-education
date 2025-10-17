"""
ANÁLISE ABA A3 - VELOCIDADE DA CONEXÃO DE INTERNET
TIC Educação 2024
"""

import pandas as pd
import json
from pathlib import Path


def analisar_a3_velocidade(arquivo_path, aba_nome='A3'):
    """
    Analisa a aba A3 - Velocidade da principal conexão de internet
    """
    print(f"\n{'='*80}")
    print(f"ANÁLISE ABA {aba_nome} - VELOCIDADE DA CONEXÃO DE INTERNET")
    print(f"{'='*80}\n")
    
    # Carregar dados
    print(f"📂 Carregando aba {aba_nome}...")
    df = pd.read_excel(
        arquivo_path, 
        sheet_name=aba_nome,
        skiprows=3,  # Pula título e cabeçalhos
        header=None
    )
    
    # Definir nomes das colunas baseado na estrutura da imagem
    colunas = [
        'categoria',
        'subcategoria', 
        'ate_10_mbps',
        'de_11_a_50_mbps',
        'de_51_a_100_mbps',
        'de_101_a_250_mbps',
        'de_251_a_500_mbps',
        'de_501_a_1_gbps',
        '1_gbps_ou_mais',
        'nao_sabe',
        'nao_respondeu',
        'nao_se_aplica'
    ]
    
    # Ajustar número de colunas
    df = df.iloc[:, :len(colunas)]
    df.columns = colunas
    
    # Limpar dados
    df = df.dropna(subset=['categoria'])
    df = df[~df['categoria'].astype(str).str.contains('Fonte:', na=False)]
    
    print(f"✅ {len(df)} linhas carregadas\n")
    
    # TOTAL BRASIL
    # Debug: mostrar primeiras linhas
    print(f"🔍 Debug - Primeiras categorias: {df['categoria'].head().tolist()}\n")
    
    linha_brasil = df[df['categoria'].astype(str).str.strip() == 'TOTAL'].iloc[0]
    
    # Definir faixas de velocidade
    faixas_rapidas = ['de_101_a_250_mbps', 'de_251_a_500_mbps', 'de_501_a_1_gbps', '1_gbps_ou_mais']
    faixas_medias = ['de_51_a_100_mbps']
    faixas_lentas = ['ate_10_mbps', 'de_11_a_50_mbps']
    
    # Calcular totais
    total_rapidas = sum([linha_brasil[col] for col in faixas_rapidas if pd.notna(linha_brasil[col])])
    total_medias = sum([linha_brasil[col] for col in faixas_medias if pd.notna(linha_brasil[col])])
    total_lentas = sum([linha_brasil[col] for col in faixas_lentas if pd.notna(linha_brasil[col])])
    
    total = total_rapidas + total_medias + total_lentas
    
    pct_rapidas = (total_rapidas / total) * 100 if total > 0 else 0
    pct_medias = (total_medias / total) * 100 if total > 0 else 0
    pct_lentas = (total_lentas / total) * 100 if total > 0 else 0
    
    # Conexão adequada para IA (≥ 51 Mbps)
    conexao_adequada = total_rapidas + total_medias
    pct_adequada = (conexao_adequada / total) * 100 if total > 0 else 0
    
    print(f"🇧🇷 BRASIL:")
    print(f"  Total de escolas: {total:,.0f}")
    print(f"\n  📶 VELOCIDADE DA CONEXÃO:")
    print(f"  🚀 RÁPIDA (≥100 Mbps): {total_rapidas:,.0f} ({pct_rapidas:.1f}%)")
    print(f"  ⚡ MÉDIA (51-100 Mbps): {total_medias:,.0f} ({pct_medias:.1f}%)")
    print(f"  🐌 LENTA (≤50 Mbps): {total_lentas:,.0f} ({pct_lentas:.1f}%)")
    print(f"\n  ✅ ADEQUADA para IA (≥51 Mbps): {conexao_adequada:,.0f} ({pct_adequada:.1f}%)")
    print(f"  ❌ INADEQUADA para IA (≤50 Mbps): {total_lentas:,.0f} ({pct_lentas:.1f}%)")
    
    # REGIÕES
    regioes = df[df['categoria'].astype(str).str.strip() == 'REGIÃO'].copy()
    regioes_data = []
    
    if len(regioes) > 0:
        print(f"\n📍 POR REGIÃO:")
        for _, regiao in regioes.iterrows():
            nome = regiao['subcategoria']
            
            rapidas = sum([regiao[col] for col in faixas_rapidas if pd.notna(regiao[col])])
            medias = sum([regiao[col] for col in faixas_medias if pd.notna(regiao[col])])
            lentas = sum([regiao[col] for col in faixas_lentas if pd.notna(regiao[col])])
            
            total_reg = rapidas + medias + lentas
            adequada_reg = rapidas + medias
            pct_adequada_reg = (adequada_reg / total_reg) * 100 if total_reg > 0 else 0
            
            print(f"  {nome}: {pct_adequada_reg:.1f}% com velocidade adequada (≥51 Mbps)")
            
            regioes_data.append({
                'regiao': nome,
                'total': int(total_reg),
                'conexao_adequada': int(adequada_reg),
                'conexao_inadequada': int(lentas),
                'percentual_adequada': round(pct_adequada_reg, 1)
            })
    
    # ÁREAS
    areas = df[df['categoria'].astype(str).str.strip() == 'ÁREA'].copy()
    areas_data = []
    
    if len(areas) > 0:
        print(f"\n🏙️  POR ÁREA:")
        for _, area in areas.iterrows():
            nome = area['subcategoria']
            
            rapidas = sum([area[col] for col in faixas_rapidas if pd.notna(area[col])])
            medias = sum([area[col] for col in faixas_medias if pd.notna(area[col])])
            lentas = sum([area[col] for col in faixas_lentas if pd.notna(area[col])])
            
            total_area = rapidas + medias + lentas
            adequada_area = rapidas + medias
            pct_adequada_area = (adequada_area / total_area) * 100 if total_area > 0 else 0
            
            print(f"  {nome}: {pct_adequada_area:.1f}% com velocidade adequada")
            
            areas_data.append({
                'area': nome,
                'total': int(total_area),
                'conexao_adequada': int(adequada_area),
                'conexao_inadequada': int(lentas),
                'percentual_adequada': round(pct_adequada_area, 1)
            })
    
    # Consolidar resultados
    resultados = {
        'aba': aba_nome,
        'indicador': 'Velocidade da Principal Conexão de Internet',
        'fonte': 'TIC Educação 2024 - Escolas',
        'brasil': {
            'total_escolas': int(total),
            'conexao_rapida': int(total_rapidas),
            'conexao_media': int(total_medias),
            'conexao_lenta': int(total_lentas),
            'conexao_adequada_ia': int(conexao_adequada),
            'pct_adequada': round(pct_adequada, 1),
            'pct_rapida': round(pct_rapidas, 1),
            'pct_media': round(pct_medias, 1),
            'pct_lenta': round(pct_lentas, 1)
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
    json_path = f"{output_dir}/a3_velocidade_completo.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(resultados, f, ensure_ascii=False, indent=2)
    print(f"✅ JSON completo salvo: {json_path}")
    
    # CSV do Brasil
    df_brasil = pd.DataFrame([resultados['brasil']])
    csv_brasil_path = f"{output_dir}/a3_brasil.csv"
    df_brasil.to_csv(csv_brasil_path, index=False, encoding='utf-8-sig')
    print(f"✅ CSV Brasil salvo: {csv_brasil_path}")
    
    # CSV das regiões
    if resultados['regioes']:
        df_regioes = pd.DataFrame(resultados['regioes'])
        csv_regioes_path = f"{output_dir}/a3_regioes.csv"
        df_regioes.to_csv(csv_regioes_path, index=False, encoding='utf-8-sig')
        print(f"✅ CSV Regiões salvo: {csv_regioes_path}")
    
    # CSV das áreas
    if resultados['areas']:
        df_areas = pd.DataFrame(resultados['areas'])
        csv_areas_path = f"{output_dir}/a3_areas.csv"
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
        resultados = analisar_a3_velocidade(arquivo, aba_nome='A3_1')
        
        # SALVAR RESULTADOS
        arquivos_gerados = salvar_resultados(resultados)
        
        print(f"\n{'='*80}")
        print("✅ ANÁLISE A3 CONCLUÍDA!")
        print(f"{'='*80}")
        print(f"\n📊 Resultado principal:")
        print(f"  • {resultados['brasil']['pct_adequada']:.1f}% das escolas têm velocidade ADEQUADA (≥51 Mbps)")
        print(f"  • {resultados['brasil']['pct_lenta']:.1f}% têm velocidade LENTA (≤50 Mbps)")
        
        print(f"\n📶 Detalhamento:")
        print(f"  • Rápida (≥100 Mbps): {resultados['brasil']['pct_rapida']:.1f}%")
        print(f"  • Média (51-100 Mbps): {resultados['brasil']['pct_media']:.1f}%")
        print(f"  • Lenta (≤50 Mbps): {resultados['brasil']['pct_lenta']:.1f}%")
        
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