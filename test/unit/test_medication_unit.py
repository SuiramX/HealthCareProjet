import pytest
from src.medication import Medication

@pytest.mark.unit
class TestMedicationUnit:
    """Test individual Patient methods in isolation"""
    
    @pytest.fixture
    def medication_mgr(self):
        return Medication()
    
    def test_read_interactions(self, medication_mgr):
        """Test: les interactions sont bien lues"""
        result = medication_mgr.interactions_df
        assert result.shape[0] > 2
    