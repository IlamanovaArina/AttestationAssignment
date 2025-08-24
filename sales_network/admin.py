from django.contrib import admin
from sales_network.models import NetworkNode, Product
from django.utils.html import format_html


@admin.action(description='Очистить задолженность перед поставщиком')
def clear_debt(modeladmin, request, queryset):
    queryset.update(debt=0)


@admin.register(NetworkNode)
class NetworkNodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'country', 'city', 'street', 'house_number', 'node_type', 'provider',
                    'debt', 'created_at', 'user',)
    list_filter = ('city',)
    actions = [clear_debt]

    def provider_link(self, obj):
        if obj.provider:
            url = f'/admin/your_app_networknode/{obj.provider.id}/change/'
            return format_html('<a href="{}">{}</a>', url, obj.provider.name)
        return '-'
    provider_link.short_description = 'Поставщик'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'model', 'release_date', 'node', 'user')
