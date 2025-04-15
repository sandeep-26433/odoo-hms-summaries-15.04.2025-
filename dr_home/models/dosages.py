from odoo import models, fields, api
import re

class DoctorDosages(models.Model):
    _name = 'doctor.dosages'
    _description = 'Dosages'
    _rec_name = 'dosage'  # Ensures that "Dosage" is displayed in dropdowns

    dosage = fields.Char(string="Dosage", required=True, index=True)
    description = fields.Text(string="Description")
    quantity = fields.Integer(string="Total Quantity", compute="_compute_quantity", store=True) #Split for Calculation
 
 
    @api.depends('dosage')
    def _compute_quantity(self):
        """Calculate total medicine count from valid dosage format like '1-0-1'."""
        for record in self:
            if record.dosage:
                # Extract only the part before '(' or text
                clean_dosage = re.split(r'\s*\(|[a-zA-Z]', record.dosage.strip())[0]
 
                # Check if it follows '1-0-1' pattern
                if re.match(r'^(\d+-\d+-\d+(-\d+)?)$', clean_dosage):
                    record.quantity = sum(int(x) for x in clean_dosage.split('-'))
                else:
                    record.quantity = 0  # Invalid format or text-based description
 

    @api.onchange('dosage')
    def _onchange_dosage(self):
        if self.dosage:
            self.description = self.dosage
