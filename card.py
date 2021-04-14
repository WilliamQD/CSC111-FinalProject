import pygame
from typing import Optional, Any

size = (640, 480)  # 设置窗口
screen = pygame.display.set_mode(size)  # 显示窗口

width, height = screen.get_size()  # 获取屏幕大小
square_size = (width / 12, height / 9)  # 获取单个方块大小

# 加载图片
image_miniguner = pygame.image.load("Resources/Tachaka.jpg")  # 机枪兵图片（机枪哥）
image_charger = pygame.image.load("Resources/Ash.jpg")  # 冲锋枪兵图片（ash）
image_sniper = pygame.image.load("Resources/Andreana.jpg")  # 狙击兵图片
image_rocketer = pygame.image.load("Resources/W.jpg")  # 火箭兵图片（W）
image_doctor = pygame.image.load("Resources/Folinic.jpg")  # 医疗兵图片
image_ninja = pygame.image.load("Resources/Snow.jpg")  # 忍者图片（白雪）
image_fireball = pygame.image.load("Resources/fireball.png")  # 艾雅法拉二技能图标
image_lightening = pygame.image.load("Resources/lightening.png")  # 雷蛇二技能图标
image_mine = pygame.image.load("Resources/mine.png")  # 梅尔一技能图标
image_autogun = pygame.image.load("Resources/autogun.png")  # 机枪哥二技能图标

# 干员图片大小转换
image_miniguner_card = pygame.transform.scale(image_miniguner, (int(square_size[0] * 1.5),
                                                                int(square_size[1] * 1.5)))
image_charger_card = pygame.transform.scale(image_charger, (int(square_size[0] * 1.5),
                                                            int(square_size[1] * 1.5)))
image_sniper_card = pygame.transform.scale(image_sniper, (int(square_size[0] * 1.5),
                                                          int(square_size[1] * 1.5)))
image_rocketer_card = pygame.transform.scale(image_rocketer, (int(square_size[0] * 1.5),
                                                              int(square_size[1] * 1.5)))
image_doctor_card = pygame.transform.scale(image_doctor, (int(square_size[0] * 1.5),
                                                          int(square_size[1] * 1.5)))
image_ninja_card = pygame.transform.scale(image_ninja, (int(square_size[0] * 1.5),
                                                        int(square_size[1] * 1.5)))
image_fireball_card = pygame.transform.scale(image_fireball, (int(square_size[0] * 1.5),
                                                              int(square_size[1] * 1.5)))
image_lightening_card = pygame.transform.scale(image_lightening, (int(square_size[0] * 1.5),
                                                                  int(square_size[1] * 1.5)))
image_mine_card = pygame.transform.scale(image_mine, (int(square_size[0] * 1.5),
                                                      int(square_size[1] * 1.5)))
image_autogun_card = pygame.transform.scale(image_autogun, (int(square_size[0] * 1.5),
                                                            int(square_size[1] * 1.5)))

image_miniguner_square = pygame.transform.scale(image_miniguner, (int(square_size[0] * 0.8),
                                                                  int(square_size[1] * 0.8)))
image_charger_square = pygame.transform.scale(image_charger, (int(square_size[0] * 0.8),
                                                              int(square_size[1] * 0.8)))
image_sniper_square = pygame.transform.scale(image_sniper, (int(square_size[0] * 0.8),
                                                            int(square_size[1] * 0.8)))
image_rocketer_square = pygame.transform.scale(image_rocketer, (int(square_size[0] * 0.8),
                                                                int(square_size[1] * 0.8)))
image_doctor_square = pygame.transform.scale(image_doctor, (int(square_size[0] * 0.8),
                                                            int(square_size[1] * 0.8)))
image_ninja_square = pygame.transform.scale(image_ninja, (int(square_size[0] * 0.8),
                                                          int(square_size[1] * 0.8)))
image_fireball_square = pygame.transform.scale(image_fireball, (int(square_size[0] * 0.8),
                                                                int(square_size[1] * 0.8)))
image_lightening_square = pygame.transform.scale(image_lightening, (int(square_size[0] * 0.8),
                                                                    int(square_size[1] * 0.8)))
image_mine_square = pygame.transform.scale(image_mine, (int(square_size[0] * 0.8),
                                                        int(square_size[1] * 0.8)))
image_autogun_square = pygame.transform.scale(image_autogun, (int(square_size[0] * 0.8),
                                                              int(square_size[1] * 0.8)))


