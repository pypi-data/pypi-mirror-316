# Copyright 2022 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "SO Report Hide Price Portal",
    "summary": "Show/Hide price info in sale portal view",
    "version": "15.0.1.0.0",
    "category": "Sales",
    "website": "https://github.com/sygel-technology/sy-sale-reporting",
    "author": "Sygel",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "sale",
        "so_report_hide_price",
    ],
    "data": [
        "views/sale_portal_templates.xml",
    ],
}
