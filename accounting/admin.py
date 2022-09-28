from django.contrib import admin

from accounting.models import (Account, Asset, Bank, BankAccount, Category, Cheque, Cost, DoubleTransaction, FinancialBalance, FinancialDocument, FinancialDocumentTag, 
                               Invoice, InvoiceLine, Payment, Price, Product, ProductSpecification, Salary, Service,
                               Transaction, TransactionCategory)

# Register your models here.
admin.site.register(Asset)
admin.site.register(Account)
admin.site.register(DoubleTransaction)
admin.site.register(Category)
admin.site.register(Cost)
admin.site.register(Cheque)
admin.site.register(FinancialDocumentTag)
admin.site.register(FinancialDocument)
admin.site.register(FinancialBalance)
admin.site.register(Invoice)
admin.site.register(InvoiceLine)
admin.site.register(Price)
admin.site.register(Payment)
admin.site.register(Product)
admin.site.register(ProductSpecification)
admin.site.register(Service)
admin.site.register(Salary)
admin.site.register(TransactionCategory)
admin.site.register(BankAccount)
admin.site.register(Bank)
admin.site.register(Transaction)