# Copyright 2023 Ángel García de la Chica <angel.garcia@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "SO Report Hide Lines",
    "summary": "SO Report Hide Lines",
    "version": "15.0.1.0.0",
    "category": "Sale",
    "website": "https://github.com/sygel-technology/sy-sale-reporting",
    "author": "Sygel, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "sale",
    ],
    "data": ["views/sale_views.xml", "report/sale_report_templates.xml"],
}
