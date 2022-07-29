from django.contrib import admin

from accounting.models import (Account, Asset, Bank, BankAccount, Cheque, FinancialBalance, FinancialDocument, FinancialDocumentTag, 
                               Invoice, InvoiceLine, Payment, Price, Product, ProductOrServiceCategory, Salary, Service,
                               Transaction, TransactionCategory)

# Register your models here.
admin.site.register(Asset)
admin.site.register(Account)
admin.site.register(Cheque)
admin.site.register(FinancialDocumentTag)
admin.site.register(FinancialDocument)
admin.site.register(FinancialBalance)
admin.site.register(Invoice)
admin.site.register(InvoiceLine)
admin.site.register(Price)
admin.site.register(Payment)
admin.site.register(Product)
admin.site.register(ProductOrServiceCategory)
admin.site.register(Service)
admin.site.register(Salary)
admin.site.register(TransactionCategory)
admin.site.register(BankAccount)
admin.site.register(Bank)
admin.site.register(Transaction)