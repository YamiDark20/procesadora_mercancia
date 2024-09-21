import datetime
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Cliente(models.Model):
    _name = 'empresa.cliente'
    _description = 'Informacion del cliente'

    
    cedula = fields.Char(string='Cedula', index=True, required=True)
    nombre = fields.Char(string='Nombre', required=True)
    apellido = fields.Char(string='Apellido', required=True)
    telefono = fields.Char(string='Telefono', required=True)
    email = fields.Char(string='Correo Electrónico', required=True)
    direccion = fields.Char(string='Direccion')
    
    def name_get(self):
        result = []
        for record in self:
            name = f"{record.cedula}"
            result.append((record.id, name))
        return result