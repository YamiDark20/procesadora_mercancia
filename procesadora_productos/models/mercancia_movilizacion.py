import datetime
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class MercanciaMovilizacion(models.Model):
    _name = 'movilizacion.mercancia'
    _description = 'Informacion de la mercancia que se van a mover.'

    # fecharealizacion = fields.Datetime(string='Fecha Realizacion', default=lambda d: fields.Datetime.now(), required=True)
    solicitud_movilizacion_id = fields.Many2one('movilizacion.solicitud', string='Solicitud', required=True)
    mercancia_traslado_id = fields.Many2one('traslado.mercancia', string='Envio de Puerto')
    zona_mercancia_id = fields.Many2one('zona.mercancia', string='Envio de Almacen')
    direccion_mercancia = fields.Selection([
        ('puerto', 'Puerto'),
        ('zona_almacen', 'Zona de Almacen'),
    ], string='Dir. Mercancia', copy=False, tracking=True, default='puerto', required=True)
    
    zona_almacen_entrega_id = fields.Many2one('zona.almacen', string='Zona de Entrega')

    precio = fields.Float(string='Precio', related='mercancia_traslado_id.precio', required=True)

    cantidad = fields.Integer(string="Num. Mercancia", default=0, required=True)
    cant_mercancia = fields.Selection([
        ('por_kilo', 'Por Kilo'),
        ('toneladas', 'Toneladas'),
        ('por_bultos', 'Por Bultos'),
    ], string='Cant. Mercancia', copy=False, tracking=True, default='por_kilo')
    # estado = fields.Selection([
    #     ('buena', 'Buena'),
    #     ('regular', 'Regular'),
    #     ('danada', 'Dañada'),
    # ], string='Estado', copy=False, tracking=True, default='buena')

    @api.onchange('cantidad')
    def cantidad_update(self):
        if self.cantidad:
            if self.mercancia_traslado_id.num_producto < self.cantidad:
                self.cantidad = self.mercancia_traslado_id.num_producto
            elif self.cantidad < 0:
                self.cantidad = 0
                
    def update_mercancia_traslado(self, cantidad_anterior, cantidad, mercancia_traslado_anterior, mercancia_traslado):
        traslado = self.env['traslado.mercancia'].browse(mercancia_traslado)
        # assert False, [traslado, mercancia_traslado]
        if traslado.exists():
            if cantidad != None:
                traslado.productos_sacados += cantidad

                traslado_mercancia_anterior = self.env['traslado.mercancia'].browse(mercancia_traslado_anterior.id)
                traslado_mercancia_anterior.productos_sacados -= cantidad_anterior
                return traslado, traslado_mercancia_anterior
            else:
                
                traslado.productos_sacados += cantidad_anterior

                traslado_mercancia_anterior = self.env['traslado.mercancia'].browse(mercancia_traslado_anterior.id)
                traslado_mercancia_anterior.productos_sacados -= cantidad_anterior
                return traslado.mercancia_id.id, traslado_mercancia_anterior.mercancia_id.id
        else:
            # assert False, "enrtee"
            traslado_mercancia_anterior = self.env['traslado.mercancia'].browse(mercancia_traslado_anterior.id)
            traslado_mercancia_anterior.productos_sacados += (cantidad - cantidad_anterior)

    def update_zona_almacen(self, cantidad_anterior, cantidad, zona_mercancia, zona_mercancia_anterior):
        traslado = self.env['zona.mercancia'].browse(zona_mercancia)
        # assert False, [traslado, mercancia_traslado]
        if traslado.exists():
            if cantidad != None:
                traslado.productos_sacados += cantidad

                traslado_mercancia_anterior = self.env['zona.mercancia'].browse(zona_mercancia_anterior.id)
                traslado_mercancia_anterior.productos_sacados -= cantidad_anterior
                return traslado, traslado_mercancia_anterior
            else:
                
                traslado.productos_sacados += cantidad_anterior

                traslado_mercancia_anterior = self.env['zona.mercancia'].browse(zona_mercancia_anterior.id)
                traslado_mercancia_anterior.productos_sacados -= cantidad_anterior
                return traslado.mercancia_id.id, traslado_mercancia_anterior.mercancia_id.id
        else:
            # assert False, "enrtee"
            traslado_mercancia_anterior = self.env['zona.mercancia'].browse(zona_mercancia_anterior.id)
            traslado_mercancia_anterior.productos_sacados += (cantidad - cantidad_anterior)
        
    def update_zona_mercancia(self, cantidad_anterior, cantidad, mercancia_traslado_anterior, mercancia_traslado, object_a_crear, zona_almacen_anterior, zona_almacen_nuevo):
        if zona_almacen_nuevo == None:
            if cantidad != None:
                zona_mercancia = self.env['zona.mercancia'].search([('mercancia_id', '=', mercancia_traslado),('zona_almacen_id', '=', zona_almacen_anterior.id)], limit=1)
                if zona_mercancia:
                    zona_mercancia.cantidad += (cantidad - cantidad_anterior)
                else:
                    # self.env['zona.mercancia'].create(object_a_crear)

                    zona_mercancia = self.env['zona.mercancia'].search([('mercancia_id', '=', mercancia_traslado_anterior),('zona_almacen_id', '=', zona_almacen_anterior.id)], limit=1)

                    if zona_mercancia:
                        zona_mercancia.cantidad += (cantidad - cantidad_anterior)
                    else:
                        self.env['zona.mercancia'].create(object_a_crear)
            else:
                zona_mercancia = self.env['zona.mercancia'].search([('mercancia_id', '=', mercancia_traslado),('zona_almacen_id', '=', zona_almacen_anterior.id)], limit=1)

                if zona_mercancia:
                    zona_mercancia.cantidad += cantidad_anterior
                else:
                    self.env['zona.mercancia'].create(object_a_crear)
        else:
            if cantidad != None:
                zona_mercancia = self.env['zona.mercancia'].search([('mercancia_id', '=', mercancia_traslado),('zona_almacen_id', '=', zona_almacen_nuevo.id)], limit=1)
            else:
                if mercancia_traslado == None:
                    zona_mercancia = self.env['zona.mercancia'].search([('mercancia_id', '=', mercancia_traslado_anterior),('zona_almacen_id', '=', zona_almacen_anterior.id)], limit=1)
                    if zona_mercancia:
                        zona_mercancia.cantidad -= cantidad_anterior

                        zona_mercancia_new = self.env['zona.mercancia'].search([('mercancia_id', '=', mercancia_traslado_anterior),('zona_almacen_id', '=', zona_almacen_nuevo)], limit=1)
                        if zona_mercancia_new.exists():
                            zona_mercancia_new.cantidad -= cantidad_anterior
                        else:
                            self.env['zona.mercancia'].create(object_a_crear)
                    else:
                        self.env['zona.mercancia'].create(object_a_crear)
                        # zona_mercancia = self.env['zona.mercancia'].search([('mercancia_id', '=', mercancia_traslado),('zona_almacen_id', '=', zona_almacen_nuevo.id)], limit=1)

    def write(self, vals):
        for record in self:
            cantidad_anterior = record.cantidad
            
            if 'cantidad' in vals:
                nueva_cantidad = vals['cantidad']

                if 'direccion_mercancia' in vals and vals['direccion_mercancia'] == 'puerto':
                    if 'mercancia_traslado_id' in vals:
                        self.update_mercancia_traslado( cantidad_anterior, nueva_cantidad, record.mercancia_traslado_id, vals['mercancia_traslado_id'])

                        zona_mercancia = self.env['zona.mercancia'].search([
                            ('mercancia_id', '=', vals['mercancia_traslado_id']),
                            ('zona_almacen_id', '=', record.zona_almacen_entrega_id.id)
                        ], limit=1)

                        if zona_mercancia:
                            zona_mercancia.cantidad += (nueva_cantidad - cantidad_anterior)
                        else:
                            self.env['zona.mercancia'].create({
                                'mercancia_id': vals.get('mercancia_traslado_id.mercancia_id'),
                                'zona_almacen_id': record.zona_almacen_entrega_id.id,
                                'cantidad': nueva_cantidad,
                                'precio': record.precio,
                            })
                else:
                    if 'mercancia_traslado_id' in vals:
                        traslado, traslado_anterior = self.update_mercancia_traslado( cantidad_anterior, nueva_cantidad, record.mercancia_traslado_id, vals['mercancia_traslado_id'])

                        self.update_zona_mercancia( cantidad_anterior, nueva_cantidad, traslado.mercancia_id.id, None, {
                            'mercancia_id': traslado.mercancia_id.id,
                            'zona_almacen_id': record.zona_almacen_entrega_id.id,
                            'cantidad': nueva_cantidad,
                            'precio': record.precio,
                        }, record.zona_almacen_entrega_id, None)

                        # zona_mercancia = self.env['zona.mercancia'].search([
                        #     ('mercancia_id', '=', traslado.mercancia_id.id),
                        #     ('zona_almacen_id', '=', record.zona_almacen_entrega_id.id)
                        # ], limit=1)

                        # if zona_mercancia:
                        #     zona_mercancia.cantidad += (nueva_cantidad - cantidad_anterior)
                        # else:
                        #     self.env['zona.mercancia'].create({
                        #         'mercancia_id': traslado.mercancia_id.id,
                        #         'zona_almacen_id': record.zona_almacen_entrega_id.id,
                        #         'cantidad': nueva_cantidad,
                        #         'precio': record.precio,
                        #     })
                    else:
                        self.update_mercancia_traslado( cantidad_anterior, nueva_cantidad, record.mercancia_traslado_id, None)

                        self.update_zona_mercancia( cantidad_anterior, nueva_cantidad, record.mercancia_traslado_id.mercancia_id.id, None, {
                            'mercancia_id': record.mercancia_traslado_id.mercancia_id.id,
                            'zona_almacen_id': record.zona_almacen_entrega_id.id,
                            'cantidad': nueva_cantidad,
                            'precio': record.precio,
                        }, record.zona_almacen_entrega_id, None)
                    
                        # zona_mercancia = self.env['zona.mercancia'].search([
                        #     ('mercancia_id', '=', record.mercancia_traslado_id.mercancia_id.id),
                        #     ('zona_almacen_id', '=', record.zona_almacen_entrega_id.id)
                        # ], limit=1)

                        # if zona_mercancia:
                        #     zona_mercancia.cantidad += (nueva_cantidad - cantidad_anterior)
                        # else:
                        #     self.env['zona.mercancia'].create({
                        #         'mercancia_id': record.mercancia_traslado_id.mercancia_id.id,
                        #         'zona_almacen_id': record.zona_almacen_entrega_id.id,
                        #         'cantidad': nueva_cantidad,
                        #         'precio': record.precio,
                        #     })
            else:
                if 'direccion_mercancia' in vals and vals['direccion_mercancia'] == 'puerto':
                    pass
                elif 'direccion_mercancia' in vals and vals['direccion_mercancia'] == 'zona_almacen':
                    if 'zona_mercancia_id' in vals:
                        traslado, traslado_anterior = self.update_zona_almacen( cantidad_anterior, None, record.zona_mercancia_id, vals['zona_mercancia_id'])
                    else:
                        pass

                else:
                    if 'mercancia_traslado_id' in vals:

                        traslado_mercancia_id, traslado_mercancia_id_anterior = self.update_mercancia_traslado( cantidad_anterior, None, record.mercancia_traslado_id, vals['mercancia_traslado_id'])
                            
                        if traslado_mercancia_id != traslado_mercancia_id_anterior:
                            zona_mercancia_anterior = self.env['zona.mercancia'].search([
                            ('mercancia_id', '=', traslado_mercancia_id_anterior),
                            ('zona_almacen_id', '=', record.zona_almacen_entrega_id.id)
                            ], limit=1)

                            if zona_mercancia_anterior:
                                zona_mercancia_anterior.cantidad -= cantidad_anterior

                            zona_mercancia = self.env['zona.mercancia'].search([
                            ('mercancia_id', '=', traslado_mercancia_id),
                            ('zona_almacen_id', '=', record.zona_almacen_entrega_id.id)
                            ], limit=1)

                            if zona_mercancia:
                                zona_mercancia.cantidad += cantidad_anterior
                            else:
                                self.env['zona.mercancia'].create({
                                    'mercancia_id': traslado_mercancia_id,
                                    'zona_almacen_id': record.zona_almacen_entrega_id.id,
                                    'cantidad': cantidad_anterior,
                                    'precio': record.precio,
                                })
                    else:
                        if 'zona_almacen_entrega_id' in vals:
                            self.update_zona_mercancia( cantidad_anterior, None, record.mercancia_traslado_id.mercancia_id.id, None, {
                                'mercancia_id': record.mercancia_traslado_id.mercancia_id.id,
                                'zona_almacen_id': vals['zona_almacen_entrega_id'],
                                'cantidad': cantidad_anterior,
                                'precio': record.precio,
                            }, record.zona_almacen_entrega_id, vals['zona_almacen_entrega_id'])

            res = super(MercanciaMovilizacion, self).write(vals)
            return res

    @api.onchange('direccion_mercancia')
    def onchange_direccion_mercancia(self):
        if self.direccion_mercancia == 'puerto':
            self.zona_mercancia_id = False
            self.mercancia_traslado_id = True
        elif self.direccion_mercancia == 'zona_almacen':
            self.zona_mercancia_id = True     # Activar el campo 1
            self.mercancia_traslado_id = False    # Desactivar el campo 2