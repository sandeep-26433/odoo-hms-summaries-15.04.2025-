from odoo import models, fields

class ReportMedicineLines(models.TransientModel):
    _name = "report.medicine.lines"
    _description = "Report Medicine Lines"

    report_id = fields.Many2one('report.appointment.report', string="Report", ondelete='set null')
    medicine_name = fields.Char("Medicine Name")
    dosage = fields.Char("Dosage")
    days = fields.Integer("Days")
    quantity = fields.Integer("Quantity")
    usage = fields.Text(string="Usage")
    course = fields.Selection([
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
    ], string="Course")
  

