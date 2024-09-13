# -*- coding: utf-8 -*-
{
    'name': "procesadora_productos",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/procesadora_users.xml',
        'security/ir.model.access.csv',
        'views/empresa_view.xml',
        'views/guia_movilizacion_view.xml',
        'views/mercancia_view.xml',
        'views/factura_traslado.xml',
        # 'views/views.xml',
        # 'views/templates.xml',
    ],
    # 'icon': '/procesadora_productos/static/description/Logo_UDO.svg.png',
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': True,
}
