import pytest
from datetime import datetime, timedelta
from src.patient import Patient

@pytest.mark.unit
class TestPatientUnit:
    """Test individual Patient methods in isolation"""
    
    @pytest.fixture
    def patient_mgr(self):
        return Patient()
    
    # --- Tests Addition ---
    
    def test_add_patient_creates_entry(self, patient_mgr):
        """Test: add_patient creates a patient entry"""
        result = patient_mgr.add_patient("John", "Doe", "01/01/1990", "123456789012345")
        assert result == 1
    
    def test_add_patient_increments_id(self, patient_mgr):
        """Test: IDs increment correctly"""
        id1 = patient_mgr.add_patient("John", "Doe", "01/01/1990", "123456789012345")
        id2 = patient_mgr.add_patient("Jane", "Doe", "02/02/1980", "123456789012346")
        assert id2 == id1 + 1

    def test_add_patient_missing_nom_prenom(self, patient_mgr):
        """Test: Nom et prénom obligatoires et sans chiffres"""
        with pytest.raises(ValueError, match="Le nom et le prénom sont obligatoires."):
            patient_mgr.add_patient("", "Jean", "01/01/1990", "123456789012345")
            
        with pytest.raises(ValueError, match="Le nom et le prénom ne doivent pas contenir de chiffres."):
            patient_mgr.add_patient("Dup0nt", "Jean", "01/01/1990", "123456789012345")

    def test_add_patient_invalid_dob(self, patient_mgr):
        """Test: Format et validité de la date de naissance"""
        with pytest.raises(ValueError, match="La date de naissance doit être au format DD/MM/YYYY."):
            patient_mgr.add_patient("Dupont", "Jean", "1990-01-01", "123456789012345")
            
        future_date = (datetime.now() + timedelta(days=1)).strftime("%d/%m/%Y")
        with pytest.raises(ValueError, match="La date de naissance ne peut pas être dans le futur."):
            patient_mgr.add_patient("Dupont", "Jean", future_date, "123456789012345")

    def test_add_patient_invalid_ssn(self, patient_mgr):
        """Test: Numéro de sécu à 15 chiffres et unique"""
        with pytest.raises(ValueError, match="Le numéro de sécurité sociale doit contenir exactement 15 chiffres."):
            patient_mgr.add_patient("Dupont", "Jean", "01/01/1990", "123")
            
        patient_mgr.add_patient("Dupont", "Jean", "01/01/1990", "123456789012345")
        with pytest.raises(ValueError, match="Ce numéro de sécurité sociale existe déjà."):
            patient_mgr.add_patient("Martin", "Paul", "02/02/1980", "123456789012345")

    def test_add_patient_age_calculation(self, patient_mgr):
        """Test: Génération et vérification de l'âge"""
        id1 = patient_mgr.add_patient("Dupont", "Jean", "01/01/2000", "123456789012345")
        patient = patient_mgr.get_patient_info(id1)
        assert patient['age'] >= 26
        
        with pytest.raises(ValueError, match="L'âge fourni ne correspond pas à la date de naissance."):
            patient_mgr.add_patient("Martin", "Paul", "01/01/2000", "123456789012346", age=10)

    # --- Tests Modification ---

    def test_update_patient_valid(self, patient_mgr):
        """Test: Mise à jour classique d'un dossier et génération d'historique"""
        id1 = patient_mgr.add_patient("Doe", "John", "01/01/1990", "123456789012345")
        patient_mgr.update_patient(id1, phone="0612345678", email="contact@doe.com")
        
        patient = patient_mgr.get_patient_info(id1)
        assert patient['phone'] == "0612345678"
        assert patient['email'] == "contact@doe.com"
        assert len(patient['history']) == 1
        assert "Modification: phone: 0612345678" in patient['history'][0]

    def test_update_patient_ssn_unchangeable(self, patient_mgr):
        """Test: Impossibilité de modifier le numéro de sécurité sociale (immuable)"""
        id1 = patient_mgr.add_patient("Doe", "John", "01/01/1990", "123456789012345")
        with pytest.raises(ValueError, match="L'identifiant unique \(numéro de sécu\) ne peut pas être modifié."):
            patient_mgr.update_patient(id1, numero_secu="987654321098765")

    def test_update_patient_invalid_phone(self, patient_mgr):
        """Test: Validation basique du téléphone lors de la modification"""
        id1 = patient_mgr.add_patient("Doe", "John", "01/01/1990", "123456789012345")
        with pytest.raises(ValueError, match="Le format du numéro de téléphone est invalide."):
            patient_mgr.update_patient(id1, phone="123")

    def test_update_unknown_patient(self, patient_mgr):
        """Test: Modification d'un patient inexistant"""
        with pytest.raises(ValueError, match="Patient introuvable."):
            patient_mgr.update_patient(999, phone="0612345678")

    # --- Tests Archivage ---

    def test_archive_patient_success(self, patient_mgr):
        """Test: L'archivage change le statut et ajoute un historique, sans supprimer l'entrée"""
        id1 = patient_mgr.add_patient("Doe", "John", "01/01/1990", "123456789012345")
        patient_mgr.archive_patient(id1)
        
        patient = patient_mgr.get_patient_info(id1)
        assert patient['status'] == 'archived'
        assert len(patient['history']) == 1
        assert "Archivage" in patient['history'][0]
        
    def test_archive_already_archived_patient(self, patient_mgr):
        """Test: Impossible d'archiver un dossier déjà archivé"""
        id1 = patient_mgr.add_patient("Doe", "John", "01/01/1990", "123456789012345")
        patient_mgr.archive_patient(id1)
        
        with pytest.raises(ValueError, match="Ce dossier est déjà archivé."):
            patient_mgr.archive_patient(id1)
            
    def test_archive_unknown_patient(self, patient_mgr):
        """Test: Archivage d'un patient inexistant"""
        with pytest.raises(ValueError, match="Patient introuvable."):
            patient_mgr.archive_patient(999)