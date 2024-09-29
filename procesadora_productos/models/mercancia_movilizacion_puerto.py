import datetime
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class MercanciaMovilizacionPuerto(models.Model):
    _name = 'movilizacion.puertomercancia'
    _description = 'Informacion de la mercancia que se van a mover.'

    solicitud_movilizacion_id = fields.Many2one('movilizacion.puertosolicitud', string='Solicitud', required=True)
    mercancia_traslado_id = fields.Many2one('traslado.mercancia', string='Envio de Puerto')

    precio = fields.Float(string='Precio', related='mercancia_traslado_id.precio', required=True)
    estado = fields.Selection(string="Estado", related='mercancia_traslado_id.estado', required=True)

    cantidad = fields.Integer(string="Num. Mercancia", default=0, required=True)
    cant_mercancia = fields.Selection([
        ('por_kilo', 'Por Kilo'),
        ('toneladas', 'Toneladas'),
        ('por_bultos', 'Por Bultos'),
    ], string='Cant. Mercancia', copy=False, tracking=True, default='por_kilo')

    @api.onchange('cantidad')
    def cantidad_update(self):
        if self.cantidad:
            if self.mercancia_traslado_id.num_producto < self.cantidad:
                self.cantidad = self.mercancia_traslado_id.num_producto
            elif self.cantidad < 0:
                self.cantidad = 0
    
    @api.model
    def create(self, vals):
        if 'sequence_number' not in vals:
            traslado = self.env['traslado.mercancia'].browse(vals['mercancia_traslado_id'])
            traslado.productos_sacados += vals['cantidad']

            solicitud_movilizacion = self.env['movilizacion.puertosolicitud'].browse(vals['solicitud_movilizacion_id'])

            zona_mercancia = self.env['zona.mercancia'].search([('mercancia_id', '=', traslado.mercancia_id.id),('zona_almacen_id', '=', solicitud_movilizacion.zona_almacen_entrega_id.id), ('estado', '=', traslado.estado)], limit=1)

            if zona_mercancia:
                zona_mercancia.cantidad += vals['cantidad']
            else:
                self.env['zona.mercancia'].create({
                    'mercancia_id': traslado.mercancia_id.id,
                    'zona_almacen_id': solicitud_movilizacion.zona_almacen_entrega_id.id,
                    'cantidad': vals['cantidad'],
                    'estado': traslado.estado,
                    'precio': traslado.precio,
                })

            # vals['sequence_number'] = self.env['ir.sequence'].next_by_code('empresa.mercancia')
        return super(MercanciaMovilizacionPuerto, self).create(vals)

    def write(self, vals):
        for record in self:
            cantidad_anterior = record.cantidad
            if 'cantidad' in vals:
                nueva_cantidad = vals['cantidad']
                if 'mercancia_traslado_id' in vals:
                    traslado = self.env['traslado.mercancia'].browse(vals['mercancia_traslado_id'])
                    traslado.productos_sacados += nueva_cantidad

                    traslado_mercancia_anterior = self.env['traslado.mercancia'].browse(record.mercancia_traslado_id.id)
                    traslado_mercancia_anterior.productos_sacados -= cantidad_anterior

                    #######
                    if traslado.mercancia_id.id == traslado_mercancia_anterior.mercancia_id.id:
                        if traslado.estado == traslado_mercancia_anterior.estado:
                            zona_mercancia = self.env['zona.mercancia'].search([('mercancia_id', '=', traslado.mercancia_id.id),('zona_almacen_id', '=', record.solicitud_movilizacion_id.zona_almacen_entrega_id.id), ('estado', '=', traslado.estado)], limit=1)
                            zona_mercancia.cantidad += (nueva_cantidad - cantidad_anterior)
                        else:
                            zona_mercancia = self.env['zona.mercancia'].search([('mercancia_id', '=', traslado.mercancia_id.id),('zona_almacen_id', '=', record.solicitud_movilizacion_id.zona_almacen_entrega_id.id), ('estado', '=', traslado.estado)], limit=1)
                            zona_mercancia.cantidad += nueva_cantidad

                            zona_mercancia_anterior = self.env['zona.mercancia'].search([('mercancia_id', '=', traslado_mercancia_anterior.mercancia_id.id),('zona_almacen_id', '=', record.solicitud_movilizacion_id.zona_almacen_entrega_id.id), ('estado', '=', traslado_mercancia_anterior.estado)], limit=1)

                            zona_mercancia_anterior.cantidad -=  cantidad_anterior
                    else:
                        zona_mercancia = self.env['zona.mercancia'].search([('mercancia_id', '=', traslado.mercancia_id.id),('zona_almacen_id', '=', record.solicitud_movilizacion_id.zona_almacen_entrega_id.id), ('estado', '=', traslado.estado)], limit=1)

                        if zona_mercancia:
                            zona_mercancia.cantidad += nueva_cantidad
                        else:
                            self.env['zona.mercancia'].create({
                                'mercancia_id': traslado.mercancia_id.id,
                                'zona_almacen_id': record.solicitud_movilizacion_id.zona_almacen_entrega_id.id,
                                'cantidad': nueva_cantidad,
                                'estado': traslado.estado,
                                'precio': record.precio,
                            })

                        zona_mercancia_anterior = self.env['zona.mercancia'].search([('mercancia_id', '=', traslado_mercancia_anterior.mercancia_id.id),('zona_almacen_id', '=', record.solicitud_movilizacion_id.zona_almacen_entrega_id.id), ('estado', '=', traslado_mercancia_anterior.estado)], limit=1)

                        zona_mercancia_anterior.cantidad -=  cantidad_anterior

                    #Cambio de mercancia (validation)
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
                    traslado_mercancia_anterior = self.env['traslado.mercancia'].browse(record.mercancia_traslado_id.id)
                    traslado_mercancia_anterior.productos_sacados += (nueva_cantidad - cantidad_anterior)

                    zona_mercancia = self.env['zona.mercancia'].search([('mercancia_id', '=', traslado_mercancia_anterior.mercancia_id.id),('zona_almacen_id', '=', record.solicitud_movilizacion_id.zona_almacen_entrega_id.id), ('estado', '=', traslado_mercancia_anterior.estado)], limit=1)
                    zona_mercancia.cantidad += (nueva_cantidad - cantidad_anterior)
            else:
                if 'mercancia_traslado_id' in vals:
                    traslado = self.env['traslado.mercancia'].browse(vals['mercancia_traslado_id'])
                    traslado.productos_sacados += cantidad_anterior

                    traslado_mercancia_anterior = self.env['traslado.mercancia'].browse(record.mercancia_traslado_id.id)
                    traslado_mercancia_anterior.productos_sacados -= cantidad_anterior

                    #######
                    if traslado.mercancia_id.id == traslado_mercancia_anterior.mercancia_id.id:
                        # if traslado.estado == traslado_mercancia_anterior.estado:
                        #     zona_mercancia = self.env['zona.mercancia'].search([('mercancia_id', '=', traslado.mercancia_id.id),('zona_almacen_id', '=', record.solicitud_movilizacion_id.zona_almacen_entrega_id.id), ('estado', '=', traslado.estado)], limit=1)
                        #     zona_mercancia.cantidad += (nueva_cantidad - cantidad_anterior)
                        # else:
                        if traslado.estado == traslado_mercancia_anterior.estado:
                            zona_mercancia = self.env['zona.mercancia'].search([('mercancia_id', '=', traslado.mercancia_id.id),('zona_almacen_id', '=', record.solicitud_movilizacion_id.zona_almacen_entrega_id.id), ('estado', '=', traslado.estado)], limit=1)
                            zona_mercancia.cantidad += cantidad_anterior

                            zona_mercancia_anterior = self.env['zona.mercancia'].search([('mercancia_id', '=', traslado_mercancia_anterior.mercancia_id.id),('zona_almacen_id', '=', record.solicitud_movilizacion_id.zona_almacen_entrega_id.id), ('estado', '=', traslado_mercancia_anterior.estado)], limit=1)

                            zona_mercancia_anterior.cantidad -=  cantidad_anterior
                    else:
                        zona_mercancia = self.env['zona.mercancia'].search([('mercancia_id', '=', traslado.mercancia_id.id),('zona_almacen_id', '=', record.solicitud_movilizacion_id.zona_almacen_entrega_id.id), ('estado', '=', traslado.estado)], limit=1)

                        if zona_mercancia:
                            zona_mercancia.cantidad += cantidad_anterior
                        else:
                            self.env['zona.mercancia'].create({
                                'mercancia_id': traslado.mercancia_id.id,
                                'zona_almacen_id': record.solicitud_movilizacion_id.zona_almacen_entrega_id.id,
                                'cantidad': cantidad_anterior,
                                'estado': traslado.estado,
                                'precio': traslado.precio,
                            })

                        zona_mercancia_anterior = self.env['zona.mercancia'].search([('mercancia_id', '=', traslado_mercancia_anterior.mercancia_id.id),('zona_almacen_id', '=', record.solicitud_movilizacion_id.zona_almacen_entrega_id.id), ('estado', '=', traslado_mercancia_anterior.estado)], limit=1)

                        zona_mercancia_anterior.cantidad -=  cantidad_anterior

            res = super(MercanciaMovilizacionPuerto, self).write(vals)
            return res
        
    def unlink(self):
        for record in self:
            traslado_mercancia_anterior = self.env['traslado.mercancia'].browse(record.mercancia_traslado_id.id)
            traslado_mercancia_anterior.productos_sacados -= record.cantidad

            zona_mercancia = self.env['zona.mercancia'].search([('mercancia_id', '=', traslado_mercancia_anterior.mercancia_id.id),('zona_almacen_id', '=', record.solicitud_movilizacion_id.zona_almacen_entrega_id.id), ('estado', '=', traslado_mercancia_anterior.estado)], limit=1)
            zona_mercancia.cantidad -= record.cantidad
        return super(MercanciaMovilizacionPuerto, self).unlink()