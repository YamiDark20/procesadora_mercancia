import datetime
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Almacen(models.Model):
    _name = 'empresa.almacen'
    _description = 'Informacion del almacen de la empresa'

    sucursal = fields.Char(string='Sucursal', required=True)

    zona_almacen_ids = fields.One2many('zona.almacen', 'almacen_id', string='Id Zona')

    sequence_number = fields.Char(string='ID Almacen', index=True, readonly=True)

    @api.model
    def create(self, vals):
        if 'sequence_number' not in vals:
            vals['sequence_number'] = self.env['ir.sequence'].next_by_code('empresa.almacen')
        return super(Almacen, self).create(vals)
    
    # def name_get(self):
    #     result = []
    #     for record in self:
    #         name = f"{record.sequence_number} - {record.vehiculo_id}"
    #         result.append((record.id, name))
    #     return result