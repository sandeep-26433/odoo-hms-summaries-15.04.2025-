from odoo import models, fields

class ReportOpSummary(models.TransientModel):
    _name = "report.op.summary"
    _description = "OP Summary"

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

    associated_complaint = fields.Text(string="Associated Complaint")
    past_history = fields.Text(string="Past History")
    family_history = fields.Text(string="Family History")
    present_history = fields.Text(string="Present History")
    diagnosis = fields.Text(string="Diagnosis")
    investigations = fields.Text(string="Investigations")
    others = fields.Text(string="Others")
    panchakarma_advice = fields.Text(string="Panchakarma Advice")

    # Health Parameters
    artava = fields.Text(string="ARTAVA")
    nadi = fields.Text(string="NADI")
    agni = fields.Text(string="AGNI")
    mala = fields.Text(string="MALA")
    mutra = fields.Text(string="MUTRA")
    nidra = fields.Text(string="NIDRA")
    manas = fields.Text(string="MANAS")
    print_summary_type = fields.Selection([
    ('current', 'Print Current Date Summary'),
    ('all', 'Print Entire Summary'),
], string="Summary Type", default='current')


   