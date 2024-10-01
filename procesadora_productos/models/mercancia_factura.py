import datetime
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class MercanciaFactura(models.Model):
    _name = 'factura.mercancia'
    _description = 'Informacion de la mercancia que pago un cliente.'

    factura_pago_id = fields.Many2one('factura.pago', string='Factura', required=True)
    
    zona_mercancia_id = fields.Many2one('zona.mercancia', string='ID Mercancia')
    # mercancia_id = fields.Many2one('empresa.mercancia', string='Id. Mercancia')
    nombre_mercancia = fields.Char(string="Nombre de Mercancia", related='zona_mercancia_id.mercancia_id.nombre', required=True)
    estado = fields.Selection(string="Estado", related='zona_mercancia_id.estado')

    precio = fields.Float(string='Precio', related='zona_mercancia_id.precio', required=True)

    cantidad = fields.Integer(string="Cantidad", default=0, required=True)
    descuento = fields.Integer(string="% Descuento", default=0)

    @api.onchange('cantidad')
    def cantidad_update(self):
        if self.cantidad:
            if self.zona_mercancia_id.cantidad < self.cantidad:
                self.cantidad = self.zona_mercancia_id.cantidad
            elif self.cantidad < 0:
                self.cantidad = 0
                
    @api.onchange('descuento')
    def descuento_update(self):
        if self.descuento:
            if self.descuento > 80:
                self.descuento = 80
            elif self.descuento < 0:
                self.descuento = 0
    
    @api.model
    def create(self, vals):
        if 'sequence_number' not in vals:
            traslado = self.env['zona.mercancia'].browse(vals['zona_mercancia_id'])
            traslado.cantidad -= vals['cantidad']
        return super(MercanciaFactura, self).create(vals)

    def write(self, vals):
        for record in self:
            cantidad_anterior = record.cantidad
            if 'cantidad' in vals:
                nueva_cantidad = vals['cantidad']
                if 'zona_mercancia_id' in vals:
                    traslado = self.env['zona.mercancia'].browse(vals['zona_mercancia_id'])
                    traslado.cantidad -= nueva_cantidad

                    traslado_mercancia_anterior = self.env['zona.mercancia'].browse(record.zona_mercancia_id.id)
                    traslado_mercancia_anterior.cantidad += cantidad_anterior

                    # traslado_mercancia_anterior = self.env['traslado.mercancia'].browse(record.mercancia_traslado_id.id)
                    # traslado_mercancia_anterior.productos_sacados -= cantidad_anterior

                    # #Cambio de mercancia (validation)
                    # if traslado.mercancia_id.id == traslado_mercancia_anterior.mercancia_id.id:
                    #     zona_mercancia = self.env['zona.mercancia'].search([('mercancia_id', '=', traslado.mercancia_id.id),('zona_almacen_id', '=', record.solicitud_movilizacion_id.zona_almacen_entrega_id.id)], limit=1)
                    #     zona_mercancia.cantidad += (nueva_cantidad - cantidad_anterior)
                    # else:
                    #     zona_mercancia = self.env['zona.mercancia'].search([('mercancia_id', '=', traslado.mercancia_id.id),('zona_almacen_id', '=', record.solicitud_movilizacion_id.zona_almacen_entrega_id.id)], limit=1)

                    #     if zona_mercancia:
                    #         zona_mercancia.cantidad += nueva_cantidad
                    #     else:
                    #         self.env['zona.mercancia'].create({
                    #             'mercancia_id': traslado.mercancia_id.id,
                    #             'zona_almacen_id': record.solicitud_movilizacion_id.zona_almacen_entrega_id.id,
                    #             'cantidad': nueva_cantidad,
                    #             'precio': record.precio,
                    #         })

                    #     zona_mercancia_anterior = self.env['zona.mercancia'].search([('mercancia_id', '=', traslado_mercancia_anterior.mercancia_id.id),('zona_almacen_id', '=', record.solicitud_movilizacion_id.zona_almacen_entrega_id.id)], limit=1)

                    #     zona_mercancia_anterior.cantidad -=  cantidad_anterior
                else:
                    traslado = self.env['zona.mercancia'].browse(record.zona_mercancia_id.id)
                    traslado.cantidad += (cantidad_anterior - nueva_cantidad)
            else:
                if 'zona_mercancia_id' in vals:
                    traslado = self.env['zona.mercancia'].browse(vals['zona_mercancia_id'])
                    traslado.cantidad -= cantidad_anterior

                    traslado_mercancia_anterior = self.env['zona.mercancia'].browse(record.zona_mercancia_id.id)
                    traslado_mercancia_anterior.cantidad += cantidad_anterior

            res = super(MercanciaFactura, self).write(vals)
            return res

    # @api.model
    # def create(self, vals):
    #     if 'sequence_number' not in vals:
    #         traslado = self.env['zona.mercancia'].browse(vals['zona_mercancia_id'])
    #         traslado.cantidad -= vals['cantidad']

    #         solicitud_movilizacion = self.env['movilizacion.almacensolicitud'].browse(vals['solicitud_movilizacion_almacen_id'])

    #         zona_mercancia = self.env['zona.mercancia'].search([('mercancia_id', '=', traslado.mercancia_id.id),('zona_almacen_id', '=', solicitud_movilizacion.zona_almacen_entrega_id.id)], limit=1)

    #         if zona_mercancia:
    #             zona_mercancia.cantidad += vals['cantidad']
    #         else:
    #             self.env['zona.mercancia'].create({
    #                 'mercancia_id': traslado.mercancia_id.id,
    #                 'zona_almacen_id': solicitud_movilizacion.zona_almacen_entrega_id.id,
    #                 'cantidad': vals['cantidad'],
    #                 'precio': vals['precio'],
    #             })

    #         # vals['sequence_number'] = self.env['ir.sequence'].next_by_code('empresa.mercancia')
    #     return super(MercanciaMovilizacionAlmacen, self).create(vals)

    # def write(self, vals):
    #     for record in self:
    #         cantidad_anterior = record.cantidad
    #         if 'cantidad' in vals:
    #             nueva_cantidad = vals['cantidad']
    #             if 'zona_mercancia_id' in vals:
    #                 traslado = self.env['zona.mercancia'].browse(vals['zona_mercancia_id'])
    #                 traslado.cantidad -= nueva_cantidad

    #                 traslado_mercancia_anterior = self.env['zona.mercancia'].browse(record.zona_mercancia_id.id)
    #                 traslado_mercancia_anterior.cantidad += cantidad_anterior

    #                 #Cambio de mercancia (validation)
    #                 if traslado.mercancia_id.id == traslado_mercancia_anterior.mercancia_id.id:
    #                     zona_mercancia = self.env['zona.mercancia'].search([('mercancia_id', '=', traslado.mercancia_id.id),('zona_almacen_id', '=', record.solicitud_movilizacion_almacen_id.zona_almacen_entrega_id.id)], limit=1)
    #                     zona_mercancia.cantidad += (nueva_cantidad - cantidad_anterior)
    #                 else:
    #                     zona_mercancia = self.env['zona.mercancia'].search([('mercancia_id', '=', traslado.mercancia_id.id),('zona_almacen_id', '=', record.solicitud_movilizacion_almacen_id.zona_almacen_entrega_id.id)], limit=1)

    #                     if zona_mercancia:
    #                         zona_mercancia.cantidad += nueva_cantidad
    #                     else:
    #                         self.env['zona.mercancia'].create({
    #                             'mercancia_id': traslado.mercancia_id.id,
    #                             'zona_almacen_id': record.solicitud_movilizacion_almacen_id.zona_almacen_entrega_id.id,
    #                             'cantidad': nueva_cantidad,
    #                             'precio': record.precio,
    #                         })

    #                     zona_mercancia_anterior = self.env['zona.mercancia'].search([('mercancia_id', '=', traslado_mercancia_anterior.mercancia_id.id),('zona_almacen_id', '=', record.solicitud_movilizacion_almacen_id.zona_almacen_entrega_id.id)], limit=1)

    #                     zona_mercancia_anterior.cantidad -=  cantidad_anterior
    #             else:
    #                 traslado_mercancia_anterior = self.env['zona.mercancia'].browse(record.zona_mercancia_id.id)
    #                 traslado_mercancia_anterior.cantidad += (cantidad_anterior - nueva_cantidad)

    #                 zona_mercancia = self.env['zona.mercancia'].search([('mercancia_id', '=', traslado_mercancia_anterior.mercancia_id.id),('zona_almacen_id', '=', record.solicitud_movilizacion_almacen_id.zona_almacen_entrega_id.id)], limit=1)
    #                 zona_mercancia.cantidad += (nueva_cantidad - cantidad_anterior)
    #         else:
    #             if 'zona_mercancia_id' in vals:
    #                 traslado = self.env['zona.mercancia'].browse(vals['zona_mercancia_id'])
    #                 traslado.cantidad -= cantidad_anterior

    #                 traslado_mercancia_anterior = self.env['zona.mercancia'].browse(record.zona_mercancia_id.id)
    #                 traslado_mercancia_anterior.cantidad += cantidad_anterior

    #         res = super(MercanciaMovilizacionAlmacen, self).write(vals)
    #         return res
        
    # def unlink(self):
    #     for record in self:
    #         traslado_mercancia_anterior = self.env['zona.mercancia'].browse(record.zona_mercancia_id.id)
    #         traslado_mercancia_anterior.cantidad += record.cantidad

    #         zona_mercancia = self.env['zona.mercancia'].search([('mercancia_id', '=', traslado_mercancia_anterior.mercancia_id.id),('zona_almacen_id', '=', record.solicitud_movilizacion_almacen_id.zona_almacen_entrega_id.id)], limit=1)
    #         zona_mercancia.cantidad -= record.cantidad
    #     return super(MercanciaMovilizacionAlmacen, self).unlink()