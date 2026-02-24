import re
from datetime import datetime

class Patient:
    def __init__(self):
        self.patients = {}

    def add_patient(self, nom: str, prenom: str, date_naissance: str, numero_secu: str, age: int = None, email: str = None, phone: str = None, medical_history: list = None, allergies: list = None):
        if not nom or not prenom:
            raise ValueError("Le nom et le prénom sont obligatoires.")
        if any(char.isdigit() for char in nom + prenom):
            raise ValueError("Le nom et le prénom ne doivent pas contenir de chiffres.")
        
        try:
            dt_naissance = datetime.strptime(date_naissance, "%d/%m/%Y")
        except ValueError:
            raise ValueError("La date de naissance doit être au format DD/MM/YYYY.")
        if dt_naissance > datetime.now():
            raise ValueError("La date de naissance ne peut pas être dans le futur.")
        
        today = datetime.now()
        age_calcule = today.year - dt_naissance.year - ((today.month, today.day) < (dt_naissance.month, dt_naissance.day))
        if age is not None and age != age_calcule:
            raise ValueError("L'âge fourni ne correspond pas à la date de naissance.")
        age = age_calcule

        if not numero_secu or not re.match(r'^\d{15}$', str(numero_secu)):
            raise ValueError("Le numéro de sécurité sociale doit contenir exactement 15 chiffres.")
        for p in self.patients.values():
            if p.get('numero_secu') == numero_secu:
                raise ValueError("Ce numéro de sécurité sociale existe déjà.")

        patient_id = len(self.patients) + 1
        self.patients[patient_id] = {
            'nom': nom,
            'prenom': prenom,
            'date_naissance': date_naissance,
            'numero_secu': numero_secu,
            'age': age,
            'email': email,
            'phone': phone,
            'medical_history': medical_history or [],
            'allergies': allergies or [],
            'status': 'active'
        }
        return patient_id

    def get_patient_info(self, patient_id: int):
        return self.patients.get(patient_id, "Patient not found")

    def update_patient(self, patient_id: int, **kwargs):
        if patient_id not in self.patients:
            raise ValueError("Patient introuvable.")
            
        patient = self.patients[patient_id]
        
        # L'identifiant unique (numero_secu) ne doit jamais changer
        if 'numero_secu' in kwargs and kwargs['numero_secu'] != patient['numero_secu']:
             raise ValueError("L'identifiant unique (numéro de sécu) ne peut pas être modifié.")

        # Validation spécifique pour le téléphone (simple Regex par exemple)
        if 'phone' in kwargs and kwargs['phone']:
            if not re.match(r'^\+?[\d\s-]{10,}$', kwargs['phone']):
                raise ValueError("Le format du numéro de téléphone est invalide.")
                
        # Historisation de la modification
        if 'history' not in patient:
            patient['history'] = []
            
        modifs = [f"{k}: {v}" for k, v in kwargs.items()]
        log_entry = f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Modification: {', '.join(modifs)}"
        patient['history'].append(log_entry)

        patient.update(kwargs)
        return True

    def archive_patient(self, patient_id: int):
        if patient_id not in self.patients:
            raise ValueError("Patient introuvable.")
            
        patient = self.patients[patient_id]
        
        if patient.get('status') == 'archived':
            raise ValueError("Ce dossier est déjà archivé.")
            
        patient['status'] = 'archived'
        
        # Log de l'archivage
        if 'history' not in patient:
            patient['history'] = []
            
        log_entry = f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Archivage du dossier"
        patient['history'].append(log_entry)
        
        return True

    def add_medical_history(self, patient_id: int, condition: str):
        if patient_id in self.patients:
            self.patients[patient_id]['medical_history'].append(condition)
            return True
        return False

    def add_allergy(self, patient_id: int, allergy: str):
        if patient_id in self.patients:
            self.patients[patient_id]['allergies'].append(allergy)
            return True
        return False

    def list_all_patients(self):
        return self.patients

    def get_patients_by_age(self, age: int):
        return {pid: info for pid, info in self.patients.items() if info['age'] == age}

    def __str__(self):
        return f"Patient Manager with {len(self.patients)} patients"