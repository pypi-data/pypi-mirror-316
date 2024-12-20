import pytest
import pandas as pd
from datalib_ym import DataLoader, DataTransformer

@pytest.fixture
def sample_data():
    return pd.DataFrame({
        'A': [1, 2, 3, 4, 5],
        'B': [5, 4, 3, 2, 1],
        'C': [1, 1, 2, 2, 3]
    })

def test_data_loader(tmp_path):
    loader = DataLoader()
    data = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
    csv_file = tmp_path / "test.csv"
    data.to_csv(csv_file, index=False)
    
    loaded_data = loader.load_csv(csv_file)
    assert loaded_data.equals(data)

def test_data_transformer_normalize(sample_data):
    transformer = DataTransformer()
    normalized_data = transformer.normalize(sample_data)
    assert normalized_data.mean().round(6).equals(pd.Series([0, 0, 0]))
    assert normalized_data.std().round(6).equals(pd.Series([1, 1, 1]))

def test_data_transformer_handle_missing_values(sample_data):
    transformer = DataTransformer()
    sample_data.loc[0, 'A'] = None
    filled_data = transformer.handle_missing_values(sample_data)
    assert filled_data['A'].isnull().sum() == 0

