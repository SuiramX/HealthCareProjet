"""Tests d'intégration : Lien patient-ordonnance"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src'))

from patient import Patient
from medication import Medication

def test_prescription_linked_to_correct_patient():
    """Test: ordonnance correctement liée au patient"""
    patient_manager = Patient()
    medication_manager = Medication()

    # Créer un patient avec tous les paramètres obligatoires
    pid = patient_manager.add_patient(
        nom="Durand",
        prenom="Jean",
        date_naissance="15/03/1974",  # Actuellement 50 ans (né en 1974)
        numero_secu="174031512345678"
    )

    # Ajouter une médication au patient
    medication_manager.prescribe_medication(
        patient_id=pid,
        medication_name="Ibuprofene"
    )

    # Vérifier que la médication est dans l'historique
    history = medication_manager.get_medication_history(pid)

    assert len(history) == 1
    assert history[0]["name"] == "Ibuprofene"
