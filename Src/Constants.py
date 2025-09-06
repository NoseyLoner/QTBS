from enum import Enum

class Constants(Enum):

    # Team Constants
    Hostile = "Hostile"
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

    # Event Constants
    Attacking = "Attacking"
    UnitDeath = "UnitDeath"
    Infliction = "Infliction"
    Trigger = "Trigger"
    Clearing = "Clearing"
    Healing = "Healing"
    Consuming = "Consuming"