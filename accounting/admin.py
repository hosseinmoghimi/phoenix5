from django.contrib import admin

from accounting.models import (Account, Cheque, FinancialBalance, FinancialDocument, FinancialDocumentTag, SubAccount,
                               Invoice, InvoiceLine, Price, Product, Salary, Service,
                               Transaction, TransactionCategory)

# Register your models here.
admin.site.register(Account)
admin.site.register(Cheque)
admin.site.register(FinancialDocumentTag)
admin.site.register(FinancialDocument)
admin.site.register(FinancialBalance)
admin.site.register(Invoice)
admin.site.register(InvoiceLine)
admin.site.register(Price)
admin.site.register(Product)
admin.site.register(SubAccount)
admin.site.register(Service)
admin.site.register(Salary)
admin.site.register(TransactionCategory)
admin.site.register(Transaction)