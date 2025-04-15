from odoo import api, fields, models, _


class VendorManagement(models.Model):
    _name = 'vendor.management'
    _description = 'Vendor Management'

    invoice_number = fields.Char(string="Invoice Number")
    vendor_id = fields.Many2one('res.partner', string='Vendor', required=True)
    line_ids = fields.One2many('vendor.management.line', 'vendor_management_id', string='Product Lines')

    @api.model
    def create(self, vals):
        record = super(VendorManagement, self).create(vals)
        record._process_lines()
        return record

    def _process_lines(self):
        order_lines = []  # ⬅️ Prepare all order lines here

        for line in self.line_ids:
            product = line.product_id

            # Update cost
            product.write({'standard_price': line.cost})

            # Create or get lot (allowing duplicate lot numbers)
            lot_id = self._create_lot(line, product)

            # Update stock quant
            current_quant = self.env['stock.quant'].search([
                ('product_id', '=', product.id),
                ('location_id', '=', self.env.ref('stock.stock_location_stock').id),
                ('lot_id.name', '=', line.lot_number),
            ], limit=1)

            if current_quant:
                current_quant.quantity += line.quantity
            else:
                self.env['stock.quant'].create({
                    'product_id': product.id,
                    'quantity': line.quantity,
                    'location_id': self.env.ref('stock.stock_location_stock').id,
                    'lot_id': lot_id,
                })

            # ⬇️ Build order line (DON’T create PO here)
            order_lines.append((0, 0, {
                'product_id': product.id,
                'product_qty': line.quantity,
                'price_unit': line.cost,
            }))

        # ✅ First, create the PO and store the result
        purchase_order = self.env['purchase.order'].create({
            'partner_id': self.vendor_id.id,
            'order_line': order_lines,
            'currency_id': self.env.ref('base.INR').id,
            'date_order': fields.Datetime.now(),
            'origin': self.invoice_number or '',  # Optional for traceability
        })

        # ✅ Now confirm it
        purchase_order.button_confirm()

        # ✅ Now you can safely access picking_ids
        for picking in purchase_order.picking_ids:
            if self.invoice_number:
                picking.name = self.invoice_number

    def _create_lot(self, line, product):
        if line.lot_number:
            # Always create a new lot, even if the same lot number exists
            existing_lot = self.env['stock.lot'].search([
                ('product_id', '=', product.id),
                ('name', '=', line.lot_number)
            ], limit=1)

            if existing_lot:
                # If the lot exists, reuse it without creating a new one
                return existing_lot.id
            else:
                # If the lot doesn't exist, create a new one
                lot = self.env['stock.lot'].create({
                    'product_id': product.id,
                    'name': line.lot_number,  # Reuse the lot number without validation
                    'expiration_date': line.expiry_date,
                })
                return lot.id
        return False
