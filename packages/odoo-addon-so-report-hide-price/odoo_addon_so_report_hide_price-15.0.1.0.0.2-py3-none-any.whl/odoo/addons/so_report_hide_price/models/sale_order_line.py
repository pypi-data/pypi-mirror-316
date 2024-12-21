# Copyright 2022 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    show_price_info_report = fields.Boolean(string="Price in Report", default=True)

    def _prepare_invoice_line(self, **optional_values):
        values = super()._prepare_invoice_line(**optional_values)
        if self.env["account.move.line"]._fields.get("show_price_info_report"):
            values["show_price_info_report"] = self.show_price_info_report
        return values