class card:
    """The attribute class of card.

    Instance Attributes:
        - images: The images for a card on visualization
        - display_mode: A int representing which image will display on the screen
        (Ex. attack image, defend image)
        - buffs: A dictionary collects string as key, and its respond value can be float and bool.
        Each key in this dictionary represents one kind of buff.
        - location: A tuple represents location of the card on the map
        - direction: A string represents that the way of a card
        that how it move in the game (move toward left or right)

    Preconditions:
        - images != []
        - 0 <= display_mode <=2
        - 1 <= location[0] <= 10
        - 1 <= location[1] <= 6
        - direction in {'left', 'right'}
    """
    images: list[pygame.image]
    display_mode: int
    buffs: dict[str, Any]
    location: Optional[tuple]  # This is a location based on screen divided by square, which is 9*12
    direction: str

    def __init__(self, images: list[pygame.image], location: Optional[tuple], direction: str = ''):
        """initialize the function
        """
        self.images = images
        self.display_mode = 0
        self.buffs = {'attack buff': 1.0, 'defend buff': 1.0, 'mobility': True, 'burn': False}
        self.direction = direction
        self.location = location

    def display_mode_refresh(self, new_mode: int):
        """Change the display mode by input.
        0 is original size and should not appear.
        1 is card size which is used below the mpa to represent a card.
        2 is square size which is used in the map to represent a visual soldier.
        """
        self.display_mode = new_mode

    def display(self) -> pygame.image:
        """Return the picture of the display mode.
        """
        return self.images[self.display_mode]

    def get_real_location(self) -> Optional[tuple]:
        """Return the location data on map and refresh the display mode by data.
        Also refresh display mode.
        """
        if self.location is None:
            return None
        else:
            real_location = (int(self.location[0] * square_size[0]),
                             int(self.location[1] * square_size[1]))
            if square_size[0] < real_location[0] < square_size[0] * 10 \
                    and square_size[1] <= real_location[1] <= square_size[1] * 7:
                self.display_mode = 2
            elif square_size[1] * 7 < real_location[1]:
                self.display_mode = 1
            return (real_location[0] - 1, real_location[1] - 1)


class miniguner(card):
    """The class of miniguner.
    """
    max_hp: int
    hp: int
    attack: int
    weight: int
    value: int
    type: str
    attack_system: str
    defend_system: str
    special: Any
    range: int

    def __init__(self, location: Optional[tuple], direction: str = ''):
        """initialize the function.
        """
        super().__init__([image_miniguner, image_miniguner_card, image_miniguner_square],
                         location, direction)
        self.max_hp = 20
        self.hp = 20
        self.attack = 5
        self.weight = ...
        self.value = 5
        self.location = location
        self.type = 'soldier'
        self.attack_system = 'light'
        self.defend_system = 'heavy'
        self.special = None
        self.range = 1

    def attack(self, target: Any) -> None:
        """Attacking the given target.
        The given target should be subclass of card.
        """
        mult_pow = self.buffs['attack buff'] * target.buffs['defend buff']
        if target.defend_system == self.attack_system:  # 轻打轻
            mult_pow = mult_pow * 1.5

        target.hp = int(target.hp - self.attack * mult_pow)


class charger(card):
    """The class of charger.
    """
    max_hp: int
    hp: int
    attack: int
    weight: int
    value: int
    type: str
    attack_system: str
    defend_system: str
    special: Any
    range: int

    def __init__(self, location: Optional[tuple], direction: str = ''):
        """initialize the function.
        """
        super().__init__([image_charger, image_charger_card, image_charger_square],
                         location, direction)
        self.max_hp = 10
        self.hp = 10
        self.attack = 15
        self.weight = ...
        self.value = 5
        self.type = 'soldier'
        self.attack_system = 'light'
        self.defend_system = 'light'
        self.special = None
        self.range = 1

    def attack(self, target: Any) -> None:
        """Attacking the given target.
        The given target should be subclass of card.
        """
        mult_pow = self.buffs['attack buff'] * target.buffs['defend buff']
        if target.defend_system == self.attack_system:  # 轻打轻
            mult_pow = mult_pow * 1.5

        target.hp = int(target.hp - self.attack * mult_pow)


class sniper(card):
    """The class of sniper.
    """
    max_hp: int
    hp: int
    attack: int
    weight: int
    value: int
    type: str
    attack_system: str
    defend_system: str
    special: Any
    range: int

    def __init__(self, location: Optional[tuple], direction: str = ''):
        """initialize the function.
        """
        super().__init__([image_sniper, image_sniper_card, image_sniper_square],
                         location, direction)
        self.max_hp = 5
        self.hp = 5
        self.attack = 20
        self.weight = ...
        self.value = 7
        self.type = 'soldier'
        self.attack_system = 'heavy'
        self.defend_system = 'light'
        self.special = None
        self.range = 2

    def attack(self, target: Any) -> None:
        """Attacking the given target.
        The given target should be subclass of card.
        """
        mult_pow = self.buffs['attack buff'] * target.buffs['defend buff']
        if target.defend_system == self.attack_system:  # 重打重
            mult_pow = mult_pow * 1.5
        else:  # 重打轻
            mult_pow = mult_pow * 0.8

        target.hp = int(target.hp - self.attack * mult_pow)


