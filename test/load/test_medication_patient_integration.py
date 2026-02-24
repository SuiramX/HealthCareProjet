from patient import Patient
from medication import Medication

def test_prescription_linked_to_correct_patient():
    patient_manager = Patient()
    medication_manager = Medication()

    pid = patient_manager.add_patient("Durand", 50)

    medication_manager.prescribe_medication(
        patient_id=pid,
        medication_name="Ibuprofene"
    )

    history = medication_manager.get_medication_history(pid)

    assert len(history) == 1
    assert history[0]["name"] == "Ibuprofene"