from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from Projekti import models


# class AccountAdmin(UserAdmin):
#     list_display = ('email', 'name', 'lastname', 'age', 'gender')
#
#     filter_horizontal = ()
#     list_filter = ()
#     fieldsets = ()


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name',)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'category', 'quantity', 'is_available')


class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('product', 'invoice', 'quantity', 'price','total')


class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variations_category',  'is_active', 'gender')
    list_editable = ('is_active',)
    list_filter = ('product', 'variations_category', 'is_active', 'gender')


class ReviewRatingAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')


admin.site.register(models.UserProfile)
admin.site.register(models.Category,CategoryAdmin)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Invoice)
admin.site.register(models.InvoiceItem, InvoiceAdmin)
admin.site.register(models.Variation, VariationAdmin)
admin.site.register(models.ReviewRating,ReviewRatingAdmin)
