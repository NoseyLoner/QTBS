from enum import Enum

class Constants(Enum):

    def __str__(self) -> str:
        return self.value   

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

    # State Constants
    Start = "Start"
    End = "End"
    Shopping = "Shopping"

    # Event Constants
    Attacking = "Attacking"
    UnitDeath = "UnitDeath"
    Infliction = "Infliction"
    Trigger = "Trigger"
    Clearing = "Clearing"
    Healing = "Healing"
    Consumption = "Consumption"
    Blocked = "Blocked"