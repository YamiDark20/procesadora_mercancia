import datetime
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Pago(models.Model):
    _name = 'factura.pago'
    _description = 'Informacion de la factura realizada a un cliente'

    fecharealizacion = fields.Datetime(string='Fecha Realizacion', default=lambda d: fields.Datetime.now(), required=True)
    cliente_id = fields.Many2one('res.partner', string='Id. Cliente')

    # zona_mercancia_id = fields.Many2one('zona.mercancia', string='Zona de Entrega')
    mercancia_factura_ids = fields.One2many('factura.mercancia', 'factura_pago_id', string='Mercancias')

    totalpagado = fields.Float(string='Total', compute='compute_total', store=False)
    state = fields.Selection([
        ('no_pagado', 'No Pagado'),
        ('por_cuota', 'Por Cuota'),
        ('pagado', 'Pagado'),

    ], string='Pagado?', readonly=True, copy=False, index=True, tracking=True, default='no_pagado')
    # fields.Boolean(string="Pagado?", default=True)

    metodopago = fields.Selection([
        ('pago_movil', 'Pago Movil'),
        ('efectivo', 'Efectivo'),
        ('por_tarjeta', 'Por Tarjeta'),
    ], string='Metodo de Pago', copy=False, tracking=True, default='efectivo')

    num_cuenta = fields.Char(string='Num. Cuenta', size=9)
    banco = fields.Selection([
        ('banco_vzla', 'Banco de Vzla'),
        ('mercantil', 'Mercantil'),
        ('banesco', 'Banesco'),
        ('banco_provincial', 'Banco Provincial'),
    ], string='Tipo de Banco', copy=False, tracking=True, default='banco_vzla')
    # fields.Char(string='Banco', required=True, size=9)

    informacion = fields.Text(string='Informacion')

    sequence_number = fields.Char(string='ID Factura', index=True, readonly=True)

    @api.model
    def create(self, vals):
        if 'sequence_number' not in vals:
            vals['sequence_number'] = self.env['ir.sequence'].next_by_code('factura.pago')
        return super(Pago, self).create(vals)
    
    def set_to_no_pagado(self):
        return self.write({'state': 'por_cuota'})

    def set_to_por_cuota(self):
        return self.write({'state': 'pagado'})

    def set_to_pagado(self):
        return self.write({'state': 'pagado'})
    
    def name_get(self):
        result = []
        for record in self:
            name = f"{record.sequence_number}"
            result.append((record.id, name))
        return result
    
    @api.depends('mercancia_factura_ids')
    def compute_total(self):
        for record in self:
            total_mercancia = 0
            for mercancia in record.mercancia_factura_ids:
                total_mercancia += (mercancia.precio -(mercancia.precio * (mercancia.descuento / 100))) * mercancia.cantidad
            # monto_total = total_mercancia
            record.totalpagado = total_mercancia