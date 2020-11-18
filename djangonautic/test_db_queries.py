
from djangonautic.models import *

product = Product.objects.all().latest("id")
curr_vars = Variation.objects.all().filter(product=product)
first = curr_vars[0]
second = curr_vars[1]

first_vals = VariationValue.objects.all().filter(variation_name=first)
second_vals = VariationValue.objects.all().filter(variation_name=second)

combo = VariationCombination(sku="test_sku_5")
combo.save()
combo.variation_name.add(first)
combo.variation_name.add(second)


combo.variation_value.add(first_vals[0])
combo.variation_value.add(second_vals[1])

query = VariationCombination.objects.filter(sku=combo.sku)

second_query = query.filter(variation_value = first_vals[0])
third_query = second_query.filter(variation_value = second_vals[1])