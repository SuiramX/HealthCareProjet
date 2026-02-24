class Patient:
    def __init__(self):
        self.patients = {}

    def add_patient(self, name: str, age: int, email: str = None, phone: str = None, medical_history: list = None, allergies: list = None):
        patient_id = len(self.patients) + 1
        self.patients[patient_id] = {
            'name': name,
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
        if patient_id in self.patients:
            self.patients[patient_id].update(kwargs)
            return True
        return False

    def delete_patient(self, patient_id: int):
        if patient_id in self.patients:
            del self.patients[patient_id]
            return True
        return False

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