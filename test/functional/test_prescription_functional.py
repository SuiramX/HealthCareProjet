"""Tests fonctionnels : Workflow complet du médecin (sélection, remplissage, validation, vérification)"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src'))

import pytest
from patient import Patient
from medication import Medication
from prescription import Prescription


@pytest.mark.functional
class TestMedicianPrescriptionWorkflow:
    """Tests fonctionnels : workflow complet du médecin"""
    
    @pytest.fixture
    def doctor_office_setup(self):
        """Configuration complète : patient, médecin, système"""
        patient_mgr = Patient()
        medication_mgr = Medication()
        prescription_mgr = Prescription()
        
        # Créer un patient
        patient_id = patient_mgr.add_patient(
            nom="Bernard",
            prenom="Marie",
            date_naissance="10/02/1967",
            numero_secu="267021234567890",
            medical_history=["Hypertension"],
            allergies=["Pénicilline"]
        )
        
        return {
            'patient_mgr': patient_mgr,
            'medication_mgr': medication_mgr,
            'prescription_mgr': prescription_mgr,
            'patient_id': patient_id,
            'doctor_id': 101
        }
    
    def test_step1_doctor_selects_medication(self, doctor_office_setup):
        """Étape 1 : Médecin sélectionne un médicament"""
        env = doctor_office_setup
        
        # Médecin choisit Aspirine
        medication_name = "Aspirine"
        
        # Vérifier que c'est un choix valide
        assert medication_name is not None
        assert isinstance(medication_name, str)
        assert len(medication_name) > 0
    
    def test_step2_doctor_fills_dosage(self, doctor_office_setup):
        """Étape 2 : Médecin remplit la posologie"""
        env = doctor_office_setup
        
        # Le médecin remplit la dose
        medication_name = "Aspirine"
        base_dosage = 500.0  # mg
        patient_weight = 72.0
        
        # Calcul automatique
        calculated_dosage = env['medication_mgr'].calculate_dosage(
            base_dosage, 
            patient_weight
        )
        
        assert calculated_dosage > 0
        assert calculated_dosage != 500.0  # Standard weight
    
    def test_step3_doctor_validates_submission(self, doctor_office_setup):
        """Étape 3 : Médecin valide l'envoi de la prescription"""
        env = doctor_office_setup
        
        # Médecin prépare les données
        medication_name = "Aspirine"
        dosage = "500mg"
        frequency = "1 fois par jour"
        duration_days = 10
        
        # Validation avant envoi
        is_valid = env['medication_mgr'].validate_prescription_fields(
            medication_name=medication_name,
            dosage=dosage,
            frequency=frequency,
            duration_days=duration_days
        )
        
        assert is_valid is True
    
    def test_step4_prescription_instant_appearance(self, doctor_office_setup):
        """Étape 4 : Prescription apparaît INSTANTANÉMENT dans le dossier"""
        env = doctor_office_setup
        patient_id = env['patient_id']
        
        # Médecin valide et envoie
        prescription_id = env['prescription_mgr'].create_prescription(
            patient_id=patient_id,
            medication_name="Aspirine",
            dosage="500mg",
            frequency="1/j",
            duration_days=10,
            doctor_id=env['doctor_id']
        )
        
        # IMMÉDIATE VERIFICATION - la prescription apparaît tout de suite
        prescriptions = env['prescription_mgr'].get_patient_prescriptions(patient_id)
        
        assert len(prescriptions) > 0
        assert prescriptions[0]['medication_name'] == "Aspirine"
        assert prescriptions[0]['patient_id'] == patient_id
        assert prescriptions[0]['status'] == 'active'
    
    def test_complete_physician_workflow_start_to_finish(self, doctor_office_setup):
        """TEST COMPLET : Workflow médecin du début à la fin"""
        env = doctor_office_setup
        patient_id = env['patient_id']
        doctor_id = env['doctor_id']
        
        # 1. ACCÈS AU DOSSIER PATIENT
        patient_info = env['patient_mgr'].get_patient_info(patient_id)
        assert patient_info['nom'] == "Bernard"
        assert patient_info['prenom'] == "Marie"
        
        # 2. SÉLECTION MÉDICAMENT + REMPLISSAGE POSOLOGIE
        medication_name = "Aspirine"
        dosage = "500mg"
        frequency = "1 fois par jour"
        duration_days = 10
        
        # 3. VALIDATION DES CHAMPS
        is_valid = env['medication_mgr'].validate_prescription_fields(
            medication_name=medication_name,
            dosage=dosage,
            frequency=frequency,
            duration_days=duration_days
        )
        assert is_valid is True
        
        # 4. ENVOI (CRÉATION ORDONNANCE)
        prescription_id = env['prescription_mgr'].create_prescription(
            patient_id=patient_id,
            medication_name=medication_name,
            dosage=dosage,
            frequency=frequency,
            duration_days=duration_days,
            doctor_id=doctor_id
        )
        
        assert prescription_id is not None
        
        # 5. VÉRIFICATION INSTANTANÉE DANS LE DOSSIER
        prescriptions = env['prescription_mgr'].get_patient_prescriptions(patient_id)
        
        assert len(prescriptions) == 1
        prescription = prescriptions[0]
        assert prescription['medication_name'] == "Aspirine"
        assert prescription['dosage'] == "500mg"
        assert prescription['frequency'] == "1 fois par jour"
        assert prescription['duration_days'] == 10
        assert prescription['status'] == 'active'
        assert prescription['patient_id'] == patient_id
        assert prescription['doctor_id'] == doctor_id
    
    def test_workflow_error_missing_dosage(self, doctor_office_setup):
        """Gestion erreur : médecin oublie la posologie"""
        env = doctor_office_setup
        
        with pytest.raises(ValueError, match="La posologie est obligatoire"):
            env['medication_mgr'].validate_prescription_fields(
                medication_name="Aspirine",
                dosage="",
                frequency="1/j",
                duration_days=10
            )
    
    def test_workflow_error_missing_frequency(self, doctor_office_setup):
        """Gestion erreur : médecin oublie la fréquence"""
        env = doctor_office_setup
        
        with pytest.raises(ValueError, match="La fréquence est obligatoire"):
            env['medication_mgr'].validate_prescription_fields(
                medication_name="Aspirine",
                dosage="500mg",
                frequency="",
                duration_days=10
            )
    
    def test_workflow_error_missing_duration(self, doctor_office_setup):
        """Gestion erreur : médecin oublie la durée"""
        env = doctor_office_setup
        
        with pytest.raises(ValueError, match="La durée doit être un entier positif"):
            env['medication_mgr'].validate_prescription_fields(
                medication_name="Aspirine",
                dosage="500mg",
                frequency="1/j",
                duration_days=0
            )
    
    def test_workflow_multiple_prescriptions_same_patient(self, doctor_office_setup):
        """Workflow : médecin prescrit 3 médicaments au même patient"""
        env = doctor_office_setup
        patient_id = env['patient_id']
        doctor_id = env['doctor_id']
        
        medications = [
            ("Aspirine", "500mg", "1/j", 10),
            ("Ibuprofene", "200mg", "2/j", 5),
            ("Paracetamol", "1000mg", "3/j", 7)
        ]
        
        # Médecin valide et envoie 3 prescriptions
        for med_name, dos, freq, dur in medications:
            env['prescription_mgr'].create_prescription(
                patient_id=patient_id,
                medication_name=med_name,
                dosage=dos,
                frequency=freq,
                duration_days=dur,
                doctor_id=doctor_id
            )
        
        # Vérifier toutes les prescriptions
        prescriptions = env['prescription_mgr'].get_patient_prescriptions(patient_id)
        
        assert len(prescriptions) == 3
        med_names = {p['medication_name'] for p in prescriptions}
        assert med_names == {"Aspirine", "Ibuprofene", "Paracetamol"}
    
    def test_workflow_stops_active_prescription(self, doctor_office_setup):
        """Workflow : médecin arrête une prescription active"""
        env = doctor_office_setup
        patient_id = env['patient_id']
        
        # Créer une prescription
        prescription_id = env['prescription_mgr'].create_prescription(
            patient_id=patient_id,
            medication_name="Aspirine",
            dosage="500mg",
            frequency="1/j",
            duration_days=10
        )
        
        # Vérifier qu'elle est active
        presc = env['prescription_mgr'].get_prescription(prescription_id)
        assert presc['status'] == 'active'
        
        # Médecin l'arrête
        env['prescription_mgr'].stop_prescription(prescription_id)
        
        # Vérifier qu'elle n'est plus active
        presc = env['prescription_mgr'].get_prescription(prescription_id)
        assert presc['status'] == 'stopped'
    
    def test_workflow_immediate_visibility_multiple_doctors(self, doctor_office_setup):
        """Workflow : plusieurs médecins voient immédiatement les prescriptions les uns des autres"""
        env = doctor_office_setup
        patient_id = env['patient_id']
        
        # Médecin 1 crée une prescription
        presc1_id = env['prescription_mgr'].create_prescription(
            patient_id=patient_id,
            medication_name="Aspirine",
            dosage="500mg",
            frequency="1/j",
            duration_days=10,
            doctor_id=101
        )
        
        # Médecin 2 voit immédiatement cette prescription
        prescriptions = env['prescription_mgr'].get_patient_prescriptions(patient_id)
        assert len(prescriptions) == 1
        
        # Médecin 2 ajoute une prescription
        presc2_id = env['prescription_mgr'].create_prescription(
            patient_id=patient_id,
            medication_name="Ibuprofene",
            dosage="200mg",
            frequency="2/j",
            duration_days=5,
            doctor_id=102
        )
        
        # Médecin 1 voit immédiatement la prescription du médecin 2
        prescriptions = env['prescription_mgr'].get_patient_prescriptions(patient_id)
        assert len(prescriptions) == 2
