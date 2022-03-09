from .models import SubAccount,ColorEnum
from .enums import SubAccountEnum
def init_sub_accounts(*args, **kwargs):
    if 'delete_all' in kwargs and kwargs['delete_all']:
        SubAccount.objects.all().delete()
    if len(SubAccount.objects.all())>0:
        return
    
    ASSET=SubAccount(title=SubAccountEnum.ASSET,color=ColorEnum.DANGER)
    ASSET.save()

    COST=SubAccount(title=SubAccountEnum.COST,color=ColorEnum.DANGER)
    COST.save()
    
    TAX=SubAccount(title=SubAccountEnum.TAX,color=ColorEnum.DANGER)
    TAX.save()

    
    BUILDING=SubAccount(title=SubAccountEnum.BUILDING,parent=ASSET,color=ColorEnum.DANGER)
    BUILDING.save()

    ASSET.save()

    
    INVESTMENT=SubAccount(title=SubAccountEnum.INVESTMENT,color=ColorEnum.DANGER)
    INVESTMENT.save()

    
    FURNITURE=SubAccount(title=SubAccountEnum.FURNITURE,parent=ASSET,color=ColorEnum.DANGER)
    FURNITURE.save()
    
    