class rocketer(card):
    """The class of rocketer.
    """
    max_hp: int
    hp: int
    attack: int
    weight: int
    value: int
    type: str
    attack_system: str
    defend_system: str
    special: Any
    range: int

    def __init__(self, location: Optional[tuple], direction: str = ''):
        """initialize the function.
        """
        super().__init__([image_rocketer, image_rocketer_card, image_rocketer_square],
                         location, direction)
        self.max_hp = 10
        self.hp = 10
        self.attack = 15
        self.weight = ...
        self.value = 5
        self.type = 'soldier'
        self.attack_system = 'heavy'
        self.defend_system = 'heavy'
        self.special = None
        self.range = 2

    def attack(self, target: Any) -> None:
        """Attacking the given target.
        The given target should be subclass of card.
        """
        mult_pow = self.buffs['attack buff'] * target.buffs['defend buff']
        if target.defend_system == self.attack_system:  # 重打重
            mult_pow = mult_pow * 1.5
        else:  # 重打轻
            mult_pow = mult_pow * 0.8

        target.hp = int(target.hp - self.attack * mult_pow)


class doctor(card):
    """The class of doctor.
    """
    max_hp: int
    hp: int
    attack: int
    weight: int
    value: int
    type: str
    attack_system: Optional[str]  # 医生设定不会攻击
    defend_system: str
    special: Any
    range: int

    def __init__(self, location: Optional[tuple], direction: str = ''):
        """initialize the function.
        """
        super().__init__([image_doctor, image_doctor_card, image_doctor_square],
                         location, direction)
        self.max_hp = 10
        self.hp = 10
        self.attack = 8
        self.weight = ...
        self.value = 5
        self.type = 'soldier'
        self.attack_system = None
        self.defend_system = 'light'
        self.special = None
        self.range = 1  # 以医生为半径画圆，别的都是直线

    def attack(self, target: Any) -> None:
        """Attacking the given target.
        The given target should be subclass of card.

        NOTE: doctor's attack is not affected by any buff!!!
        """
        if target.hp + self.attack > target.max_hp:
            target.hp = target.max_hp
        else:
            target.hp += self.attack


class ninja(card):
    """The class of ninja.
    """
    max_hp: int
    hp: int
    attack: int
    weight: int
    value: int
    type: str
    attack_system: str
    defend_system: str
    special: Any
    range: int

    def __init__(self, location: Optional[tuple], direction: str = ''):
        """initialize the function.
        """
        super().__init__([image_ninja, image_ninja_card, image_ninja_square, location],
                         location, direction)
        self.max_hp = 10
        self.hp = 10
        self.attack = 10
        self.weight = ...
        self.value = 7
        self.type = 'soldier'
        self.attack_system = 'light'
        self.defend_system = 'light'
        self.special = None
        self.range = 1
        self.buffs['first attack'] = True

    def attack(self, target: Any) -> None:
        """Attacking the given target.
        The given target should be subclass of card.
        """
        mult_pow = self.buffs['attack buff'] * target.buffs['defend buff']
        if target.defend_system == self.attack_system:  # 轻打轻
            mult_pow = mult_pow * 1.5

        if self.buffs['first attack'] is True:  # Check whether it is first attack (only for ninja)
            mult_pow = mult_pow * 2
            self.buffs['first attack'] = False

        target.hp = int(target.hp - self.attack * mult_pow)


class fireball(card):
    """The class of fire ball.
    """
    attack: int
    weight: int
    value: int
    type: str

    def __init__(self, location: Optional[tuple], direction: str = ''):
        """initialize the function.
        """
        super().__init__([image_fireball, image_fireball_card, image_fireball_square],
                         location, direction)
        self.attack = 10
        self.weight = ...
        self.value = 10
        self.type = 'magic'


class lightening(card):
    """The class of lightening.
    """
    attack: int
    weight: int
    value: int
    type: str

    def __init__(self, location: Optional[tuple], direction: str = ''):
        """initialize the function.
        """
        super().__init__([image_lightening, image_lightening_card, image_lightening_square],
                         location, direction)
        self.attack = 20
        self.weight = ...
        self.value = 10
        self.type = 'magic'


class mine(card):
    """The class of mine.
    """
    max_hp: int
    hp: int
    attack: int
    weight: int
    value: int
    type: str

    def __init__(self, location: Optional[tuple], direction: str = ''):
        """initialize the function.
        """
        super().__init__([image_mine, image_mine_card, image_mine_square],
                         location, direction)
        self.max_hp = 10
        self.hp = 10
        self.attack = 5
        self.weight = ...
        self.value = 10
        self.type = 'building'


class autogun(card):
    """The class of autogun.
    """
    max_hp: int
    hp: int
    attack: int
    weight: int
    value: int
    type: str
    attack_system: str
    defend_system: str

    def __init__(self, location: Optional[tuple], direction: str = ''):
        """initialize the function.
        """
        super().__init__([image_autogun, image_autogun_card, image_autogun_square],
                         location, direction)
        self.max_hp = 20
        self.hp = 20
        self.attack = 5
        self.weight = ...
        self.value = 10
        self.type = 'building'
        self.attack_system = 'heavy'
        self.defend_system = 'heavy'

    def attack(self, target: Any) -> None:
        """Attacking the given target.
        The given target should be subclass of card.
        """
        mult_pow = self.buffs['attack buff'] * target.buffs['defend buff']
        if target.defend_system == self.attack_system:  # 重打重
            mult_pow = mult_pow * 1.5
        else:  # 重打轻
            mult_pow = mult_pow * 0.8

        target.hp = int(target.hp - self.attack * mult_pow)
