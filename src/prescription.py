from datetime import datetime, timedelta

class Prescription:
    """Représente une ordonnance médicale"""
    
    def __init__(self):
        self.prescriptions = {}
        self.prescription_counter = 0
    
    def create_prescription(self, patient_id: int, medication_name: str, dosage: str, 
                           frequency: str, duration_days: int, doctor_id: int = None):
        """Créer une ordonnance avec validation des champs obligatoires"""
        # Validation des champs obligatoires
        if not patient_id or not isinstance(patient_id, int):
            raise ValueError("L'ID patient est obligatoire et doit être un entier.")
        if not medication_name or not isinstance(medication_name, str):
            raise ValueError("Le nom du médicament est obligatoire.")
        if not dosage or not isinstance(dosage, str):
            raise ValueError("La posologie est obligatoire.")
        if not frequency or not isinstance(frequency, str):
            raise ValueError("La fréquence est obligatoire.")
        if not duration_days or not isinstance(duration_days, int) or duration_days <= 0:
            raise ValueError("La durée (en jours) est obligatoire et doit être un entier positif.")
        
        self.prescription_counter += 1
        prescription_id = self.prescription_counter
        
        prescription = {
            'id': prescription_id,
            'patient_id': patient_id,
            'medication_name': medication_name,
            'dosage': dosage,
            'frequency': frequency,
            'duration_days': duration_days,
            'doctor_id': doctor_id,
            'created_at': datetime.now(),
            'end_date': datetime.now() + timedelta(days=duration_days),
            'status': 'active'
        }
        
        self.prescriptions[prescription_id] = prescription
        return prescription_id
    
    def get_prescription(self, prescription_id: int):
        """Récupérer une ordonnance par son ID"""
        return self.prescriptions.get(prescription_id, None)
    
    def get_patient_prescriptions(self, patient_id: int):
        """Récupérer toutes les ordonnances d'un patient"""
        return [p for p in self.prescriptions.values() if p['patient_id'] == patient_id]
    
    def stop_prescription(self, prescription_id: int):
        """Arrêter une ordonnance"""
        if prescription_id not in self.prescriptions:
            return False
        self.prescriptions[prescription_id]['status'] = 'stopped'
        return True
    
    def __str__(self):
        return f"Prescription Manager ({len(self.prescriptions)} prescriptions)"
