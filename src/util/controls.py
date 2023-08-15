import pygame

# controls USED to support wasd, but some of these
# buttons are being reserved for abilities
# namely w, a, s: ability 1...5 -> {q,w,e,a,s}

# we are still utilizing lists because some (confirmation)
# will have multiple options

UP_CONTROL = [pygame.K_UP]
DOWN_CONTROL = [pygame.K_DOWN]
RIGHT_CONTROL = [pygame.K_RIGHT]
LEFT_CONTROL = [pygame.K_LEFT]

INTERACT_CONTROL = [pygame.K_z]

ABILITY_1_CONTROL = [pygame.K_q]
ABILITY_2_CONTROL = [pygame.K_w]
ABILITY_3_CONTROL = [pygame.K_e]
ABILITY_4_CONTROL = [pygame.K_a]
ABILITY_5_CONTROL = [pygame.K_s]

CONFIRMATION_CONTROL = [pygame.K_SPACE, pygame.K_KP_ENTER]

TEST_DAMAGE_CONTROL = [pygame.K_f]

DEVTOOLS_CONTROL = [pygame.K_o]

def control_pressed(control_keys: list[int], keys: list[bool]) -> bool:
    for k in control_keys:
        if keys[k]:
            return True
    return False