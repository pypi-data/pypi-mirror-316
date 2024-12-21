# Copyright 2022 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    has_show_price_report_lines = fields.Boolean(
        compute="_compute_has_show_price_report_lines",
    )
    hide_tax_information = fields.Boolean(compute="_compute_hide_tax_information")

    def _compute_has_show_price_report_lines(self):
        for sel in self:
            sel.has_show_price_report_lines = any(
                line.show_price_info_report
                for line in sel.order_line.filtered(lambda a: not a.display_type)
            )

    def _compute_hide_tax_information(self):
        for sel in self:
            sel.hide_tax_information = (
                self.env["ir.config_parameter"]
                .sudo()
                .get_param("so_report_hide_price.hide_taxes")
            )

    def action_activate_show_price_info_report(self):
        self.mapped("order_line").filtered(
            lambda a: not a.show_price_info_report
        ).write({"show_price_info_report": True})

    def action_deactivate_show_price_info_report(self):
        self.mapped("order_line").filtered(lambda a: a.show_price_info_report).write(
            {"show_price_info_report": False}
        )
