import datetime
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Abono(models.Model):
    _name = 'abono.mercancia'
    _description = 'Informacion de la mercancia que abono un cliente.'

    fechaculminacion = fields.Datetime(string='Fecha Expiracion', default=lambda d: fields.Datetime.now(), required=True)
    
    factura_pago_id = fields.Many2one('factura.pago', string='Factura', required=True)

    # mercancia_factura_ids = fields.One2many(related='factura_pago_id.mercancia_factura_ids', string='Mercancias')

    state = fields.Selection([
        ('pendiente', 'Pendiente'),
        ('completado', 'Completado'),
    ], string='Estado', copy=False, tracking=True, default='pendiente')

    monto = fields.Float(string='Monto', compute='compute_total', store=True)
    abono = fields.Integer(string="% Abono", default=0)
    observacion = fields.Text(string='Observacion')

    sequence_number = fields.Char(string='ID Abono', index=True, readonly=True)

    # @api.onchange('cantidad')
    # def cantidad_update(self):
    #     if self.cantidad:
    #         if self.zona_mercancia_id.cantidad < self.cantidad:
    #             self.cantidad = self.zona_mercancia_id.cantidad
    #         elif self.cantidad < 0:
    #             self.cantidad = 0

    def set_to_pendiente(self):
        return self.write({'state': 'completado'})

    def set_to_completado(self):
        return self.write({'state': 'pendiente'})
    
    @api.depends('abono', 'factura_pago_id')
    def compute_total(self):
        for record in self:
            if record.factura_pago_id:
                if record.abono:
                    self.monto = record.factura_pago_id.totalpagado * (record.abono / 100)

    @api.onchange('abono')
    def abono_update(self):
        if self.abono:
            abono_restante = None
            for record in self:
                abonos = None
                if self.sequence_number:
                    abonos = self.env['abono.mercancia'].search([('factura_pago_id', '=', record.factura_pago_id.id), ('sequence_number', '!=', self.sequence_number)])
                else:
                    abonos = self.env['abono.mercancia'].search([('factura_pago_id', '=', record.factura_pago_id.id)])
                    # assert False, [abonos, record]
                # abonos = self.env['abono.mercancia'].search([('factura_pago_id', '=', record.factura_pago_id.id)])
                abono_restante = 100 - (sum(abono.abono for abono in abonos))
                # assert False, [abono_restante, self.abono, (sum(abono.abono for abono in abonos)), abonos]
            if self.abono > abono_restante:
                self.abono = abono_restante
            elif self.abono < 0:
                self.abono = 0
            # self.monto = record.factura_pago_id.totalpagado * (self.abono / 100)
            # assert False, [abono_restante, self.abono, (sum(abono.monto_abono for abono in abonos)), record.factura_pago_id.totalpagado, (self.abono / 100), (record.factura_pago_id.totalpagado * (self.abono / 100))]
    
    @api.model
    def create(self, vals):
        if 'sequence_number' not in vals:
            vals['sequence_number'] = self.env['ir.sequence'].next_by_code('abono.mercancia')
        return super(Abono, self).create(vals)

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
    #             else:
    #                 traslado = self.env['zona.mercancia'].browse(record.zona_mercancia_id.id)
    #                 traslado.cantidad += (cantidad_anterior - nueva_cantidad)
    #         else:
    #             if 'zona_mercancia_id' in vals:
    #                 traslado = self.env['zona.mercancia'].browse(vals['zona_mercancia_id'])
    #                 traslado.cantidad -= cantidad_anterior

    #                 traslado_mercancia_anterior = self.env['zona.mercancia'].browse(record.zona_mercancia_id.id)
    #                 traslado_mercancia_anterior.cantidad += cantidad_anterior

    #         res = super(MercanciaFactura, self).write(vals)
    #         return res

    def name_get(self):
        result = []
        for record in self:
            name = f"{record.sequence_number}"
            result.append((record.id, name))
        return result