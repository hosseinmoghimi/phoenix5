from django.contrib import admin

from accounting.models import (Account, FinancialBalance, FinancialDocument,
                               Invoice, InvoiceLine, Product, Service,
                               Transaction, TransactionCategory)

# Register your models here.
admin.site.register(Transaction)
admin.site.register(TransactionCategory)
admin.site.register(Account)
admin.site.register(FinancialDocument)
admin.site.register(FinancialBalance)
admin.site.register(InvoiceLine)
admin.site.register(Invoice)
admin.site.register(Service)
admin.site.register(Product)
