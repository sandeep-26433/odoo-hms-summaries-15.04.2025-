{
    'name': 'Doctor Home',
    'version': '1.0',
    'summary': 'Manage Doctor Appointments, Medicines, Dosages, and Medicine Lines',
    'description': """
        This module provides functionality to manage doctor appointments, medicines, dosages, and medicine lines.
        It includes list and form views for appointments and a separate view to manage medicine lines.
    """,
    'category': 'Hospital Management',
    'depends': ['base','point_of_sale', 'product','stock','web','account'],
    'data': [
        'security/ir.model.access.csv',
        'report/op_summary_report_template.xml',
        'report/op_summary_report.xml',
        'report/overall_summary_report_template.xml',
        'report/overall_summary_report.xml',
        'report/custom_layout_view.xml',
        'report/appointment_report_template.xml',
        'report/appointment_report.xml',
        'views/doctor_appointments_view.xml',
        'views/doctor_medicines_view.xml',
        'views/doctor_dosages_view.xml',
        'views/doctor_medicine_lines_view.xml',
        'views/op_history_views.xml',  # Add this line

        
    ],
    'installable': True,
    'application': True,
    'license': 'OPL-1',
}
