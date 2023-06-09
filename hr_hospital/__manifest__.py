{
    "name": "hr_hospital",
    "version": "16.0.1.0.0",
    "category": "Automation",
    "summary": "Keeping records of doctors and patients",
    "license": "LGPL-3",
    "author": "Oleg Usenko",
    "website": "https://github.com/Glasis9/my_custom_addon_for_odoo_16",
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "views/hospital_menu.xml",
        "views/hospital_doctor_views.xml",
        "views/hospital_patient_views.xml",
        "views/hospital_diagnosis_views.xml",
        "views/hospital_visits_patient_views.xml",
        "data/hospital_diagnosis_data.xml",
    ],
    "demo": [
        "data/hospital_doctor_demo.xml",
        "data/hospital_patient_demo.xml",
        "data/hospital_visits_patient_demo.xml",
    ],
}
