class GameController:
    screen = None
    mobs_group = None
    items_group = None
    static_group = None

    def __init__(self, screen, mobs_group, items_group, static_group):
        self.screen = screen
        self.mobs_group = mobs_group
        self.items_group = items_group
        self.static_group = static_group

    '''
        Static objects methods
    '''
    def add_static_object(self, static_object):
        self.static_group.add(static_object)

    def draw_static_objects(self):
        self.static_group.draw(self.screen)

    def remove_static_object(self, static_object):
        self.static_group.remove(static_object)

    '''
        Mobs methods
    '''
    def add_mob(self, mob_object):
        self.mobs_group.add(mob_object)

    def draw_mobs(self):
        self.mobs_group.draw(self.screen)

    def remove_mob(self, mob_object):
        self.mobs_group.remove(mob_object)

    def update_mobs(self):
        self.mobs_group.update()
    '''
        Items methods
    '''
    def add_item(self, item_object):
        self.items_group.add(item_object)

    def draw_items(self):
        self.items_group.draw(self.screen)

    def remove_item(self, item_object):
        self.items_group.remove(item_object)
