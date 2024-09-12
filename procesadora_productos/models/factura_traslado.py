import datetime
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class FacturaTraslado(models.Model):
    _name = 'traslado.factura'
    _description = 'Informacion de la Factura de traslado'

    fecharealizacion = fields.Datetime(string='Fecha Realizacion', default=lambda d: fields.Datetime.now(), required=True)
    moneda = fields.Selection([
        ('dolars', '$'),
        ('bolivars', 'Bs.'),
    ], string='Moneda', copy=False, tracking=True, default='bolivars', required=True)
    guia_movilizacion_id = fields.Many2one('empresa.guia_movilizacion', string='ID Guia Mov.',      required=True)
    gasto_nacional = fields.Float(string='Gasto Nac.', required=True)
    tasa_gasto_nacional = fields.Float(string='Tasa Gasto Nac.', compute='compute_total', store=True)
    
    gasto_extrajero = fields.Float(string='Gasto Extranjero', required=True)
    descuento = fields.Integer(string="Descuento", default=0)
    total = fields.Float(string="Total", compute='compute_total', store=False)

    @api.constrains('descuento')
    def validar_descuento(self):
        for record in self:
            if record.descuento < 0 or record.descuento > 100:
                raise ValidationError("El descuento debe estar entre 0 y 100.")

    @api.depends('gasto_nacional', 'gasto_extrajero', 'descuento')
    def _compute_total(self):
        for record in self:
            monto_total = record.gasto_nacional + record.gasto_extrajero
            record.total = monto_total + (monto_total * record.descuento)
            record.tasa_gasto_nacional = (record.gasto_nacional / monto_total) * (100 - record.descuento)