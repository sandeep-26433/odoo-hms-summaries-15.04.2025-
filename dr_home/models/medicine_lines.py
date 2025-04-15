from odoo import models, fields, api
from odoo.exceptions import ValidationError
 
class DoctorMedicineLines(models.Model):
    _name = 'doctor.medicine.lines'
    _description = 'Medicine Lines'
 
    appointment_id = fields.Many2one('doctor.appointments', string="Appointment", ondelete='cascade', required=True)
    reference_id = fields.Char(string="Patient Reference ID", readonly=True)
    medicine_id = fields.Many2one('doctor.medicines', string="Medicine", required=True)
    dosage_id = fields.Many2one('doctor.dosages', string="Dosage")
    usage = fields.Text(string="Usage")
    days = fields.Integer(string="Days", required=True, default=1)
    course = fields.Selection([
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
    ], string="Course")
    quantity = fields.Integer(string="Quantity",compute="_compute_quantity", required=True,readonly=False ,default=1)
    prescription_date = fields.Date(string="Prescription Date", default=fields.Date.today)
 
    product_id = fields.Many2one('product.product', string='Medicine')
    price_unit = fields.Float(string='Price', compute='_compute_price', store=True)
    subtotal = fields.Float(string='Subtotal', compute='_compute_subtotal')
    on_hand_qty = fields.Float(string="On Hand Quantity",compute='_onchange_medicine_name',store=True)
    quantity_display = fields.Html(string="Available Quantity", compute="_compute_quantity_display", sanitize=False)

    name = fields.Char(string="Patient Name", compute="_compute_name", store=True)

    @api.constrains('product_id', 'course', 'appointment_id')
    def _check_unique_medicine_for_course(self):
        """Ensure that the same medicine is not added for the same course in the same appointment."""
        for record in self:
            # Check if the same medicine and course already exist for the same appointment
            existing_lines = self.env['doctor.medicine.lines'].search([
                ('appointment_id', '=', record.appointment_id.id),
                ('product_id', '=', record.product_id.id),
                ('course', '=', record.course),
                ('id', '!=', record.id)  # Exclude current record from the check
            ])
            if existing_lines:
                raise ValidationError(
                    f"The medicine '{record.product_id.name}' has already been added for course {record.course} in this appointment."
                )

    @api.depends('appointment_id')
    def _compute_name(self):
        for record in self:
            if record.appointment_id:
                record.name = record.appointment_id.name  # assuming 'patient_name' exists in doctor.appointments
                

    
    @api.onchange('quantity', 'on_hand_qty')
    def _compute_quantity_display(self):
        """Display `quantity` in **Red** (if less stock) or **Green** (if sufficient stock)."""
        for record in self:
            if record.quantity > record.on_hand_qty:
                record.quantity_display = f"<span style='color: red; font-weight: bold;'>{record.on_hand_qty}</span>"
            else:
                record.quantity_display = f"<span style='color: green; font-weight: bold;'>{record.on_hand_qty}</span>"
 
 
    @api.depends('dosage_id', 'days')
    def _compute_quantity(self):
        """Calculate total medicine quantity as `dosage.quantity * days`."""
        for record in self:
            if record.dosage_id:
                record.quantity = record.dosage_id.quantity * record.days
 
            else:
                record.quantity = 0
 
    @api.onchange('dosage_id', 'days')
    def _onchange_dosage_or_days(self):
        """Update the quantity automatically when dosage or days change."""
        if self.dosage_id:
            self.quantity = self.dosage_id.quantity * self.days
   
   
    @api.onchange('medicine_id')
    def _onchange_medicine_name(self):
        """Fetch On Hand Quantity by linking `medicine_name` to `product_template` and `product_product`."""
        for record in self:
            if record.medicine_id.medicine_name:
                # Step 1: Extract `product_id` using `product_template` name
                query = """
                    SELECT pp.id
                    FROM product_product pp
                    JOIN product_template pt ON pp.product_tmpl_id = pt.id
                    WHERE pt.name->>'en_US' = %s
                """
                self.env.cr.execute(query, (record.medicine_id.medicine_name,))
                result = self.env.cr.fetchone()
 
                if result:
                    product_id = result[0]
                    record.product_id = product_id  # Assign the matched product ID
 
                    # Step 2: Fetch On-Hand Quantity from `stock.quant`
                    stock_quant = self.env['stock.quant'].search([
                        ('product_id', '=', product_id)
                    ], limit=1)
 
                    record.on_hand_qty = stock_quant.quantity if stock_quant else 0
                    # record.low_stock_warning = record.quantity > record.on_hand_qty
                else:
                    record.product_id = False
                    record.on_hand_qty = 0
                    # record.low_stock_warning = True  # Mark as warning if no product found
 
    @api.depends('product_id')
    def _compute_price(self):
        for record in self:
            record.price_unit = record.product_id.lst_price if record.product_id else 0.0
 
    @api.depends('quantity', 'price_unit')
    def _compute_subtotal(self):
        for record in self:
            record.subtotal = record.quantity * record.price_unit
 
    @api.model
    def create(self, vals):
        """Auto-fetch product_id from POS products using product_template name"""
        if not vals.get('product_id') and vals.get('medicine_id'):
            # Fetch medicine name from doctor.medicines model
            medicine = self.env['doctor.medicines'].browse(vals['medicine_id'])
 
            if not medicine:
                raise ValidationError(f"Medicine with ID {vals['medicine_id']} does not exist in 'doctor.medicines'.")
 
            # Extract product name from JSON structure in product_template
            query = """
                SELECT pp.id
                FROM product_product pp
                JOIN product_template pt ON pp.product_tmpl_id = pt.id
                WHERE pt.name->>'en_US' = %s
            """
            self.env.cr.execute(query, (medicine.medicine_name,))
            result = self.env.cr.fetchone()
 
            if not result:
                raise ValidationError(f"Product '{medicine.medicine_name}' does not exist in POS products. Please add it to POS products.")
 
            vals['product_id'] = result[0]
 
        return super(DoctorMedicineLines, self).create(vals)
 
    def write(self, vals):
        """Ensure product_id is updated when medicine_id changes"""
        for record in self:
            if 'medicine_id' in vals:
                medicine = self.env['doctor.medicines'].browse(vals['medicine_id'])
 
                if not medicine:
                    raise ValidationError(f"Medicine with ID {vals['medicine_id']} does not exist in 'doctor.medicines'.")
 
                # Extract product name from JSON structure in product_template
                query = """
                    SELECT pp.id
                    FROM product_product pp
                    JOIN product_template pt ON pp.product_tmpl_id = pt.id
                    WHERE pt.name->>'en_US' = %s
                """
                self.env.cr.execute(query, (medicine.medicine_name,))
                result = self.env.cr.fetchone()
 
                if not result:
                    raise ValidationError(f"Product '{medicine.medicine_name}' does not exist in POS products. Please add it to POS products.")
 
                vals['product_id'] = result[0]
 
        return super(DoctorMedicineLines, self).write(vals)
    #from this updatation of mediceines
   
         
    # def push_medicines_to_pos_cart(self, pos_session_id):
    #     """Pushes prescribed medicines directly to the POS cart in the active POS session."""
    #     pos_session = self.env['pos.session'].browse(pos_session_id)
 
    #     if not pos_session or pos_session.state != 'opened':
    #         raise ValidationError("No active POS session found to push medicines.")
 
    #     # Prepare medicine data
    #     medicine_data = [
    #         {
    #             'product_id': medicine.product_id.id,
    #             'qty': medicine.quantity,
    #             'price_unit': medicine.price_unit
    #         }
    #         for medicine in self
    #     ]
 
    #     # Send data to POS UI using Bus Event
    #     self.env['bus.bus']._sendone(
    #         (self.env.cr.dbname, 'pos.sync', pos_session.id),
    #         'load_prescription_medicines',
    #         {'medicine_data': medicine_data}
    #     )
 
    # def write(self, vals):
    #     """Ensure product_id is updated when medicine_id changes"""
    #     for record in self:
    #         if 'medicine_id' in vals:
    #             medicine = self.env['doctor.medicines'].browse(vals['medicine_id'])
    #             if not medicine:
    #                 raise ValidationError(f"Medicine with ID {vals['medicine_id']} does not exist in 'doctor.medicines'.")
               
    #             vals['product_id'] = self._get_product_id_from_name(medicine.medicine_name)
 
    #     return super(DoctorMedicineLines, self).write(vals)
#----------------------------------------------------------------------------------------------------------------------
# previous_medicine_id = fields.Many2one('doctor.medicines', string="Previous Medicine", readonly=True)
 
    # # Track previous quantity for accurate stock restoration
    # previous_quantity = fields.Integer(string="Previous Quantity", readonly=True)
 
    # color_class = fields.Selection([
    #     ('green', 'Sufficient Stock'),
    #     ('red', 'Low Stock')
    # ], string='Color Class', compute='_compute_color_class', store=True)
    # @api.onchange('quantity', 'on_hand_qty')
    # def _compute_color_class(self):
    #     for record in self:
    #         if record.quantity > record.on_hand_qty:
    #             record.color_class = 'red'
    #         else:
    #             record.color_class = 'green'
 
    # low_stock_warning = fields.Boolean(string="Low Stock Warning")
 
    # pos_session_id = fields.Many2one('pos.session', string='POS Session')
    
 