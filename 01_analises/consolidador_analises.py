"""
CONSOLIDADOR DE ANÁLISES - TRIPLO DÉFICIT TECNOLÓGICO
TIC Educação 2024 - Análise Completa
Reúne A8, A3, G6 e H4D em um relatório final
"""

import pandas as pd
import json
from pathlib import Path
from datetime import datetime


def carregar_resultado(arquivo_json):
    """
    Carrega um arquivo JSON de resultado
    """
    try:
        with open(arquivo_json, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"⚠️  Arquivo não encontrado: {arquivo_json}")
        return None


def calcular_indice_infraestrutura(a8_data, a3_data, b4a_data):
    """
    Calcula índice de infraestrutura combinando acesso, velocidade e proporção
    """
    if not a8_data or not a3_data or not b4a_data:
        return None
    
    print("\n" + "="*80)
    print("PILAR 1: INFRAESTRUTURA TECNOLÓGICA")
    print("="*80 + "\n")
    
    pct_acesso = a8_data['brasil']['pct_com_acesso']
    pct_velocidade = a3_data['brasil']['pct_adequada']
    pct_proporcao = b4a_data['brasil']['pct_adequada']
    
    # Índice multiplicativo (todos três precisam estar presentes)
    indice_infra = (pct_acesso / 100) * (pct_velocidade / 100) * (pct_proporcao / 100) * 100
    
    print(f"📊 Componentes da Infraestrutura:")
    print(f"  • Acesso (PC+Internet): {pct_acesso:.1f}%")
    print(f"  • Velocidade Adequada (≥51 Mbps): {pct_velocidade:.1f}%")
    print(f"  • Proporção Adequada (≤20 alunos/PC): {pct_proporcao:.1f}%")
    print(f"\n🎯 ÍNDICE DE INFRAESTRUTURA: {indice_infra:.1f}%")
    print(f"   (Escolas com TODOS os 3 requisitos)")
    
    return {
        'pct_acesso': pct_acesso,
        'pct_velocidade': pct_velocidade,
        'pct_proporcao': pct_proporcao,
        'indice': indice_infra
    }


def calcular_indice_orientacao(h4d_data):
    """
    Analisa o pilar de orientação pedagógica sobre IA
    """
    if not h4d_data:
        return None
    
    print("\n" + "="*80)
    print("PILAR 2: ORIENTAÇÃO PEDAGÓGICA SOBRE IA")
    print("="*80 + "\n")
    
    pct_orientacao = h4d_data['brasil']['percentual']
    
    print(f"👨‍🏫 Orientação dos professores:")
    print(f"  • Alunos que receberam orientação sobre IA: {pct_orientacao:.1f}%")
    print(f"\n🎯 ÍNDICE DE ORIENTAÇÃO: {pct_orientacao:.1f}%")
    
    return {
        'pct_orientacao': pct_orientacao,
        'indice': pct_orientacao
    }


def calcular_indice_uso(g6_data):
    """
    Analisa o pilar de uso real
    """
    if not g6_data:
        return None
    
    print("\n" + "="*80)
    print("PILAR 3: USO REAL DE IA")
    print("="*80 + "\n")
    
    pct_uso = g6_data['brasil']['percentual']
    
    print(f"🤖 Uso de IA Generativa:")
    print(f"  • Alunos que usam IA: {pct_uso:.1f}%")
    print(f"\n🎯 ÍNDICE DE USO: {pct_uso:.1f}%")
    
    return {
        'pct_uso': pct_uso,
        'indice': pct_uso
    }


