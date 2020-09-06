"""
coding:utf8
@Time : 2020/9/6 14:41
@Author : cjr
@File : 我是动物饲养员.py
"""
from abc import ABC, abstractmethod


class Animal(ABC):
    animal_type = None
    size = None
    character = None

    @abstractmethod
    def is_fierce(self):
        sizes = {'小': 1, '中等': 2, '大': 3}
        if self.animal_type == '食肉动物' and sizes[self.size] >= sizes['中等']:
            return True
        return False


class Cat(Animal):

    voice = '嗷呜嗷呜嗷呜'

    def __init__(self, name, animal_type, size, character):
        self.name = name
        self.animal_type = animal_type
        self.size = size
        self.character = character

    def is_pet(self):
        if self.is_fierce():
            return False
        return True

    def is_fierce(self):
        pass


class Dog(Animal):
    voice = '汪汪汪'

    def __init__(self, name, animal_type, size, character):
        self.name = name
        super().__init__(animal_type, size, character)

    def is_pet(self):
        if self.is_fierce():
            return False
        return True

    def is_fierce(self):
        pass


class Zoo(object):

    def __init__(self, name):
        self.name = name

    def add_animal(self, animal: Animal):
        if not hasattr(self, animal.__class__.__name__):
            setattr(self, animal.__class__.__name__, animal)


if __name__ == '__main__':
    # 实例化动物园
    z = Zoo('时间动物园')
    # 实例化一只猫，属性包括名字、类型、体型、性格
    cat1 = Cat('大花猫 1', '食肉', '小', '温顺')
    # 增加一只猫到动物园
    z.add_animal(cat1)
    # 动物园是否有猫这种动物
    have_cat = hasattr(z, 'Cat')
    print(have_cat)
