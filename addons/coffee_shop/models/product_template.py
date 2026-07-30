from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    coffee_shop_item_type = fields.Selection(
        selection=[
            ("drink", "Drink"),
            ("food", "Food"),
            ("retail", "Retail"),
        ],
        string="Coffee Shop Item Type",
        help="Categorizes menu items for simple coffee shop reporting and filtering.",
    )
