"""
PROJETO: Cluster Analysis - Perfis Digitais das Escolas Brasileiras
FASE 3: CLUSTERING DAS REGIÕES

Este script:
1. Carrega dados preparados (5 regiões, 162 features)
2. Aplica PCA para redução de dimensionalidade
3. Executa múltiplos algoritmos de clustering
4. Visualiza resultados
5. Interpreta clusters encontrados

Autor: [Seu nome]
Data: 2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.metrics import silhouette_score, davies_bouldin_score
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.spatial.distance import pdist, squareform
import warnings
warnings.filterwarnings('ignore')

# Configurações de visualização
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10

print("="*80)
print("CLUSTER ANALYSIS - REGIÕES BRASILEIRAS")
print("Perfis Digitais da Educação")
print("="*80)

# ============================================================================
# 1. CARREGAR DADOS
# ============================================================================

print("\n" + "-"*80)
print("1. CARREGANDO DADOS")
print("-"*80)

df = pd.read_csv('dados_processados/regioes_preparado_para_clustering.csv')

# Separar features e labels
regioes = df['observacao_id'].str.replace('REGIÃO_', '').values
X = df.drop('observacao_id', axis=1).values

print(f"\n✓ Dados carregados:")
print(f"  - Regiões: {len(regioes)}")
print(f"  - Features: {X.shape[1]}")
print(f"\nRegiões:")
for i, regiao in enumerate(regioes, 1):
    print(f"  {i}. {regiao}")

# ============================================================================
# 2. ANÁLISE DE COMPONENTES PRINCIPAIS (PCA)
# ============================================================================

print("\n" + "-"*80)
print("2. REDUÇÃO DE DIMENSIONALIDADE - PCA")
print("-"*80)

# PCA completo para ver variância explicada
pca_full = PCA()
pca_full.fit(X)

# Variância explicada cumulativa
variance_cumsum = np.cumsum(pca_full.explained_variance_ratio_)

# Encontrar número de componentes para 90% e 95% de variância
n_comp_90 = np.argmax(variance_cumsum >= 0.90) + 1
n_comp_95 = np.argmax(variance_cumsum >= 0.95) + 1

print(f"\nVariância explicada:")
print(f"  - {n_comp_90} componentes explicam 90% da variância")
print(f"  - {n_comp_95} componentes explicam 95% da variância")
print(f"  - Primeiros 5 componentes: {variance_cumsum[4]*100:.1f}%")

# Aplicar PCA com número reduzido de componentes
n_components = min(n_comp_90, 4)  # Máximo 4 para 5 observações
pca = PCA(n_components=n_components)
X_pca = pca.fit_transform(X)

print(f"\n✓ PCA aplicado:")
print(f"  - Componentes selecionados: {n_components}")
print(f"  - Variância explicada total: {sum(pca.explained_variance_ratio_)*100:.2f}%")

# Visualizar variância explicada
fig, axes = plt.subplots(1, 2, figsize=(15, 5))

# Scree plot
axes[0].bar(range(1, min(21, len(pca_full.explained_variance_ratio_)+1)), 
            pca_full.explained_variance_ratio_[:20])
axes[0].set_xlabel('Componente Principal')
axes[0].set_ylabel('Variância Explicada')
axes[0].set_title('Scree Plot - Variância por Componente')
axes[0].axhline(y=0.1, color='r', linestyle='--', label='10% threshold')
axes[0].legend()

# Variância cumulativa
axes[1].plot(range(1, min(21, len(variance_cumsum)+1)), variance_cumsum[:20], 'bo-')
axes[1].axhline(y=0.90, color='r', linestyle='--', label='90%')
axes[1].axhline(y=0.95, color='g', linestyle='--', label='95%')
axes[1].set_xlabel('Número de Componentes')
axes[1].set_ylabel('Variância Explicada Cumulativa')
axes[1].set_title('Variância Cumulativa')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('dados_processados/01_pca_variance.png', dpi=300, bbox_inches='tight')
print("\n✓ Gráfico salvo: dados_processados/01_pca_variance.png")
plt.close()

# ============================================================================
# 3. MATRIZ DE DISTÂNCIAS
# ============================================================================

print("\n" + "-"*80)
print("3. ANÁLISE DE DISTÂNCIAS ENTRE REGIÕES")
print("-"*80)

# Calcular matriz de distâncias Euclidianas
distances = squareform(pdist(X_pca, metric='euclidean'))
dist_df = pd.DataFrame(distances, index=regioes, columns=regioes)

print("\nMatriz de Distâncias (resumo):")
print(dist_df.round(2))

# Heatmap de distâncias
plt.figure(figsize=(10, 8))
sns.heatmap(dist_df, annot=True, fmt='.2f', cmap='YlOrRd', 
            square=True, cbar_kws={'label': 'Distância Euclidiana'})
plt.title('Matriz de Distâncias Entre Regiões\n(Baseada em PCA)', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('dados_processados/02_distance_matrix.png', dpi=300, bbox_inches='tight')
print("\n✓ Heatmap salvo: dados_processados/02_distance_matrix.png")
plt.close()

# Identificar pares mais similares e mais diferentes
dist_flat = dist_df.values[np.triu_indices_from(dist_df.values, k=1)]
min_idx = np.unravel_index(np.argmin(distances + np.eye(5)*1000), distances.shape)
max_idx = np.unravel_index(np.argmax(distances), distances.shape)

print(f"\nRegiões MAIS SIMILARES: {regioes[min_idx[0]]} ↔ {regioes[min_idx[1]]}")
print(f"  Distância: {distances[min_idx]:.2f}")

print(f"\nRegiões MAIS DIFERENTES: {regioes[max_idx[0]]} ↔ {regioes[max_idx[1]]}")
print(f"  Distância: {distances[max_idx]:.2f}")

# ============================================================================
# 4. CLUSTERING HIERÁRQUICO
# ============================================================================

print("\n" + "-"*80)
print("4. CLUSTERING HIERÁRQUICO")
print("-"*80)

# Calcular linkage
linkage_matrix = linkage(X_pca, method='ward')

# Plotar dendrograma
plt.figure(figsize=(12, 6))
dendrogram(linkage_matrix, 
           labels=regioes,
           leaf_font_size=12,
           color_threshold=0)
plt.title('Dendrograma - Clustering Hierárquico das Regiões', 
          fontsize=14, fontweight='bold')
plt.xlabel('Região', fontsize=12)
plt.ylabel('Distância (Ward)', fontsize=12)
plt.axhline(y=linkage_matrix[-2, 2], color='r', linestyle='--', 
            label=f'Corte para 2 clusters')
plt.axhline(y=linkage_matrix[-3, 2], color='g', linestyle='--', 
            label=f'Corte para 3 clusters')
plt.legend()
plt.tight_layout()
plt.savefig('dados_processados/03_dendrogram.png', dpi=300, bbox_inches='tight')
print("\n✓ Dendrograma salvo: dados_processados/03_dendrogram.png")
plt.close()

# Aplicar clustering hierárquico com diferentes números de clusters
print("\nTestando diferentes números de clusters:")
for n_clusters in [2, 3]:
    hier = AgglomerativeClustering(n_clusters=n_clusters)
    labels = hier.fit_predict(X_pca)
    
    # Silhouette score (só funciona com 2+ clusters)
    if n_clusters > 1:
        sil_score = silhouette_score(X_pca, labels)
        db_score = davies_bouldin_score(X_pca, labels)
        print(f"\n  {n_clusters} clusters:")
        print(f"    - Silhouette Score: {sil_score:.3f} (quanto maior, melhor)")
        print(f"    - Davies-Bouldin Score: {db_score:.3f} (quanto menor, melhor)")
        
        # Mostrar composição
        for cluster_id in range(n_clusters):
            members = regioes[labels == cluster_id]
            print(f"    - Cluster {cluster_id+1}: {', '.join(members)}")

# ============================================================================
# 5. K-MEANS CLUSTERING
# ============================================================================

print("\n" + "-"*80)
print("5. K-MEANS CLUSTERING")
print("-"*80)

# Testar K=2 e K=3
resultados_kmeans = {}

for k in [2, 3]:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=50)
    labels = kmeans.fit_predict(X_pca)
    
    sil_score = silhouette_score(X_pca, labels)
    db_score = davies_bouldin_score(X_pca, labels)
    inertia = kmeans.inertia_
    
    resultados_kmeans[k] = {
        'labels': labels,
        'silhouette': sil_score,
        'davies_bouldin': db_score,
        'inertia': inertia,
        'centers': kmeans.cluster_centers_
    }
    
    print(f"\nK-Means com K={k}:")
    print(f"  - Silhouette Score: {sil_score:.3f}")
    print(f"  - Davies-Bouldin Score: {db_score:.3f}")
    print(f"  - Inertia: {inertia:.2f}")
    
    for cluster_id in range(k):
        members = regioes[labels == cluster_id]
        print(f"  - Cluster {cluster_id+1}: {', '.join(members)}")

# Escolher melhor K (maior silhouette)
best_k = max(resultados_kmeans.keys(), 
             key=lambda k: resultados_kmeans[k]['silhouette'])
print(f"\n✓ Melhor configuração: K={best_k}")
print(f"  Silhouette Score: {resultados_kmeans[best_k]['silhouette']:.3f}")

best_labels = resultados_kmeans[best_k]['labels']

# ============================================================================
# 6. VISUALIZAÇÃO DOS CLUSTERS
# ============================================================================

print("\n" + "-"*80)
print("6. VISUALIZAÇÃO DOS CLUSTERS")
print("-"*80)

# Criar figura com múltiplos subplots
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Plot 1: PCA 2D com clusters do K-means
if X_pca.shape[1] >= 2:
    scatter = axes[0].scatter(X_pca[:, 0], X_pca[:, 1], 
                             c=best_labels, s=500, alpha=0.6, 
                             cmap='viridis', edgecolors='black', linewidth=2)
    
    # Adicionar labels
    for i, regiao in enumerate(regioes):
        axes[0].annotate(regiao, (X_pca[i, 0], X_pca[i, 1]),
                        fontsize=11, fontweight='bold',
                        ha='center', va='center')
    
    # Adicionar centróides
    centers = resultados_kmeans[best_k]['centers']
    axes[0].scatter(centers[:, 0], centers[:, 1],
                   c='red', s=300, alpha=0.8, marker='X',
                   edgecolors='black', linewidth=2,
                   label='Centróides')
    
    axes[0].set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]*100:.1f}% var.)', 
                      fontsize=12)
    axes[0].set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]*100:.1f}% var.)', 
                      fontsize=12)
    axes[0].set_title(f'Clusters das Regiões (K-Means, K={best_k})', 
                     fontsize=14, fontweight='bold')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

# Plot 2: Heatmap de features mais importantes por região
# Selecionar top 15 features com maior variância
feature_vars = df.drop('observacao_id', axis=1).var().sort_values(ascending=False)
top_features = feature_vars.head(15).index.tolist()

data_top = df[['observacao_id'] + top_features].set_index('observacao_id')
data_top.index = data_top.index.str.replace('REGIÃO_', '')

sns.heatmap(data_top.T, annot=True, fmt='.2f', cmap='RdYlGn', 
            ax=axes[1], cbar_kws={'label': 'Valor Normalizado'})
axes[1].set_title('Top 15 Features Mais Variáveis por Região', 
                 fontsize=14, fontweight='bold')
axes[1].set_xlabel('Região', fontsize=12)
axes[1].set_ylabel('Feature', fontsize=12)

plt.tight_layout()
plt.savefig('dados_processados/04_clustering_results.png', dpi=300, bbox_inches='tight')
print("\n✓ Visualização salva: dados_processados/04_clustering_results.png")
plt.close()

# ============================================================================
# 7. INTERPRETAÇÃO DOS CLUSTERS
# ============================================================================

print("\n" + "="*80)
print("7. INTERPRETAÇÃO DOS CLUSTERS")
print("="*80)

# Carregar dados originais (não normalizados) para interpretação
df_original = pd.read_csv('dados_processados/escolas_2024_consolidado.csv')
df_regioes_orig = df_original[df_original['observacao_id'].str.contains('REGIÃO_', na=False)]
df_regioes_orig = df_regioes_orig[~df_regioes_orig['observacao_id'].str.contains('TOTAL')]

# Adicionar labels de cluster
df_regioes_orig['cluster'] = best_labels
df_regioes_orig['regiao'] = df_regioes_orig['observacao_id'].str.replace('REGIÃO_', '')

print(f"\nClustering final (K={best_k}):")
print("-"*80)

for cluster_id in range(best_k):
    cluster_regioes = df_regioes_orig[df_regioes_orig['cluster'] == cluster_id]['regiao'].values
    print(f"\n{'='*80}")
    print(f"CLUSTER {cluster_id + 1}: {', '.join(cluster_regioes)}")
    print(f"{'='*80}")
    
    # Selecionar dados deste cluster
    cluster_data = df_regioes_orig[df_regioes_orig['cluster'] == cluster_id]
    
    # Identificar features distintivas (comparar com média global)
    numeric_cols = cluster_data.select_dtypes(include=[np.number]).columns
    numeric_cols = [c for c in numeric_cols if c not in ['cluster']]
    
    # Calcular médias do cluster vs global
    cluster_means = cluster_data[numeric_cols].mean()
    global_means = df_regioes_orig[numeric_cols].mean()
    
    # Diferenças relativas
    rel_diff = ((cluster_means - global_means) / (global_means + 1)) * 100
    rel_diff = rel_diff.sort_values(ascending=False)
    
    print(f"\nCaracterísticas distintivas (TOP 10 acima da média):")
    for feat in rel_diff.head(10).index:
        val = cluster_means[feat]
        global_val = global_means[feat]
        diff = rel_diff[feat]
        if diff > 5:  # Apenas diferenças > 5%
            print(f"  ↑ {feat[:60]}")
            print(f"     Cluster: {val:.0f} | Média: {global_val:.0f} | +{diff:.1f}%")
    
    print(f"\nCaracterísticas distintivas (TOP 10 abaixo da média):")
    for feat in rel_diff.tail(10).index:
        val = cluster_means[feat]
        global_val = global_means[feat]
        diff = rel_diff[feat]
        if diff < -5:  # Apenas diferenças < -5%
            print(f"  ↓ {feat[:60]}")
            print(f"     Cluster: {val:.0f} | Média: {global_val:.0f} | {diff:.1f}%")

# ============================================================================
# 8. SALVAR RESULTADOS
# ============================================================================

print("\n" + "="*80)
print("8. SALVANDO RESULTADOS")
print("="*80)

# Criar DataFrame com resultados
resultados_df = pd.DataFrame({
    'regiao': regioes,
    'cluster': best_labels + 1,  # +1 para ficar 1-indexed
    'PC1': X_pca[:, 0],
    'PC2': X_pca[:, 1] if X_pca.shape[1] > 1 else 0
})

output_file = 'dados_processados/resultados_clustering.csv'
resultados_df.to_csv(output_file, index=False)
print(f"\n✓ Resultados salvos: {output_file}")

# Salvar relatório textual
with open('dados_processados/relatorio_clustering.txt', 'w', encoding='utf-8') as f:
    f.write("="*80 + "\n")
    f.write("RELATÓRIO DE CLUSTER ANALYSIS - REGIÕES BRASILEIRAS\n")
    f.write("Perfis Digitais da Educação\n")
    f.write("="*80 + "\n\n")
    
    f.write(f"Dados analisados: 5 regiões, 162 features\n")
    f.write(f"Método: K-Means com PCA\n")
    f.write(f"Número de clusters: {best_k}\n")
    f.write(f"Silhouette Score: {resultados_kmeans[best_k]['silhouette']:.3f}\n\n")
    
    f.write("COMPOSIÇÃO DOS CLUSTERS:\n")
    f.write("-"*80 + "\n\n")
    
    for cluster_id in range(best_k):
        members = regioes[best_labels == cluster_id]
        f.write(f"Cluster {cluster_id+1}: {', '.join(members)}\n\n")

print("✓ Relatório salvo: dados_processados/relatorio_clustering.txt")

# ============================================================================
# RESUMO FINAL
# ============================================================================

print("\n" + "="*80)
print("✓ CLUSTER ANALYSIS CONCLUÍDA!")
print("="*80)

print("\nArquivos gerados:")
print("  1. dados_processados/01_pca_variance.png")
print("  2. dados_processados/02_distance_matrix.png")
print("  3. dados_processados/03_dendrogram.png")
print("  4. dados_processados/04_clustering_results.png")
print("  5. dados_processados/resultados_clustering.csv")
print("  6. dados_processados/relatorio_clustering.txt")

print(f"\nMelhor configuração: K={best_k} clusters")
print(f"Silhouette Score: {resultados_kmeans[best_k]['silhouette']:.3f}")

print("\nPróximos passos:")
print("  1. Revisar visualizações geradas")
print("  2. Interpretar significado dos clusters")
print("  3. Criar dashboard interativo (opcional)")
print("  4. Expandir análise com mais dados (Alunos, anos anteriores)")

print("\n" + "="*80)