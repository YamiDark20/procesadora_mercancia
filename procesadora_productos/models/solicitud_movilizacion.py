import datetime
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SolicitudMovilizacion(models.Model):
    _name = 'movilizacion.solicitud'
    _description = 'Informacion de la solicitud de las mercancias a movilizar'

    fecharealizacion = fields.Datetime(string='Fecha Realizacion', default=lambda d: fields.Datetime.now(), required=True)
    zona_mercancia_id = fields.Many2one('zona.mercancia', string='Zona de Entrega')
    mercancia_movilizacion_ids = fields.One2many('movilizacion.mercancia', 'solicitud_movilizacion_id', string='Mercancias')

    informacion = fields.Text(string='Informacion')

    sequence_number = fields.Char(string='ID Solicitud', index=True, readonly=True)

    @api.model
    def create(self, vals):
        if 'sequence_number' not in vals:
            vals['sequence_number'] = self.env['ir.sequence'].next_by_code('movilizacion.solicitud')
        return super(SolicitudMovilizacion, self).create(vals)
    
    # def write(self, vals):
    #     res = super(SolicitudMovilizacion, self).write(vals)
    #     if 'mercancia_movilizacion_ids' in vals:
    #         for mercancia in vals['mercancia_movilizacion_ids']:
    #             if mercancia[0] == 0:  # Nuevo registro
    #                 if mercancia[2]['direccion_mercancia'] == "puerto":
    #                     mercancia_traslado = self.env['traslado.mercancia'].browse(mercancia[2]['mercancia_traslado_id'])
    #                     # id_mercancia = mercancia_traslado.mercancia_id.id

    #                     self.env['zona.mercancia'].create({
    #                         'mercancia_id': mercancia_traslado.mercancia_id.id,
    #                         'cantidad': mercancia[2]['cantidad'],
    #                         'zona_almacen_id': mercancia[2]['zona_almacen_entrega_id'],
    #                         'precio': mercancia[2]['precio'],
    #                     })
    #             elif mercancia[0] > 0:  # Actualizar registro existente
    #                 if mercancia[2]['direccion_mercancia'] == "puerto":
    #                     mercancia_traslado = self.env['traslado.mercancia'].browse(mercancia[2]['mercancia_traslado_id'])
    #                     mercancia_record = self.env['movilizacion.mercancia'].browse(mercancia[0])
    #                     mercancia[2]['zona_almacen_entrega_id'].update_cantidad(self, mercancia[2]['cantidad'])

    #                     mercancia_record.write({
    #                         'mercancia_id': mercancia_traslado.mercancia_id.id,
    #                         'cantidad': mercancia[2]['cantidad'],
    #                         'zona_almacen_id': mercancia[2]['zona_almacen_entrega_id'],
    #                         'precio': mercancia[2]['precio'],
    #                     })
    #     return res
    

    # mercancia_traslado_id = fields.Many2one('traslado.mercancia', string='ID Mercancia Traslado')
    # direccion_mercancia = fields.Selection([
    #     ('puerto', 'Puerto'),
    #     ('zona_almacen', 'Zona de Almacen'),
    # ], string='Dir. Mercancia', copy=False, tracking=True, default='puerto')

    # precio = fields.Float(string='Precio', required=True)

    # cantidad = fields.Integer(string="Num. Mercancia", default=0, required=True)
    # cant_mercancia = fields.Selection([
    #     ('por_kilo', 'Por Kilo'),
    #     ('toneladas', 'Toneladas'),
    #     ('por_bultos', 'Por Bultos'),
    # ], string='Cant. Mercancia', copy=False, tracking=True, default='por_kilo')

    # @api.onchange('cantidad')
    # def cost_update(self):
    #     if self.cantidad:
    #         if self.mercancia_traslado_id.num_producto >= self.cantidad:
    #             self.mercancia_traslado_id.num_producto -= self.cantidad