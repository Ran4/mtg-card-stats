#!/usr/bin/env python3
from typing import List
from collections import Counter
import random
import re
import sys

def print_random_hand(deck: List[str]) -> None:
    random.shuffle(deck)
    for i, card_name in enumerate(deck[:18]):
        if i < 7:
            turn_name = f" H:"
        else:
            turn_name = f"T{i-7+1}:"
        print(f"{turn_name} {card_name}")

def _update_section(current_section: str, line: str) -> str:
    for section_name in ["Creatures", "Planeswalkers", "Instants",
            "Sorceries", "Enchantments", "Artifacts", "Equipment", "Lands"]:
        if section_name.lower() + ":" == line.lower():
            return section_name
    return current_section
    
def _looks_like_comment(s: str) -> bool:
    return s.strip().startswith("#")

def print_numbers(filename: str) -> None:
    """
    Prints statistics of a magic card decklist, which must be formatted like:
    
Creatures:
    4x Lighting Stormkin RU
        Flying, Haste
        2/2
        
Planeswalkers:

Instants:
    2x Hypothesizzle 3UR
        Draw two cards. You may discard a card to deal 4 dmg to target creature
    3x Ral's Outburst 2UR
        Deal 3 dmg to any target. Draw two cards, discard one
        
Sorceries:
    3x Lava Coil 1R
        Deal 4 dmg to target creature. If that creature would die, exile it instead.


Enchantments:
    4x Quicksilver Dagger 1UR
        Enchanted creature has "{T}: This creature deals 1 dmg to target player.
    # 2x Magefire Wings UR
    #     Enchanted creature gets +2/+0 and has flying

Artifacts:
Equipment:
Lands:
    10x Plains
    10x Island
    # 4x Scrylands
    """
    section: str = "other"
    counter: Counter = Counter()
    deck: List[str] = []
    
    with open(filename) as f:
        lines = [x.strip() for x in f.read().split("\n")]
    lines = [x for x in lines if x and not _looks_like_comment(x)]
        
    for stripped_line in lines:
        old_section = section
        section = _update_section(section, stripped_line)
        if section != old_section:
            print(section)
            continue
        
        matches = re.match("(\d+)x(.+)", stripped_line)
        if matches:
            amount: int = int(matches.groups()[0].strip())
            card_name: str = matches.groups()[1].strip()
            print(f"\t{amount}x {card_name}")
            counter[section] += amount
            [deck.append(card_name) for _ in range(amount)]
        else:
            pass
            #~ print(stripped_line)
            
    print("---")
    total_count = sum(counter.values())
    
    more_cards_needed_string = f" ({60-total_count} more cards to get to 60)" \
                               if total_count < 60 else ""
    print(f"{total_count} cards{more_cards_needed_string}")
    
    for section_name, count in counter.items():
        percent = 100 * count / total_count
        print(f"\t{count} {section_name} ({percent:.0f}%)")
        
    print_random_hand(deck)
        
            
if __name__ == "__main__":
    try:
        filename = sys.argv[1]
    except IndexError:
        filename = "standard_ru_copy_spell.mtg"
    print_numbers(filename)
