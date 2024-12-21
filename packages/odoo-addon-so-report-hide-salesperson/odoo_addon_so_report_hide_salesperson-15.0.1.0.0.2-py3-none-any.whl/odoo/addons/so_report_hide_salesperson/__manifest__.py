# Copyright 2023 Angel Garcia de la Chica Herrera <angel.garcia@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "SO Report Hide Salesperson",
    "summary": "Hides the salesperson in the sales reports",
    "version": "15.0.1.0.0",
    "category": "Sales",
    "website": "https://github.com/sygel-technology/sy-sale-reporting",
    "author": "Sygel, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["sale"],
    "data": ["reports/sale_report_templates.xml"],
}
