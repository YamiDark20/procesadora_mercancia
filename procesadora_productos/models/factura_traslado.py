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
    gasto_nacional = fields.Float(string='Gasto Nac.', required=True, default=0.0)
    tasa_gasto_nacional = fields.Float(string='Tasa Gasto Nac.', compute='compute_total', store=True)

    mercancia_traslado_ids = fields.One2many('traslado.mercancia', 'factura_traslado_id', string='Id Mercancia')
    
    gasto_extrajero = fields.Float(string='Gasto Extranjero', required=True, default=0.0)
    descuento = fields.Integer(string="Descuento", default=0)
    total = fields.Float(string="Total", compute='compute_total', store=False)

    # sequence_number = fields.Char(string='Secuencia', required=True, index=True, default=lambda self: self.env['ir.sequence'].next_by_code('traslado.factura'), readonly=True)
    id_guia_movilizacion = fields.Char(string='ID Guia Mov.', related='guia_movilizacion_id.sequence_number', store=False)

    sequence_number = fields.Char(string='Secuencia', index=True, readonly=True)

    @api.model
    def create(self, vals):
        if 'sequence_number' not in vals:
            vals['sequence_number'] = self.env['ir.sequence'].next_by_code('traslado.factura')
        return super(FacturaTraslado, self).create(vals)
    
    # nombre_moneda = fields.Char(string='Nombre de la Moneda', compute='compute_nombre_moneda', store=False)

    # def compute_nombre_moneda(self):
    #     for record in self:
    #         if record.moneda == '$':
    #             record.nombre_moneda = 'Dólar'
    #         elif record.moneda == 'Bs.':
    #             record.nombre_moneda = 'Euro'
    #         else:
    #             record.nombre_moneda = 'Moneda Desconocida'

    @api.constrains('descuento')
    def validar_descuento(self):
        for record in self:
            if record.descuento < 0 or record.descuento > 100:
                raise ValidationError("El descuento debe estar entre 0 y 100.")

    @api.depends('gasto_nacional', 'gasto_extrajero', 'descuento', 'mercancia_traslado_ids')
    def compute_total(self):
        for record in self:
            total_mercancia = 0
            for mercancia in record.mercancia_traslado_ids:
                total_mercancia += mercancia.precio * mercancia.num_producto
            monto_total = record.gasto_nacional + record.gasto_extrajero + total_mercancia
            record.total = monto_total + (monto_total * record.descuento)
            try:
                record.tasa_gasto_nacional = (record.gasto_nacional / monto_total) * (100 - record.descuento)
            except:
                record.tasa_gasto_nacional = 0.0