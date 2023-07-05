{
    "name": "hr_hospital",
    "version": "16.0.1.0.0",
    "category": "Automation",
    "summary": "Keeping records of doctors and patients",
    "license": "LGPL-3",
    "author": "Odoo Community Association (OCA), Oleg Usenko",
    "website": "https://github.com/Glasis9/my_custom_addon_for_odoo_16",
    "data": [
        "security/ir.model.access.csv",
        "views/hospital_menus.xml",
        "views/hospital_doctor_views.xml",
        "views/hospital_patient_views.xml",
        "views/hospital_diagnosis_views.xml",
        "views/hospital_disease_category_views.xml",
        "views/hospital_disease_views.xml",
        "views/hospital_contact_person_views.xml",
        "views/hospital_patient_visit_views.xml",
        "views/hospital_history_of_changing_personal_doctor_views.xml",
        "views/hospital_allocation_doctor_views.xml",
        "views/hospital_analysis_views.xml",
        "views/hospital_types_analysis_views.xml",
        "wizard/hospital_add_making_appointment_wizard_views.xml",
        "wizard/hospital_change_doctor_wizard_views.xml",
        "wizard/hospital_disease_report_wizard_views.xml",
    ],
    "depends": ["base"],
    "demo": [
        "demo/hospital_disease_category_demo.xml",
        "demo/hospital_disease_demo.xml",
        "demo/hospital_doctor_demo.xml",
        "demo/hospital_contact_person_demo.xml",
        "demo/hospital_patient_demo.xml",
        "demo/hospital_diagnosis_demo.xml",
        "demo/hospital_patient_visit_demo.xml",
        "demo/hospital_allocation_doctor_demo.xml",
        "demo/hospital_types_analysis_demo.xml",
        "demo/hospital_analysis_demo.xml",
    ],
    "application": True,
    "installable": True,
    "auto_install": False,
}
