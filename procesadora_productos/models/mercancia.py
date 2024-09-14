import datetime
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Mercancia(models.Model):
    _name = 'empresa.mercancia'
    _description = 'Informacion de una mercancia'

    nombre = fields.Char(string='Nombre', required=True)
    descripcion = fields.Text(string='Descripcion')
    marca = fields.Char(string='Marca')
    tipo = fields.Selection([
        ('perecedera', 'Perecedera'),
        ('no_perecedera', 'No Perecedera'),
        ('peligrosa', 'Peligrosa'),
        ('fragil', 'Fragil'),
    ], string='Tipo de Mercancia', copy=False, tracking=True, default='perecedera', required=True)

    sequence_number = fields.Char(string='Secuencia', index=True, readonly=True)

    @api.model
    def create(self, vals):
        if 'sequence_number' not in vals:
            vals['sequence_number'] = self.env['ir.sequence'].next_by_code('empresa.mercancia')
        return super(Mercancia, self).create(vals)
    
    def name_get(self):
        result = []
        for record in self:
            name = f"{record.sequence_number} - {record.nombre}"
            result.append((record.id, name))
        return result