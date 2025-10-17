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

## 📁 Files Included vs. Excluded

### ✅ Included in Repository:

**Analysis Results:**
- `01_analises/resultados/*.csv` - Small analysis results (<1KB each)
- `02_clustering_project/dados_processados/resultados_clustering.csv` - Final clustering results (262 bytes)
- All JSON metadata and text reports

**Visualizations:**
- 4 PNG charts (PCA, distance matrix, dendrogram, clustering results)

**Scripts:**
- All Python scripts for data extraction, preparation, and analysis
- Jupyter notebooks

### ❌ Excluded (Can be Regenerated):

**Intermediate Files:**
- `escolas_2024_consolidado.csv` (47KB) - Regenerate with `01_extrair_dados_escolas.py`
- `regioes_preparado_para_clustering.csv` (20KB) - Regenerate with `02_preparacao_regioes.py`
- `sheets_individuais/*.csv` (15 files, ~120KB total) - Regenerate with extraction script

**Raw Data:**
- `*.xlsx` files - Download from [CETIC.br](https://cetic.br/pt/arquivos/educacao/2024/)

### 🔄 To Reproduce All Files:
```bash
# 1. Get the raw data (place in project root)
# Download from CETIC.br

# 2. Run the pipeline
python 02_clustering_project/01_extrair_dados_escolas.py
python 02_clustering_project/02_preparacao_regioes.py
python 02_clustering_project/03_clustering_regioes.py

# All intermediate files will be regenerated
```

**Total repository size:** ~2-3 MB (mostly visualizations)
**Excluded data size:** ~20-50 MB (downloadable from source)

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