


class Shared:
    jump_power_init = 2
    jump_power = jump_power_init
    jump_power_max = 10
    speed = 5
    
    def __init__(self):
        self.starting_loc = (0, 0)
    def jump_power_add(self, value):
        Shared.jump_power += value
        if Shared.jump_power > Shared.jump_power_max:
            Shared.jump_power = Shared.jump_power_max
    def reset(self):
        Shared.jump_power = Shared.jump_power_init


