from enum import Enum

class Constants(Enum):

    # Team Constants
    Hostile = "Hostile"
    Passive = "Passive"
    Friendly = "Friendly"
    All = "All"
    
    # Effect Constants
    Buffs = "Buffs"
    Nerfs = "Nerfs"
    Null = "Null"

    # Rarity Constants
    Common = "Common"
    Rare = "Rare"
    Epic = "Epic"
    Legendary = "Legendary"

    # Upgrade Constants
    Additive = "Additive"
    Multiplicative = "Multiplicative"
    ArithmeticUpgrade = "ArithmeticUpgrade"