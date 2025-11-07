import pandas as pd
import joblib
from src.utils import clean_text
from sklearn.feature_extraction.text import TfidfVectorizer
from pathlib import Path
from typing import List, Dict, Any

# --- 1. Constantes e Configurações (Clean Code: Centralizar configuração) ---

# Caminhos (usando pathlib para ser independente de SO)
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
ARTIFACTS_DIR = BASE_DIR / "artifacts"

# Paths de Input/Output
INPUT_CSV_PATH = DATA_DIR / "postings.csv"
OUTPUT_DF_PATH = ARTIFACTS_DIR / "clean_postings.parquet"
OUTPUT_VECTORIZER_PATH = ARTIFACTS_DIR / "tfidf_vectorizer.pkl"
OUTPUT_MATRIX_PATH = ARTIFACTS_DIR / "vagas_matrix.pkl"

# Parâmetros do Modelo (Clean Code: Evitar 'magic numbers')
TFIDF_MAX_FEATURES = 5000
TEXT_COLS = ['title', 'description', 'skills_desc']
FILTER_COLS = [
    'formatted_experience_level', 
    'normalized_salary', 
    'remote_allowed'
]
DISPLAY_COLS = [
    'job_id', 
    'title', 
    'company_name', 
    'job_posting_url', 
    'med_salary', 
    'location'
]


# --- 2. Funções de Responsabilidade Única (SRP) ---

def load_data(path: Path) -> pd.DataFrame:
    """Carrega os dados do CSV."""
    print(f"Carregando dados de {path}...")
    try:
        df = pd.read_csv(path)
        print("Dados carregados com sucesso.")
        return df
    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado em {path}")
        raise


def normalize_filter_features(df: pd.DataFrame) -> pd.DataFrame:
    """Limpa e padroniza as colunas que serão usadas para filtragem."""
    print("Normalizando features de filtro...")
    
    # Nível de Experiência
    # (Exemplo: Mapeia diferentes strings para valores padronizados)
    exp_map = {
        'Entry level': 'junior',
        'Associate': 'pleno',
        'Mid-Senior level': 'senior',
        'Director': 'senior', # Exemplo de agrupamento
        'Executive': 'senior' # Exemplo de agrupamento
    }
    df['formatted_experience_level'] = df['formatted_experience_level'].map(exp_map).fillna('na')
    
    # Salário
    df['normalized_salary'] = pd.to_numeric(df['normalized_salary'], errors='coerce').fillna(0)
    
    # Remoto
    df['remote_allowed'] = df['remote_allowed'].fillna(False).astype(bool)
    
    print("Features de filtro normalizadas.")
    return df

def create_combined_text_feature(df: pd.DataFrame, text_cols: List[str]) -> pd.DataFrame:
    """Cria a 'super-coluna' de texto para o TF-IDF."""
    print(f"Combinando colunas de texto: {text_cols}...")
    
    df_text = df[text_cols].fillna("")
    
    # Aplica a limpeza
    for col in text_cols:
        df_text[col] = df_text[col].apply(clean_text)
        
    # Cria a "super-coluna"
    df['texto_vaga'] = df_text.apply(lambda row: ' '.join(row), axis=1)
    
    print("Coluna 'texto_vaga' criada.")
    return df


def train_vectorizer(text_series: pd.Series, max_features: int) -> TfidfVectorizer:
    """"Treina" (ajusta) o TfidfVectorizer."""
    print(f"Treinando TfidfVectorizer com max_features={max_features}...")
    
    # O TfidfVectorizer cuida de stopwords e lowercase (redundância OK)
    vectorizer = TfidfVectorizer(
        max_features=max_features,
        stop_words='english',
        lowercase=True
    )
    vectorizer.fit(text_series)
    
    print("Vetorizador treinado.")
    return vectorizer


def save_artifacts(artifacts: Dict[str, Any]):
    """Salva todos os artefatos de saída (DF, Vetorizador, Matriz)."""
    print("Salvando artefatos...")
    
    # Garante que o diretório de artefatos exista
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

    # Salva o DataFrame limpo
    try:
        # Colunas de filtro + Colunas de display + ID
        all_cols_to_save = list(set(['job_id'] + FILTER_COLS + DISPLAY_COLS))
        
        # Garante que as colunas existem antes de salvar
        cols_existentes = [col for col in all_cols_to_save if col in artifacts['df'].columns]
        
        df_final = artifacts['df'][cols_existentes]
        df_final.to_parquet(OUTPUT_DF_PATH, index=False)
        print(f"DataFrame limpo salvo em {OUTPUT_DF_PATH}")

        # Salva o Vetorizador
        joblib.dump(artifacts['vectorizer'], OUTPUT_VECTORIZER_PATH)
        print(f"Vetorizador salvo em {OUTPUT_VECTORIZER_PATH}")
        
        # Salva a Matriz TF-IDF
        joblib.dump(artifacts['matrix'], OUTPUT_MATRIX_PATH)
        print(f"Matriz TF-IDF salva em {OUTPUT_MATRIX_PATH}")

    except Exception as e:
        print(f"Erro ao salvar artefatos: {e}")
        raise

# --- 3. Orquestrador (main) ---

def main():
    """Orquestra o pipeline completo da Fase Offline."""
    
    # 1. Carregar
    df_vagas = load_data(INPUT_CSV_PATH)
    
    # 2. Limpar (Filtros)
    df_vagas = normalize_filter_features(df_vagas)
    
    # 3. Limpar (Texto)
    df_vagas = create_combined_text_feature(df_vagas, TEXT_COLS)
    
    # 4. Treinar
    vectorizer = train_vectorizer(df_vagas['texto_vaga'], TFIDF_MAX_FEATURES)
    
    # 5. Transformar
    vagas_matrix = vectorizer.transform(df_vagas['texto_vaga'])
    
    # 6. Salvar
    artifacts_to_save = {
        'df': df_vagas,
        'vectorizer': vectorizer,
        'matrix': vagas_matrix
    }
    save_artifacts(artifacts_to_save)
    
    print("\n--- Pré-processamento (Fase Offline) concluído! ---")
    print(f"Artefatos salvos em: {ARTIFACTS_DIR}")


# --- Ponto de Entrada (Clean Code: Permite importação vs. execução) ---
if __name__ == "__main__":
    main()