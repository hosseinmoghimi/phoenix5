from mafia.models import Role,GameScenario
from mafia.enums import RoleSideEnum


def init_scenarioes(*args, **kwargs):
    
    GameScenario.objects.all().delete()
    game_scenario=GameScenario()
    game_scenario.title="گروگان گیری"
    game_scenario.save()
    game_scenario.roles.add(Role.objects.get(title="پدرخوانده"))
    game_scenario.roles.add(Role.objects.get(title="کارآگاه"))
    game_scenario.roles.add(Role.objects.get(title="پزشک"))
    game_scenario.roles.add(Role.objects.get(title="شهروند ساده"))
    game_scenario.roles.add(Role.objects.get(title="نگهبان"))

    
    game_scenario=GameScenario()
    game_scenario.title="تفنگ دار"
    game_scenario.save()
    game_scenario.roles.add(Role.objects.get(title="پدرخوانده"))
    game_scenario.roles.add(Role.objects.get(title="کارآگاه"))
    game_scenario.roles.add(Role.objects.get(title="پزشک"))
    game_scenario.roles.add(Role.objects.get(title="شهروند ساده"))
    game_scenario.roles.add(Role.objects.get(title="تفنگ دار"))
    game_scenario.roles.add(Role.objects.get(title="خراب کار"))

    
    game_scenario=GameScenario()
    game_scenario.title="مذاکره"
    game_scenario.save()
    game_scenario.roles.add(Role.objects.get(title="پدرخوانده"))
    game_scenario.roles.add(Role.objects.get(title="کارآگاه"))
    game_scenario.roles.add(Role.objects.get(title="پزشک"))
    game_scenario.roles.add(Role.objects.get(title="شهروند ساده"))
    game_scenario.roles.add(Role.objects.get(title="خبرنگار"))
    game_scenario.roles.add(Role.objects.get(title="مذاکره کننده"))

    game_scenario=GameScenario()
    game_scenario.title="تایلر ماسون"
    game_scenario.save()
    game_scenario.roles.add(Role.objects.get(title="پدرخوانده"))
    game_scenario.roles.add(Role.objects.get(title="کارآگاه"))
    game_scenario.roles.add(Role.objects.get(title="پزشک"))
    game_scenario.roles.add(Role.objects.get(title="شهروند ساده"))
    game_scenario.roles.add(Role.objects.get(title="تفنگ دار"))
    game_scenario.roles.add(Role.objects.get(title="خراب کار"))


def init_roles(*args, **kwargs):
    Role.objects.all().delete()


    role=Role(title="تفنگ دار")
    role.side=RoleSideEnum.CITIZEN
    role.save()

    role=Role(title="پزشک")
    role.side=RoleSideEnum.CITIZEN
    role.save()

    role=Role(title="تک تیر انداز")
    role.side=RoleSideEnum.CITIZEN
    role.save()
    
    
    role=Role(title="تکاور")
    role.side=RoleSideEnum.CITIZEN
    role.save()

    role=Role(title="حرفه ای")
    role.side=RoleSideEnum.CITIZEN
    role.save()

    role=Role(title="خبرنگار")
    role.side=RoleSideEnum.CITIZEN
    role.save()

    
    role=Role(title="روانشناس")
    role.side=RoleSideEnum.CITIZEN
    role.save()

    
    role=Role(title="زره پوش")
    role.side=RoleSideEnum.CITIZEN
    role.save()

    role=Role()
    role.title="شهروند ساده"
    role.side=RoleSideEnum.CITIZEN
    role.save()

    role=Role()
    role.title="کارآگاه"
    role.side=RoleSideEnum.CITIZEN
    role.save()

    role=Role()
    role.title="کابوی"
    role.side=RoleSideEnum.CITIZEN
    role.save()

    role=Role()
    role.title="نگهبان"
    role.side=RoleSideEnum.CITIZEN
    role.save()
    
    role=Role()
    role.title="پدرخوانده"
    role.side=RoleSideEnum.MAFIA
    role.save()
    
    role=Role()
    role.title="تروریست"
    role.side=RoleSideEnum.MAFIA
    role.save()

    role=Role()
    role.title="خراب کار"
    role.side=RoleSideEnum.MAFIA
    role.save()

    role=Role()
    role.title="گروگان گیر"
    role.side=RoleSideEnum.MAFIA
    role.save()
    
    role=Role()
    role.title="مذاکره کننده"
    role.side=RoleSideEnum.MAFIA
    role.save()

    role=Role()
    role.title="ناتو"
    role.side=RoleSideEnum.MAFIA
    role.save()