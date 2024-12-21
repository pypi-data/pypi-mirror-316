# Copyright 2023 Ángel García de la Chica Herrera <angel.garcia@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    show_line_report = fields.Boolean(
        string="Line in Report",
        help="If True the line will be displayed in the sales "
        "reports. If False, the line will not be displayed",
        default=True,
    )