def calcular_triplo_deficit(infra, orientacao, uso):
    """
    Calcula o Triplo Déficit Tecnológico
    """
    print("\n" + "="*80)
    print("CÁLCULO DO TRIPLO DÉFICIT TECNOLÓGICO")
    print("="*80 + "\n")
    
    if not all([infra, orientacao, uso]):
        print("⚠️  Dados incompletos para calcular o Triplo Déficit")
        return None
    
    # Índice de Prontidão = média dos 3 pilares
    indice_prontidao = (infra['indice'] + orientacao['indice'] + uso['indice']) / 3
    
    print(f"📊 RESUMO DOS 3 PILARES:")
    print(f"  1️⃣ Infraestrutura: {infra['indice']:.1f}%")
    print(f"  2️⃣ Orientação Pedagógica: {orientacao['indice']:.1f}%")
    print(f"  3️⃣ Uso Real: {uso['indice']:.1f}%")
    print(f"\n🎯 ÍNDICE DE PRONTIDÃO PARA IA: {indice_prontidao:.1f}%")
    print(f"   (Média dos 3 pilares)")
    
    # Calcular déficits (quanto falta para 100%)
    deficit_infra = 100 - infra['indice']
    deficit_orientacao = 100 - orientacao['indice']
    deficit_uso = 100 - uso['indice']
    deficit_total = 100 - indice_prontidao
    
    print(f"\n⚠️  DÉFICITS IDENTIFICADOS:")
    print(f"  • Déficit de Infraestrutura: {deficit_infra:.1f} pontos")
    print(f"  • Déficit de Orientação: {deficit_orientacao:.1f} pontos")
    print(f"  • Déficit de Uso: {deficit_uso:.1f} pontos")
    print(f"  • DÉFICIT TOTAL: {deficit_total:.1f} pontos")
    
    return {
        'indice_prontidao': indice_prontidao,
        'deficit_infraestrutura': deficit_infra,
        'deficit_orientacao': deficit_orientacao,
        'deficit_uso': deficit_uso,
        'deficit_total': deficit_total
    }


def analisar_paradoxos(infra, orientacao, uso):
    """
    Identifica paradoxos entre os pilares
    """
    print("\n" + "="*80)
    print("ANÁLISE DE PARADOXOS")
    print("="*80 + "\n")
    
    if not all([infra, orientacao, uso]):
        return None
    
    paradoxos = []
    
    # Paradoxo 1: Uso maior que Infraestrutura
    gap_uso_infra = uso['indice'] - infra['indice']
    if gap_uso_infra > 0:
        print(f"🚨 PARADOXO 1: USO > INFRAESTRUTURA")
        print(f"   • {uso['indice']:.1f}% dos alunos USAM IA")
        print(f"   • {infra['indice']:.1f}% das escolas têm infraestrutura adequada")
        print(f"   • GAP: +{gap_uso_infra:.1f} pontos")
        print(f"   → Alunos estão usando IA FORA da escola (celular, casa)")
        paradoxos.append({
            'tipo': 'Uso > Infraestrutura',
            'gap': gap_uso_infra,
            'interpretacao': 'Uso acontece fora do ambiente escolar'
        })
    
    # Paradoxo 2: Uso maior que Orientação
    gap_uso_orientacao = uso['indice'] - orientacao['indice']
    if gap_uso_orientacao > 0:
        print(f"\n🚨 PARADOXO 2: USO > ORIENTAÇÃO")
        print(f"   • {uso['indice']:.1f}% dos alunos USAM IA")
        print(f"   • {orientacao['indice']:.1f}% receberam orientação pedagógica")
        print(f"   • GAP: +{gap_uso_orientacao:.1f} pontos")
        print(f"   → Alunos estão aprendendo sozinhos, sem orientação pedagógica")
        paradoxos.append({
            'tipo': 'Uso > Orientação',
            'gap': gap_uso_orientacao,
            'interpretacao': 'Aprendizado autônomo sem orientação'
        })
    
    # Paradoxo 3: Orientação maior que Infraestrutura
    gap_orientacao_infra = orientacao['indice'] - infra['indice']
    if gap_orientacao_infra > 0:
        print(f"\n🚨 PARADOXO 3: ORIENTAÇÃO > INFRAESTRUTURA")
        print(f"   • {orientacao['indice']:.1f}% receberam orientação")
        print(f"   • {infra['indice']:.1f}% das escolas têm infraestrutura")
        print(f"   • GAP: +{gap_orientacao_infra:.1f} pontos")
        print(f"   → Orientação sem condições de praticar na escola")
        paradoxos.append({
            'tipo': 'Orientação > Infraestrutura',
            'gap': gap_orientacao_infra,
            'interpretacao': 'Teoria sem prática por falta de infraestrutura'
        })
    
    if not paradoxos:
        print("✅ Nenhum paradoxo significativo identificado")
    
    return paradoxos


