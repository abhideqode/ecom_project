from django import template
from ..models import Product,Variations

register = template.Library()

@register.filter
def product_feature(var, feature):
    # import pdb;pdb.set_trace()
    variations = var.product_variations.all()
    return variations.values_list(feature, flat=True)

