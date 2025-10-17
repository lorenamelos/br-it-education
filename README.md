## 📂 Project Structure
```
02_clustering_project/
├── 01_extrair_dados_escolas.py       # Extract data from Excel
├── 02_preparacao_regioes.py          # Clean and prepare regional data
├── 03_clustering_regioes.py          # PCA and clustering analysis
│
├── dados_processados/
│   ├── 01_pca_variance.png           # PCA variance explained
│   ├── 02_distance_matrix.png        # Regional distance heatmap
│   ├── 03_dendrogram.png             # Hierarchical clustering
│   ├── 04_clustering_results.png     # Final cluster visualization
│   │
│   ├── resultados_clustering.csv     # Clustering results (5 regions)
│   ├── regioes_preparado_para_clustering.csv  # Prepared data
│   ├── metadados.json                # Extraction metadata
│   └── relatorio_clustering.txt      # Analysis report
│
└── README.md
```

## 📥 Data Files (Not Included)

Raw data files are **not included** in this repository due to size constraints:

- ❌ `tic_educacao_2024_escolas_tabela_total_v1.0.xlsx` (~15 MB)
- ❌ `escolas_2024_consolidado.csv` (~5 MB)
- ❌ `escolas_2024_consolidado.json` (~8 MB)
- ❌ `sheets_individuais/` folder

### To reproduce the analysis:

1. Download the TIC Educação 2024 dataset:
```
   https://cetic.br/pt/arquivos/educacao/2024/escolas
```

2. Place the Excel file in the project root:
```
   02_clustering_project/
   └── tic_educacao_2024_escolas_tabela_total_v1.0.xlsx
```

3. Run the pipeline:
```bash
   python 01_extrair_dados_escolas.py
   python 02_preparacao_regioes.py
   python 03_clustering_regioes.py
```

All intermediate files will be generated automatically.