def criar_comparacao_regional(resultados_dict):
    """
    Cria tabela comparativa por região
    """
    print("\n" + "="*80)
    print("COMPARAÇÃO REGIONAL")
    print("="*80 + "\n")
    
    if not all([resultados_dict.get('a8'), resultados_dict.get('a3'), 
                resultados_dict.get('g6'), resultados_dict.get('h4d')]):
        print("⚠️  Dados regionais incompletos")
        return None
    
    # Pegar dados regionais de cada análise
    regioes_a8 = {r['regiao']: r['percentual'] for r in resultados_dict['a8']['regioes']}
    regioes_a3 = {r['regiao']: r['percentual_adequada'] for r in resultados_dict['a3']['regioes']}
    regioes_g6 = {r['regiao']: r['percentual'] for r in resultados_dict['g6']['regioes']}
    regioes_h4d = {r['regiao']: r['percentual'] for r in resultados_dict['h4d']['regioes']}
    
    comparacao = []
    
    for regiao in regioes_a8.keys():
        acesso = regioes_a8.get(regiao, 0)
        velocidade = regioes_a3.get(regiao, 0)
        uso = regioes_g6.get(regiao, 0)
        orientacao = regioes_h4d.get(regiao, 0)
        
        # Índice de infraestrutura regional
        infra_reg = (acesso / 100) * (velocidade / 100) * 100
        
        # Índice de prontidão regional
        prontidao_reg = (infra_reg + orientacao + uso) / 3
        
        comparacao.append({
            'Região': regiao,
            'Infraestrutura (%)': round(infra_reg, 1),
            'Orientação (%)': round(orientacao, 1),
            'Uso (%)': round(uso, 1),
            'Prontidão (%)': round(prontidao_reg, 1),
            'Déficit': round(100 - prontidao_reg, 1)
        })
    
    df_comp = pd.DataFrame(comparacao).sort_values('Prontidão (%)', ascending=False)
    
    print(df_comp.to_string(index=False))
    
    return df_comp


def gerar_relatorio_final(resultados_dict, output_dir='./resultados'):
    """
    Gera relatório consolidado completo
    """
    Path(output_dir).mkdir(exist_ok=True)
    
    print("\n" + "="*80)
    print("GERANDO RELATÓRIO CONSOLIDADO")
    print("="*80 + "\n")
    
    # Calcular índices
    infra = calcular_indice_infraestrutura(
        resultados_dict.get('a8'), 
        resultados_dict.get('a3'),
            resultados_dict.get('b4a') 

    )
    
    orientacao = calcular_indice_orientacao(resultados_dict.get('h4d'))
    uso = calcular_indice_uso(resultados_dict.get('g6'))
    
    # Calcular Triplo Déficit
    triplo_deficit = calcular_triplo_deficit(infra, orientacao, uso)
    
    # Analisar paradoxos
    paradoxos = analisar_paradoxos(infra, orientacao, uso)
    
    # Comparação regional
    comp_regional = criar_comparacao_regional(resultados_dict)
    
    # Estrutura do relatório final
    relatorio = {
        'metadados': {
            'data_geracao': datetime.now().isoformat(),
            'fonte': 'TIC Educação 2024',
            'analises_incluidas': list(resultados_dict.keys())
        },
        'pilares': {
            'infraestrutura': infra,
            'orientacao': orientacao,
            'uso': uso
        },
        'triplo_deficit': triplo_deficit,
        'paradoxos': paradoxos,
        'dados_brutos': resultados_dict
    }
    
    # Salvar JSON completo
    json_path = f"{output_dir}/relatorio_triplo_deficit_completo.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(relatorio, f, ensure_ascii=False, indent=2)
    print(f"\n✅ Relatório JSON salvo: {json_path}")
    
    # Resumo executivo em CSV
    resumo_data = []
    
    if infra:
        resumo_data.append({
            'Pilar': '1. Infraestrutura',
            'Indicador': 'Acesso + Velocidade',
            'Percentual': f"{infra['indice']:.1f}%",
            'Fonte': 'A8 + A3'
        })
    
    if orientacao:
        resumo_data.append({
            'Pilar': '2. Orientação',
            'Indicador': 'Orientação pedagógica sobre IA',
            'Percentual': f"{orientacao['indice']:.1f}%",
            'Fonte': 'H4D'
        })
    
    if uso:
        resumo_data.append({
            'Pilar': '3. Uso',
            'Indicador': 'Alunos usando IA',
            'Percentual': f"{uso['indice']:.1f}%",
            'Fonte': 'G6'
        })
    
    if triplo_deficit:
        resumo_data.append({
            'Pilar': 'ÍNDICE GERAL',
            'Indicador': 'Prontidão para IA',
            'Percentual': f"{triplo_deficit['indice_prontidao']:.1f}%",
            'Fonte': 'Calculado'
        })
        resumo_data.append({
            'Pilar': 'DÉFICIT',
            'Indicador': 'Triplo Déficit Total',
            'Percentual': f"{triplo_deficit['deficit_total']:.1f} pp",
            'Fonte': 'Calculado'
        })
    
    if resumo_data:
        df_resumo = pd.DataFrame(resumo_data)
        csv_path = f"{output_dir}/resumo_executivo.csv"
        df_resumo.to_csv(csv_path, index=False, encoding='utf-8-sig')
        print(f"✅ Resumo executivo salvo: {csv_path}")
    
    # Salvar comparação regional
    if comp_regional is not None:
        csv_regional_path = f"{output_dir}/comparacao_regional.csv"
        comp_regional.to_csv(csv_regional_path, index=False, encoding='utf-8-sig')
        print(f"✅ Comparação regional salva: {csv_regional_path}")
    
    return relatorio


