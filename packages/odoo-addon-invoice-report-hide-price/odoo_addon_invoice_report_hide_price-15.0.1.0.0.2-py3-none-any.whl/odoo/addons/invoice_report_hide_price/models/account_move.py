# Copyright 2022 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    has_show_price_report_lines = fields.Boolean(
        compute="_compute_has_show_price_report_lines",
    )

    def _compute_has_show_price_report_lines(self):
        for sel in self:
            sel.has_show_price_report_lines = any(
                line.show_price_info_report for line in sel.invoice_line_ids
            )

    def action_activate_show_price_info_report(self):
        self.mapped("invoice_line_ids").filtered(
            lambda a: not a.show_price_info_report
        ).write({"show_price_info_report": True})

    def action_deactivate_show_price_info_report(self):
        self.mapped("invoice_line_ids").filtered(
            lambda a: a.show_price_info_report
        ).write({"show_price_info_report": False})
