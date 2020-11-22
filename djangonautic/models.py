from django.db import models




class Product(models.Model):
    productURL = models.URLField(max_length=1000, null=True)
    title = models.TextField(max_length=1000, null=True)
    thumbnail_image_url = models.URLField(max_length=1000, null=True)
    price = models.TextField(max_length=10, null=True)

    def __str__(self):
        return "title:" + self.title + "product URL: " + self.productURL


class ProductImage(models.Model):
    product = models.ForeignKey(Product, default=None, null=True ,on_delete=models.CASCADE)
    imageURL = models.URLField(max_length=1000, default=None)
    def __str__(self):
        return self.imageURL

class Variation(models.Model):
    product = models.ForeignKey(Product, default=None,null=True ,on_delete=models.CASCADE)
    variation_name = models.CharField(max_length=100, default=None, null=True)
    def __str__(self):
        return self.variation_name

class VariationValue(models.Model):
    product = models.ForeignKey(Product, default=None, null=True ,on_delete=models.CASCADE)
    variation_name = models.ForeignKey(Variation, default=None, null=True, on_delete=models.CASCADE)
    value = models.CharField(max_length=100, default=None)
    def __str__(self):
        return self.value


class VariationCombination(models.Model):
    product = models.ForeignKey(Product, default=None, null=True, on_delete=models.CASCADE)
    variation_name = models.ManyToManyField(Variation, default=None)
    variation_value = models.ManyToManyField(VariationValue, default=None)
    sku = models.CharField(max_length=100, default=None)
    price = models.CharField(max_length=50, default=None)
    def __str__(self):
        return self.sku

class VariationPictures(models.Model):
    '''Pictures linked to a variation value'''
    product = models.ForeignKey(Product, default=None, null=True, on_delete=models.CASCADE)
    variation_name = models.ForeignKey(Variation, default=None, null=True ,on_delete=models.CASCADE)
    value = models.ForeignKey(VariationValue, default=None, null=True ,on_delete=models.CASCADE)
    imageURL = models.URLField(max_length=1000, null=True)

class SessionID(models.Model):
    session_id = models.CharField(default=None, null=True, max_length=1000)

class Page(models.Model):
    title = models.CharField(max_length=220)
    title_description = models.TextField(blank=True, null=True)
    title_btn = models.CharField(max_length=50, null=True, blank=True, default='Join')
    title_btn_url = models.CharField(max_length=50, blank=True, null=True)
    content = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title