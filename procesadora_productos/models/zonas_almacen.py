import datetime
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ZonaAlmacen(models.Model):
    _name = 'zona.almacen'
    _description = 'Informacion de la zona del almacen'

    ubicacion = fields.Char(string='Ubicacion')
    espacio = fields.Selection([
        ('hayespacio', 'Hay espacio'),
        ('nohayespacio', 'No hay espacio'),
    ], string='Espacio', copy=False, tracking=True, default='hayespacio', required=True)
    estado = fields.Selection([
        ('disponible', 'Disponible'),
        ('entransito', 'En Tránsito'),
        ('reservado', 'Reservado'),
        ('danado', 'Dañado'),
    ], string='Estado', copy=False, tracking=True, default='disponible', required=True)
    almacen_id = fields.Many2one('empresa.almacen', string='ID Almacen', required=True)

    sector = fields.Selection([
        ('recepcion', 'Recepción'),
        ('almacenamiento', 'Almacenamiento'),
        ('picking', 'Picking'),
        ('expedicion', 'Expedición'),
    ], string='Sector', copy=False, tracking=True, default='almacenamiento', required=True)

    # sequence_number = fields.Char(string='Secuencia', required=True, index=True, default=lambda self: self.env['ir.sequence'].next_by_code('empresa.almacen'), readonly=True)

    sequence_number = fields.Char(string='ID. Zona', index=True, readonly=True)

    zona_mercancia_ids = fields.One2many('zona.mercancia', 'zona_almacen_id', string='Id Zona Almacen')

    @api.model
    def create(self, vals):
        if 'sequence_number' not in vals:
            vals['sequence_number'] = self.env['ir.sequence'].next_by_code('zona.almacen')
        return super(ZonaAlmacen, self).create(vals)