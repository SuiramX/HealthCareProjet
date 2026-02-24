import pandas as pd

class Medication:
    def __init__(self, interactions_file: str = "datas/interactions.csv"):
        self.medication_history = {}
        self.interactions_df = self._load_interactions(interactions_file)

    def _load_interactions(self, interactions_file: str):
        """Load drug interactions from CSV file"""
        try:
            df = pd.read_csv(interactions_file)
            print(f"Loaded {len(df)} drug interactions")
            return df
        except FileNotFoundError:
            print(f"Warning: {interactions_file} not found")
            return pd.DataFrame()

    def prescribe_medication(self, patient_id: int, medication_name: str, dosage: str = None, frequency: str = None):
        """Prescribe a medication to a patient"""
        if patient_id not in self.medication_history:
            self.medication_history[patient_id] = []
        
        # Check for interactions
        warnings = self._check_interactions(patient_id, medication_name)
        
        medication = {
            'name': medication_name,
            'dosage': dosage,
            'frequency': frequency,
            'status': 'active'
        }
        
        self.medication_history[patient_id].append(medication)
        
        # Print warnings
        if warnings:
            print(f"WARNING: {medication_name} interacts with:")
            for warning in warnings:
                print(f"   - {warning}")
            return False
        
        return True

    def get_medication_history(self, patient_id: int):
        """Get all medications for a patient"""
        return self.medication_history.get(patient_id, [])

    def stop_medication(self, patient_id: int, medication_name: str):
        """Stop a medication for a patient"""
        if patient_id in self.medication_history:
            for med in self.medication_history[patient_id]:
                if med['name'] == medication_name:
                    med['status'] = 'stopped'
                    return True
        return False

    def get_active_medications(self, patient_id: int):
        """Get all active medications for a patient"""
        if patient_id in self.medication_history:
            return [med for med in self.medication_history[patient_id] if med['status'] == 'active']
        return []

    def _check_interactions(self, patient_id: int, new_med: str):
        """Check if new medication interacts with active medications"""
        warnings = []
        active_meds = self.get_active_medications(patient_id)
        
        for med in active_meds:
            interaction = self._find_interaction(med['name'], new_med)
            if interaction:
                warnings.append(f"{med['name']} ({interaction})")
        
        return warnings

    def _find_interaction(self, med1: str, med2: str):
        """Find interaction between two medications"""
        if self.interactions_df.empty:
            return None
        
        med1_lower = med1.lower()
        med2_lower = med2.lower()
        
        # Search in dataframe
        for _, row in self.interactions_df.iterrows():
            m1 = row['medication_1'].lower()
            m2 = row['medication_2'].lower()
            
            if (med1_lower == m1 and med2_lower == m2) or (med1_lower == m2 and med2_lower == m1):
                return row['severity']
        
        return None

    def __str__(self):
        return f"Medication Manager"