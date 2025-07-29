from odoo import models, fields, api, _
from odoo.exceptions import UserError




class AccountMove(models.Model):
    _inherit = 'account.move'

    

    use_timbre_fiscal = fields.Boolean(string="Use Timbre Fiscal", default=True)




    def _get_timbre_fiscal_tax(self):
        #tax = self.env['account.tax'].search([('', '=', '')], limit=1)
        tax = self.env.ref('timbre_fiscal.tax_timbre_fiscal')
        if not tax:
            raise UserError("Timbre Fiscal tax not found.")
        elif not tax.active:
            raise UserError("Timbre Fiscal is not active.\n Disable 'Use Timbre Fiscal' in 'Other Info' page, or set the 'Timbre Fiscal' to active in the configuration.")
        return tax
    
    @api.model_create_multi
    def create(self, vals_list):
        moves = super().create(vals_list)
        for rec in moves:
            if rec.use_timbre_fiscal and rec.move_type == 'out_invoice':
                timbre_fiscal = rec._get_timbre_fiscal_tax()
                    
                existing = rec.invoice_line_ids.filtered(
                    lambda l: l.name == timbre_fiscal.name and l.quantity == 1 and l.price_unit == timbre_fiscal.amount
                )
                if timbre_fiscal and not existing:

                    max_sequence = max(rec.invoice_line_ids.mapped('sequence') or [0])
                    rec.write({
                        'invoice_line_ids': [(0, 0, {
                            'display_type': 'line_section',
                            'name': "Tax On Invoice",
                            'sequence': max_sequence + 1,
                        })]
                    })

                    max_sequence = max(rec.invoice_line_ids.mapped('sequence') or [0])
                    rec.write({
                        'invoice_line_ids': [(0, 0, {
                            'name': timbre_fiscal.name,
                            'quantity': 1,
                            'price_unit': timbre_fiscal.amount,
                            'sequence': max_sequence + 1,
                        })]
                    })
        return moves
    
    def action_post(self):
        for rec in self:
            if rec.move_type == 'out_invoice' and rec.use_timbre_fiscal:
                timbre_fiscal = self._get_timbre_fiscal_tax()

                existing = rec.invoice_line_ids.filtered(
                    lambda l: l.name == timbre_fiscal.name and l.quantity == 1 and l.price_unit == timbre_fiscal.amount
                )
                if not existing:

                    max_sequence = max(rec.invoice_line_ids.mapped('sequence') or [0])
                        
                    rec.write({
                    'invoice_line_ids': [(0, 0, {
                        'name': timbre_fiscal.name,
                        'quantity': 1,
                        'price_unit': timbre_fiscal.amount,
                        'sequence': max_sequence + 1,
                        })]
                    })

        return super().action_post()
    
    #@api.onchange('use_timbre_fiscal')
    #def add_timbre_fiscal_line(self):
        for rec in self:
            if rec.use_timbre_fiscal and rec.move_type == 'out_invoice':
                timbre_fiscal = self._get_timbre_fiscal_tax()
                # Check if Timbre line already exists
                existing = rec.invoice_line_ids.filtered(
                    lambda l: l.name == timbre_fiscal.name
                )
                if not existing:
                    
                    rec.invoice_line_ids.create({
                        'move_id': rec.id,
                        'name': timbre_fiscal.name,
                        'quantity': 1,
                        'price_unit': timbre_fiscal.amount,
                    })
    
    #@api.model
    #def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        timbre_fiscal = self._get_timbre_fiscal_tax()
        if timbre_fiscal:
            defaults['invoice_line_ids'] = [
                (0, 0, {
                    'move_id': self.id,
                    'name': timbre_fiscal.name,
                    'quantity': 1,
                    'price_unit': timbre_fiscal.amount,
                })
            ]
        return defaults
