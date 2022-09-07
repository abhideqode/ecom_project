"""
    this productcolor_tags.py file it is for template tags
"""
from django import template
# from ..models import Product, Variations

register = template.Library()


@register.filter
def product_feature(var, feature):
    """
        this function is for the template tag for vairations in  products
    """
    # import pdb;pdb.set_trace()
    variations = var.product_variations.all()
    return variations.values_list(feature, flat=True)
