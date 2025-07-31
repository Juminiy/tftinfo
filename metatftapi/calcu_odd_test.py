from parse import calc_augmentodds


# Golden Finale
calc_augmentodds('?', '?', 'G')

# Golden Gala
calc_augmentodds('G', 'G', 'G')

# S1LVER P4RTY
calc_augmentodds('S', 'S', 'S')

# Prismatic Prelude
calc_augmentodds('P', '?', '?')

# Ascending Augments
calc_augmentodds('S', 'G', 'P')

# Prismatic Finale
calc_augmentodds('?', '?', 'P')

# Prismatic Party
calc_augmentodds('P', 'P', 'P')

# Golden Prelude
calc_augmentodds('G', '?', '?')

# deformation
calc_augmentodds('P', 'S', '*')
calc_augmentodds('G', 'P', '?')
