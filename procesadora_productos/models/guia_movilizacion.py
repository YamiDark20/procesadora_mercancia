import datetime
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class GuiaMovilizacion(models.Model):
    _name = 'empresa.guia_movilizacion'
    _description = 'Informacion de vehiculo usado para llevar mercancia'

    vehiculo_id = fields.Char(string='Placa Vehiculo', required=True, size=8)
    vehiculo = fields.Char(string='Vehiculo Usado', required=True)
    direccion_envio = fields.Char(string='Dir. Envio')
    direccion_entrega = fields.Char(string='Dir. Entrega')
    sequence_number = fields.Char(string='Secuencia', index=True, readonly=True)

    @api.model
    def create(self, vals):
        if 'sequence_number' not in vals:
            vals['sequence_number'] = self.env['ir.sequence'].next_by_code('empresa.guia_movilizacion')
        return super(GuiaMovilizacion, self).create(vals)
    
    def name_get(self):
        result = []
        for record in self:
            name = f"{record.sequence_number} - {record.vehiculo_id}"
            result.append((record.id, name))
        return result