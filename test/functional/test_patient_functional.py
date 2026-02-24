import pytest
from datetime import datetime
from src.patient import Patient

@pytest.fixture
def patient_manager():
    return Patient()

def test_fonctionnel_ajout_dossier_patient(patient_manager):
    """
    Scénario du plan de test: Ajout d'un dossier patient
    Un utilisateur remplit une fiche patient, clique sur enregistrer.
    Le dossier apparaît dans la liste.
    """
    pid = patient_manager.add_patient(
        nom="Dupont",
        prenom="Marie",
        date_naissance="15/05/1985",
        numero_secu="285057512345678",
        email="marie.dupont@test.com",
        phone="0601020304"
    )
    
    info = patient_manager.get_patient_info(pid)
    assert info["nom"] == "Dupont"
    assert info["status"] == "active"
    
    all_patients = patient_manager.list_all_patients()
    assert pid in all_patients

def test_fonctionnel_modification_dossier_patient(patient_manager):
    """
    Scénario du plan de test: Modification d'un dossier patient
    Un infirmier modifie l'adresse de contact (ici le téléphone/email), enregistre,
    puis un médecin consulte le dossier pour vérifier que la modification est répercutée.
    """
    pid = patient_manager.add_patient("Dubois", "Jean", "01/01/2000", "100017512345678")
    
    patient_manager.update_patient(pid, phone="0611223344", email="jean.dubois@new.com")
    
    dossier_consulte = patient_manager.get_patient_info(pid)
    assert dossier_consulte["phone"] == "0611223344"
    assert dossier_consulte["email"] == "jean.dubois@new.com"
    assert any("Modification" in log for log in dossier_consulte["history"])

def test_fonctionnel_archivage_dossier_patient(patient_manager):
    """
    Scénario du plan de test: Archivage d'un dossier patient
    Un administrateur archive un dossier. 
    L'archivage doit être effectif (statut archived).
    (Invisible pour les utilisateurs standard: Non implémenté dans Patient() pour le moment, 
    on teste la mise à jour du statut).
    """
    pid = patient_manager.add_patient("Martin", "Paul", "10/10/1980", "180107512345678")
    
    patient_manager.archive_patient(pid)
    
    dossier = patient_manager.get_patient_info(pid)
    assert dossier["status"] == "archived"
    assert "Archivage" in dossier["history"][-1]

def test_fonctionnel_historique_dossier_patient(patient_manager):
    """
    Scénario du plan de test: Historique de dossiers patient
    Un responsable consulte l'historique d'un patient et voit la liste chronologique 
    exacte des interventions.
    """
    pid = patient_manager.add_patient("Blanc", "Rose", "01/01/1990", "290017512345680")
    
    patient_manager.update_patient(pid, phone="0600000001")
    patient_manager.update_patient(pid, email="rose@test.com")
    patient_manager.archive_patient(pid)
    
    dossier = patient_manager.get_patient_info(pid)
    historique = dossier["history"]
    
    assert len(historique) == 3
    assert "Modification" in historique[0]
    assert "0600000001" in historique[0]
    assert "Modification" in historique[1]
    assert "rose@test.com" in historique[1]
    assert "Archivage" in historique[2]
