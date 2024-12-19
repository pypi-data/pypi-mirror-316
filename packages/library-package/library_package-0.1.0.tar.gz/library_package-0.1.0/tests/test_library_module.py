from library_package import Fruit

def test_isInList_when_fruit_in_list():
    fruit = Fruit("elma")
    fruit1 = Fruit("kivi")
    assert fruit.isInList() == True
    assert fruit1.isInList() == False