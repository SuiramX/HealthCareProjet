import pytest
from src.patient import Patient

@pytest.mark.unit
class TestPatientUnit:
    """Test individual Patient methods in isolation"""
    
    @pytest.fixture
    def patient_mgr(self):
        return Patient()
    
    def test_add_patient_creates_entry(self, patient_mgr):
        """Test: add_patient creates a patient entry"""
        result = patient_mgr.add_patient("John", 45)
        assert result == 1
    
    def test_add_patient_increments_id(self, patient_mgr):
        """Test: IDs increment correctly"""
        id1 = patient_mgr.add_patient("John", 45)
        id2 = patient_mgr.add_patient("Jane", 30)
        assert id2 == id1 + 1