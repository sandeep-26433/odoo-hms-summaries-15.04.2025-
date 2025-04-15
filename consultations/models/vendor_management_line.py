from odoo import api, fields, models

class VendorManagementLine(models.Model):
    _name = 'vendor.management.line'
    _description = 'Vendor Management Line'

    vendor_management_id = fields.Many2one('vendor.management', string='Vendor Reference', required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Product', required=True)
    quantity = fields.Float(string='Quantity', required=True)
    cost = fields.Float(string='Cost', required=True)
    lot_number = fields.Char(string='Lot Number')
    expiry_date = fields.Date(string='Expiry Date')

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            lot = self.env['stock.lot'].search([('product_id', '=', self.product_id.id)], limit=1)
            if lot:
                self.lot_number = lot.name
