import datetime
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Pago(models.Model):
    _name = 'factura.pago'
    _description = 'Informacion de la factura realizada a un cliente'

    fecharealizacion = fields.Datetime(string='Fecha Realizacion', default=lambda d: fields.Datetime.now(), required=True)
    cliente_id = fields.Many2one('res.partner', string='Id. Cliente')

    # zona_mercancia_id = fields.Many2one('zona.mercancia', string='Zona de Entrega')
    mercancia_factura_ids = fields.One2many('factura.mercancia', 'factura_pago_id', string='Mercancias')

    totalpagado = fields.Float(string='Total',required=True)
    isfinal = fields.Boolean(string="Pagado?", default=True)

    metodopago = fields.Char(string='Metodo', required=True)

    num_cuenta = fields.Char(string='Num. Cuenta', required=True, size=9)
    banco = fields.Char(string='Banco', required=True, size=9)

    informacion = fields.Text(string='Informacion')

    sequence_number = fields.Char(string='ID Factura', index=True, readonly=True)

    @api.model
    def create(self, vals):
        if 'sequence_number' not in vals:
            vals['sequence_number'] = self.env['ir.sequence'].next_by_code('factura.pago')
        return super(Pago, self).create(vals)
    
    def name_get(self):
        result = []
        for record in self:
            name = f"{record.sequence_number}"
            result.append((record.id, name))
        return result