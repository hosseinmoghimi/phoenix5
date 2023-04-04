from mafia.models import Role,GameScenario
from mafia.enums import RoleSideEnum


def init_roles(*args, **kwargs):
    Role.objects.all().delete()


    role=Role()
    role.priority=1
    role.title="شهروند ساده"
    role.wake_up_turn=0
    role.side=RoleSideEnum.CITIZEN
    role.save()

    role=Role(title="پزشک")
    role.wake_up_turn=20
    role.priority=2
    role.side=RoleSideEnum.CITIZEN
    role.save()

    role=Role()
    role.priority=3
    role.wake_up_turn=21
    role.title="کارآگاه"
    role.side=RoleSideEnum.CITIZEN
    role.save()

    
    role=Role(title="تفنگ دار")
    role.wake_up_turn=40
    role.priority=4
    role.side=RoleSideEnum.CITIZEN
    role.save()


    
    role=Role()
    role.title="نگهبان"
    role.wake_up_turn=5
    role.priority=5
    role.side=RoleSideEnum.CITIZEN
    role.save()
    

    role=Role(title="تکاور")
    role.wake_up_turn=10
    role.priority=6
    role.side=RoleSideEnum.CITIZEN
    role.save()

    role=Role(title="روانشناس")
    role.wake_up_turn=99
    role.priority=7
    role.side=RoleSideEnum.CITIZEN
    role.save()


    role=Role(title="زره پوش")
    role.wake_up_turn=0
    role.priority=2
    role.side=RoleSideEnum.CITIZEN
    role.save()

    role=Role(title="خبرنگار")
    role.wake_up_turn=80
    role.priority=2
    role.side=RoleSideEnum.CITIZEN
    role.save()


    role=Role(title="تک تیر انداز")
    role.wake_up_turn=70
    role.priority=2
    role.side=RoleSideEnum.CITIZEN
    role.save()
    
    
    

    role=Role(title="بازپرس")
    role.wake_up_turn=50
    role.priority=2
    role.side=RoleSideEnum.CITIZEN
    role.save()
    
    

    role=Role(title="شکارچی")
    role.wake_up_turn=2
    role.priority=2
    role.side=RoleSideEnum.CITIZEN
    role.save()
    


    role=Role(title="رویین تن")
    role.priority=0
    role.side=RoleSideEnum.CITIZEN
    role.save()
    
 

    role=Role(title="حرفه ای")
    role.wake_up_turn=74
    role.priority=2
    role.side=RoleSideEnum.CITIZEN
    role.save()


    role=Role()
    role.title="کابوی"
    role.wake_up_turn=0
    role.priority=2
    role.side=RoleSideEnum.CITIZEN
    role.save()

    role=Role(title="ماسون")
    role.wake_up_turn=90
    role.priority=2
    role.side=RoleSideEnum.CITIZEN
    role.save()

    role=Role(title="تایلر")
    role.priority=2
    role.wake_up_turn=90
    role.side=RoleSideEnum.CITIZEN
    role.save()


    role=Role(title="نانوا")
    role.priority=2
    role.wake_up_turn=0
    role.side=RoleSideEnum.CITIZEN
    role.save()
    


    role=Role(title="کشیش")
    role.wake_up_turn=0
    role.priority=2
    role.side=RoleSideEnum.CITIZEN
    role.save()
    

    role=Role(title="گورکن")
    role.priority=2
    role.side=RoleSideEnum.CITIZEN
    role.save()
    

    role=Role(title="مسیح")
    role.priority=2
    role.side=RoleSideEnum.CITIZEN
    role.save()
    

    role=Role(title="فروشنده")
    role.wake_up_turn=0
    role.priority=2
    role.side=RoleSideEnum.CITIZEN
    role.save()
    
    role=Role(title="فدایی")
    role.wake_up_turn=0
    role.priority=2
    role.side=RoleSideEnum.CITIZEN
    role.save()

    role=Role(title="شهردار")
    role.wake_up_turn=0
    role.priority=2
    role.side=RoleSideEnum.CITIZEN
    role.save()

    role=Role(title="جان سخت")
    role.wake_up_turn=0
    role.priority=2
    role.side=RoleSideEnum.CITIZEN
    role.save()

    role=Role()
    role.priority=2
    role.wake_up_turn=0
    role.title="پدرخوانده"
    role.side=RoleSideEnum.MAFIA
    role.save()
    

    

    role=Role(title="مافیای ساده")
    role.priority=2
    role.wake_up_turn=0
    role.side=RoleSideEnum.MAFIA
    role.save()

    role=Role(title="دکتر لکتر")
    role.priority=2
    role.wake_up_turn=0
    role.side=RoleSideEnum.MAFIA
    role.save()

    role=Role(title="جاسوس")
    role.priority=2
    role.wake_up_turn=0
    role.side=RoleSideEnum.MAFIA
    role.save()

    role=Role(title="ناتاشا")
    role.priority=2
    role.wake_up_turn=0
    role.side=RoleSideEnum.MAFIA
    role.save()

    role=Role(title="معشوقه")
    role.priority=2
    role.wake_up_turn=0
    role.side=RoleSideEnum.MAFIA
    role.save()


    role=Role()
    role.title="تروریست"
    role.priority=2
    role.wake_up_turn=0
    role.side=RoleSideEnum.MAFIA
    role.save()

    role=Role()
    role.title="خراب کار"
    role.priority=2
    role.wake_up_turn=0
    role.side=RoleSideEnum.MAFIA
    role.save()

    role=Role()
    role.title="گروگان گیر"
    role.wake_up_turn=0
    role.priority=2
    role.side=RoleSideEnum.MAFIA
    role.save()
    
    role=Role()
    role.title="مذاکره کننده"
    role.priority=2
    role.wake_up_turn=0
    role.side=RoleSideEnum.MAFIA
    role.save()

    
    role=Role(title="شیاد")
    role.priority=2
    role.wake_up_turn=0
    role.side=RoleSideEnum.MAFIA
    role.save()
    


    role=Role()
    role.title="ناتو"
    role.wake_up_turn=0
    role.priority=2
    role.side=RoleSideEnum.MAFIA
    role.save()


    
    role=Role()
    role.title="جوکر"
    role.wake_up_turn=0
    role.priority=2
    role.side=RoleSideEnum.MAFIA
    role.save()




    role=Role()
    role.title="ساقی"
    role.wake_up_turn=0
    role.priority=2
    role.side=RoleSideEnum.INDEPENDENT
    role.save()

    role=Role()
    role.title="هزار چهره"
    role.wake_up_turn=0
    role.priority=2
    role.side=RoleSideEnum.INDEPENDENT
    role.save()




