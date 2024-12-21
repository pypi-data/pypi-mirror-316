# Copyright 2022 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Invoice Report Hide Price",
    "summary": "Show/Hide price info in invoice PDF",
    "version": "15.0.1.0.0",
    "category": "Invoicing",
    "website": "https://github.com/sygel-technology/sy-account-invoice-reporting",
    "author": "Sygel",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["account"],
    "data": [
        "views/account_move_views.xml",
        "report/report_invoice.xml",
    ],
}
