import datetime
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Empresa(models.Model):
    _name = 'empresa.empresa'
    # _inherit = 'res.partner'
    # _rec_name = 'lab_request_id'
    _description = 'Informacion de la Empresa'

    name = fields.Char(string='Nombre', compute='_compute_name', store=False)
    email = fields.Char(string='Email', compute='_compute_name', store=False)
    descripcion = fields.Text(string='Descripcion')
    # phone = fields.Char(string='Telefono', compute='_compute_phone', required=True)
    nif = fields.Char(string='NIF', size=9, required=True)
    tipo = fields.Selection([
        ('individual', 'Empresa Individual'),
        ('sociedad_anomina', 'Sociedad Anónima'),
        ('sociedad_limitada', 'Sociedad de Responsabilidad Limitada'),
        ('sociedad_colectiva', 'Sociedad Colectiva'),
        ('sociedad_comanditaria', 'Sociedad Comanditaria'),

    ], string='Tipo', copy=False, index=True, tracking=True, default='individual')
    # channel_ids = fields.Many2many(
    #     comodel_name='mail.channel',
    #     relation='empresa_channel_rel',  # Nombre de la tabla de relación
    #     column1='empresa_id',  # Nombre de la columna para empresa.empresa
    #     column2='channel_id',   # Nombre de la columna para mail.channel
    #     string='Channels'
    # )
    contacto_id = fields.Many2one(
        'res.partner', 
        string='Contacto Principal', 
        required=True,
        domain="[('is_company', '=', True)]"  # Asegúrate de que sea un contacto y no una empresa
    )
    image = fields.Binary(related='contacto_id.image_1920', string='Imagen', store=False)

    @api.depends('contacto_id')
    def _compute_name(self):
        for record in self:
            record.name = record.contacto_id.name
            record.email = record.contacto_id.email
            # record.image = record.contacto_id.image_1920
        
    # def _compute_email(self):
    #     self.email = self.contacto_id.email
    
    def set_to_individual(self):
        return self.write({'tipo': 'individual'})
    
    def set_to_sociedad_anomina(self):
        return self.write({'tipo': 'sociedad_anomina'})
    
    def set_to_sociedad_limitada(self):
        return self.write({'tipo': 'sociedad_limitada'})
    
    def set_to_sociedad_colectiva(self):
        return self.write({'tipo': 'sociedad_colectiva'})
    
    def set_to_sociedad_comanditaria(self):
        return self.write({'tipo': 'sociedad_comanditaria'})