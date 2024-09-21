import datetime
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SolicitudMovilizacion(models.Model):
    _name = 'movilizacion.solicitud'

class MercanciaMovilizacion(models.Model):
    _name = 'movilizacion.mercancia'
    