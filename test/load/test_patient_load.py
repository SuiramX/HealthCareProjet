import pytest
import time
from src.patient import Patient

@pytest.fixture
def patient_manager():
    return Patient()

def test_load_grand_afflux_patients(patient_manager):
    """
    Test de charge: Grand afflux de nouveaux patients.
    Objectif: Vérifier que l'ajout massif de dossiers patient reste performant.
    Mesure le temps pour insérer 10 000 patients.
    """
    nb_patients = 10000
    
    start_time = time.time()
    for i in range(nb_patients):
        num_secu = f"{100000000000000 + i}"
        patient_manager.add_patient(
            nom="NomTest",
            prenom="PrenomTest",
            date_naissance="01/01/1990",
            numero_secu=num_secu
        )
    end_time = time.time()
    
    execution_time = end_time - start_time
    
    assert len(patient_manager.list_all_patients()) == nb_patients
    
    assert execution_time < 2.0, f"Le système a mis trop de temps : {execution_time} s pour {nb_patients} patients."

def test_stress_recherche_et_listing(patient_manager):
    """
    Test de stress: Augmentation du nombre de requêtes / de données.
    Objectif: S'assurer que la recherche (par âge par exemple) et le listing global
    restent performants même avec une énorme base existante.
    """
    nb_patients = 10000
    
    for i in range(nb_patients):
        annee_naissance = 1950 + (i % 50)
        num_secu = f"{200000000000000 + i}"
        patient_manager.add_patient(
            nom="TestNom",
            prenom="TestPrenom",
            date_naissance=f"10/10/{annee_naissance}",
            numero_secu=num_secu
        )
        
    start_time = time.time()
    all_p = patient_manager.list_all_patients()
    listing_time = time.time() - start_time
    assert len(all_p) == nb_patients
    assert listing_time < 0.5, f"Le listing complet prend trop de temps: {listing_time}s"
    
    start_time = time.time()
    age_cible = patient_manager.get_patient_info(1)['age']
    patients_filtres = patient_manager.get_patients_by_age(age_cible)
    filtering_time = time.time() - start_time
    
    assert len(patients_filtres) > 0
    assert filtering_time < 0.5, f"Le filtrage prend trop de temps: {filtering_time}s"

def test_load_modifications_simultanees(patient_manager):
    """
    Test de charge: Augmentation du nombre de requêtes de mise à jour.
    On simule de très nombreuses modifications d'affilée pour vérifier
    la performance d'écriture et de gestion d'historique.
    """
    pid = patient_manager.add_patient("PatientUnique", "Jean", "01/01/2000", "300000000000000")
    nb_modifs = 5000
    
    start_time = time.time()
    for i in range(nb_modifs):
        patient_manager.update_patient(pid, phone=f"060000{str(i).zfill(4)}")
    end_time = time.time()
    
    execution_time = end_time - start_time
    dossier = patient_manager.get_patient_info(pid)
    
    assert len(dossier["history"]) == nb_modifs
    assert execution_time < 1.0, f"La modification en boucle prend trop de temps: {execution_time}s"
