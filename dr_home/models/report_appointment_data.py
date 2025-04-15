from odoo import models, fields

class ReportAppointmentData(models.TransientModel):
    _name = "report.appointment.report"
    _description = "Appointment Report Data"

    op_number = fields.Char("OP Number")
    appointment_date = fields.Date("Appointment Date")
    patient_name = fields.Char("Patient Name")
    patient_id = fields.Char("Patient Reference ID")
    patient_age = fields.Integer("Patient Age")
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('others', 'Others')
    ])
    phone = fields.Char("Phone")
    email = fields.Char("Email")
    chief_complaint = fields.Text("Chief Complaint")
    htn = fields.Char("HTN")
    dm = fields.Char("DM")
    th = fields.Char("TH")
    consultation_doctor=fields.Char("Doctor Name")
    
    medicine_line_ids = fields.One2many(
    'report.medicine.lines',
    'report_id',
    string='Medicines',
    ondelete='cascade'
)

    diet = fields.Selection([
    ('g', 'Diet-G: Avoid Tuberous vegetables (can consume carrot and beetroot), Besan based foods, Curd (Consume Buttermilk), Non-Veg, Masala foods, Fast foods, Deep Fried Foods.'),
    ('sk', 'Diet-SK: Avoid Brinjal, Tamarind, Fast foods, Masala foods, Deep fried foods, Curd (can consume buttermilk), Non-Veg, Besan based food.'),
    ('n', 'Diet-N: Avoid cold, refrigerated foods, Tomato, Cucumber, chocolates, ice-creams, exposure to cold winds directly, Banana, Custard apple, Consume Luke warm water.'),
    ], string="Diet")
    special_note=fields.Char(string="Special Note")
    course = fields.Selection([
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
    ], string="Course")
    usage = fields.Text(string="Usage")
   