def init_scenarioes(*args, **kwargs):
    
    GameScenario.objects.all().delete()

    
    game_scenario=GameScenario()
    game_scenario.title="بازپرس"
    game_scenario.save()
    game_scenario.roles.add(Role.objects.get(title="شهروند ساده"))
    game_scenario.roles.add(Role.objects.get(title="شهروند ساده"))
    game_scenario.roles.add(Role.objects.get(title="کارآگاه"))
    game_scenario.roles.add(Role.objects.get(title="پزشک"))
    game_scenario.roles.add(Role.objects.get(title="بازپرس"))
    game_scenario.roles.add(Role.objects.get(title="شکارچی"))
    game_scenario.roles.add(Role.objects.get(title="رویین تن"))
    game_scenario.roles.add(Role.objects.get(title="ناتو"))
    game_scenario.roles.add(Role.objects.get(title="پدرخوانده"))
    game_scenario.roles.add(Role.objects.get(title="شیاد"))



    game_scenario=GameScenario()
    game_scenario.title="گروگان گیری"
    game_scenario.save()
    game_scenario.roles.add(Role.objects.get(title="شهروند ساده"))
    game_scenario.roles.add(Role.objects.get(title="شهروند ساده"))
    game_scenario.roles.add(Role.objects.get(title="پدرخوانده"))
    game_scenario.roles.add(Role.objects.get(title="کارآگاه"))
    game_scenario.roles.add(Role.objects.get(title="پزشک"))
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



