"""Tests unitaires : Calculs de posologie automatique et validation des champs obligatoires"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src'))

import pytest
from medication import Medication


@pytest.mark.unit
class TestDosageCalculation:
    """Tests unitaires : calculs de posologie automatique selon le poids"""
    
    @pytest.fixture
    def medication_mgr(self):
        return Medication()
    
    def test_calculate_dosage_poids_standard(self, medication_mgr):
        """Test: calcul posologie pour patient poids standard (70kg)"""
        base_dosage = 10.0
        patient_weight = 70.0
        
        result = medication_mgr.calculate_dosage(base_dosage, patient_weight)
        assert result == 10.0
    
    def test_calculate_dosage_patient_lourd(self, medication_mgr):
        """Test: calcul posologie pour patient plus lourd que standard"""
        base_dosage = 10.0
        patient_weight = 85.0
        
        result = medication_mgr.calculate_dosage(base_dosage, patient_weight)
        expected = round((10.0 * 85.0) / 70.0, 2)
        assert result == expected
    
    def test_calculate_dosage_patient_leger(self, medication_mgr):
        """Test: calcul posologie pour patient plus léger que standard"""
        base_dosage = 10.0
        patient_weight = 50.0
        
        result = medication_mgr.calculate_dosage(base_dosage, patient_weight)
        expected = round((10.0 * 50.0) / 70.0, 2)
        assert result == expected
    
    def test_calculate_dosage_poids_standard_personnalise(self, medication_mgr):
        """Test: calcul avec poids standard personnalisé"""
        base_dosage = 100.0
        patient_weight = 60.0
        standard_weight = 75.0
        
        result = medication_mgr.calculate_dosage(base_dosage, patient_weight, standard_weight)
        expected = round((100.0 * 60.0) / 75.0, 2)
        assert result == expected
    
    def test_calculate_dosage_posologie_invalide(self, medication_mgr):
        """Test: erreur avec posologie de base négative"""
        with pytest.raises(ValueError, match="Posologie de base doit être un nombre positif"):
            medication_mgr.calculate_dosage(-5.0, 70.0)
    
    def test_calculate_dosage_posologie_zero(self, medication_mgr):
        """Test: erreur avec posologie de base zéro"""
        with pytest.raises(ValueError, match="Posologie de base doit être un nombre positif"):
            medication_mgr.calculate_dosage(0, 70.0)
    
    def test_calculate_dosage_poids_patient_invalide(self, medication_mgr):
        """Test: erreur avec poids patient négatif"""
        with pytest.raises(ValueError, match="Poids du patient doit être un nombre positif"):
            medication_mgr.calculate_dosage(10.0, -50.0)
    
    def test_calculate_dosage_poids_patient_zero(self, medication_mgr):
        """Test: erreur avec poids patient zéro"""
        with pytest.raises(ValueError, match="Poids du patient doit être un nombre positif"):
            medication_mgr.calculate_dosage(10.0, 0)
    
    def test_calculate_dosage_poids_standard_invalide(self, medication_mgr):
        """Test: erreur avec poids standard négatif"""
        with pytest.raises(ValueError, match="Poids standard doit être un nombre positif"):
            medication_mgr.calculate_dosage(10.0, 70.0, -70.0)


@pytest.mark.unit
class TestValidationChampsObligatoires:
    """Tests unitaires : validation des champs obligatoires (durée, fréquence, dosage)"""
    
    @pytest.fixture
    def medication_mgr(self):
        return Medication()
    
    def test_validate_tous_champs_valides(self, medication_mgr):
        """Test: validation avec tous les champs valides"""
        result = medication_mgr.validate_prescription_fields(
            medication_name="Aspirine",
            dosage="500mg",
            frequency="1 fois par jour",
            duration_days=7
        )
        assert result is True
    
    def test_validate_nom_medicament_manquant(self, medication_mgr):
        """Test: erreur quand le nom du médicament est vide"""
        with pytest.raises(ValueError, match="Le nom du médicament est obligatoire"):
            medication_mgr.validate_prescription_fields("", "500mg", "1/j", 7)
    
    def test_validate_nom_medicament_none(self, medication_mgr):
        """Test: erreur quand le nom du médicament est None"""
        with pytest.raises(ValueError, match="Le nom du médicament est obligatoire"):
            medication_mgr.validate_prescription_fields(None, "500mg", "1/j", 7)
    
    def test_validate_dosage_manquant(self, medication_mgr):
        """Test: erreur quand la posologie est vide"""
        with pytest.raises(ValueError, match="La posologie est obligatoire"):
            medication_mgr.validate_prescription_fields("Aspirine", "", "1/j", 7)
    
    def test_validate_dosage_none(self, medication_mgr):
        """Test: erreur quand la posologie est None"""
        with pytest.raises(ValueError, match="La posologie est obligatoire"):
            medication_mgr.validate_prescription_fields("Aspirine", None, "1/j", 7)
    
    def test_validate_frequence_manquante(self, medication_mgr):
        """Test: erreur quand la fréquence est vide"""
        with pytest.raises(ValueError, match="La fréquence est obligatoire"):
            medication_mgr.validate_prescription_fields("Aspirine", "500mg", "", 7)
    
    def test_validate_frequence_none(self, medication_mgr):
        """Test: erreur quand la fréquence est None"""
        with pytest.raises(ValueError, match="La fréquence est obligatoire"):
            medication_mgr.validate_prescription_fields("Aspirine", "500mg", None, 7)
    
    def test_validate_duree_zero(self, medication_mgr):
        """Test: erreur quand la durée est 0"""
        with pytest.raises(ValueError, match="La durée doit être un entier positif"):
            medication_mgr.validate_prescription_fields("Aspirine", "500mg", "1/j", 0)
    
    def test_validate_duree_negative(self, medication_mgr):
        """Test: erreur quand la durée est négative"""
        with pytest.raises(ValueError, match="La durée doit être un entier positif"):
            medication_mgr.validate_prescription_fields("Aspirine", "500mg", "1/j", -5)
    
    def test_validate_duree_none(self, medication_mgr):
        """Test: erreur quand la durée est None"""
        with pytest.raises(ValueError, match="La durée doit être un entier positif"):
            medication_mgr.validate_prescription_fields("Aspirine", "500mg", "1/j", None)
    
    def test_validate_duree_float(self, medication_mgr):
        """Test: erreur quand la durée est un float au lieu d'un entier"""
        with pytest.raises(ValueError, match="La durée doit être un entier positif"):
            medication_mgr.validate_prescription_fields("Aspirine", "500mg", "1/j", 7.5)
    