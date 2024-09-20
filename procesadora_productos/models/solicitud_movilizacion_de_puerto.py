import datetime
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SolicitudMovilizacionPuerto(models.Model):
    _name = 'movilizacion.puertosolicitud'
    _description = 'Informacion de la solicitud de un puerto para movilizar las mercancias'

    fecharealizacion = fields.Datetime(string='Fecha Realizacion', default=lambda d: fields.Datetime.now(), required=True)
    zona_mercancia_id = fields.Many2one('zona.mercancia', string='Zona de Entrega')
    mercancia_movilizacion_ids = fields.One2many('movilizacion.puertomercancia', 'solicitud_movilizacion_id', string='Mercancias')
    
    zona_almacen_entrega_id = fields.Many2one('zona.almacen', string='Zona de Entrega')

    informacion = fields.Text(string='Informacion')

    sequence_number = fields.Char(string='ID Solicitud', index=True, readonly=True)

    @api.model
    def create(self, vals):
        if 'sequence_number' not in vals:
            vals['sequence_number'] = self.env['ir.sequence'].next_by_code('movilizacion.puertosolicitud')
        return super(SolicitudMovilizacionPuerto, self).create(vals)