def main():
    """
    Função principal do consolidador
    """
    print("\n" + "="*80)
    print("CONSOLIDADOR - TRIPLO DÉFICIT TECNOLÓGICO")
    print("TIC Educação 2024")
    print("="*80)
    
    resultados_dir = './resultados'
    
    # Carregar resultados
    resultados = {}
    
    # A8 - Acesso
    a8_data = carregar_resultado(f'{resultados_dir}/a8_acesso_completo.json')
    if a8_data:
        resultados['a8'] = a8_data
        print(f"✅ A8 carregado (Acesso)")
    
    # A3 - Velocidade
    a3_data = carregar_resultado(f'{resultados_dir}/a3_velocidade_completo.json')
    if a3_data:
        resultados['a3'] = a3_data
        print(f"✅ A3 carregado (Velocidade)")

    # B4A - Proporção (ADICIONE ESTAS LINHAS)
    b4a_data = carregar_resultado(f'{resultados_dir}/b4a_proporcao_completo.json')
    if b4a_data:
        resultados['b4a'] = b4a_data
        print(f"✅ B4A carregado (Proporção)")
    
    # G6 - Uso de IA
    g6_data = carregar_resultado(f'{resultados_dir}/g6_uso_ia_completo.json')
    if g6_data:
        resultados['g6'] = g6_data
        print(f"✅ G6 carregado (Uso de IA)")
    
    # H4D - Orientação
    h4d_data = carregar_resultado(f'{resultados_dir}/h4d_orientacao_ia_completo.json')
    if h4d_data:
        resultados['h4d'] = h4d_data
        print(f"✅ H4D carregado (Orientação)")
    
    # Gerar relatório final
    if len(resultados) >= 5:
        relatorio = gerar_relatorio_final(resultados)
        
        print("\n" + "="*80)
        print("✅ CONSOLIDAÇÃO CONCLUÍDA!")
        print("="*80)
        print(f"\n📊 Total de análises: {len(resultados)}")
        print(f"📁 Arquivos gerados em: {resultados_dir}/")
        
        # Mostrar principais achados se disponíveis
        if relatorio.get('triplo_deficit'):
            print(f"\n🎯 ÍNDICE DE PRONTIDÃO: {relatorio['triplo_deficit']['indice_prontidao']:.1f}%")
            print(f"⚠️  DÉFICIT TOTAL: {relatorio['triplo_deficit']['deficit_total']:.1f} pontos")
        
        if relatorio.get('paradoxos'):
            print(f"\n🚨 PARADOXOS IDENTIFICADOS: {len(relatorio['paradoxos'])}")
            for p in relatorio['paradoxos']:
                print(f"   • {p['tipo']}: GAP de {p['gap']:.1f} pontos")
        
    else:
        print("\n⚠️  Análises incompletas.")
        print(f"   Encontradas: {len(resultados)}/4")
        print(f"   Necessárias: A8, A3, G6, H4D")
        print("\nExecute os scripts de análise primeiro:")
        print("  • python analise_a8_acesso_FINAL.py")
        print("  • python analise_a3_velocidade_FINAL.py")
        print("  • python analise_g6_uso_ia_FINAL.py")
        print("  • python analise_h4d_orientacao_ia_FINAL.py")


if __name__ == "__main__":
    main()