import random

# Create players
players = [
    {"name": "Affan", "hp": 100},
    {"name": "Kajai", "hp": 100},
    {"name": "Sami",  "hp": 100},
    {"name": "Jojo",  "hp": 100}
]

# Crown parts
crown_emojis = ["💎", "🔥", "🌟", "⚡", "👑", "🧠", "🛡️", "🦾", "🦿", "🎯"]

def generate_crown_art(name):
    row1 = "   " + ' '.join(random.choices(crown_emojis, k=3))
    row2 = "  " + ' '.join(random.choices(crown_emojis, k=5))
    row3 = " " + ' '.join(random.choices(crown_emojis, k=7))
    row4 = f"👑 {name.upper()} 👑"
    return f"{row1}\n{row2}\n{row3}\n{row4}"

print("⚔️ Let the battle begin!\n")

for round_num in range(1, 11):
    if not players:
        print("💀 Everyone is dead. Game over.")
        break

    print(f"\n🔥 Round {round_num} 🔥")

    target = random.choice(players)
    dmg = random.randint(1, 100)
    target["hp"] -= dmg

    print(f"💥 {target['name']} was hit for {dmg} damage!")

    if target["hp"] <= 0:
        print(f"☠️ {target['name']} has fucking died!")
        players.remove(target)
    else:
        print(f"❤️ {target['name']} has {target['hp']} HP left.")

# Declare winner
if players:
    winner = max(players, key=lambda p: p["hp"])
    print(f"\n🏆 The winner is {winner['name']} with {winner['hp']} HP remaining!\n")
    print(generate_crown_art(winner["name"]))
else:
    print("\n💣 No one survived. This is the end.")
