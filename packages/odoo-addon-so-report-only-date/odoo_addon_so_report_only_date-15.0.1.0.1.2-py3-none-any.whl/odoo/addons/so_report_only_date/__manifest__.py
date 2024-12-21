# Copyright 2023 Ángel García de la Chica <angel.garcia@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "SO Report Only Date",
    "summary": "Sale Report Only Date",
    "version": "15.0.1.0.1",
    "category": "Sales",
    "website": "https://github.com/sygel-technology/sy-sale-reporting",
    "author": "Sygel, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["sale"],
    "data": [
        "report/sale_report_templates.xml",
    ],
}
