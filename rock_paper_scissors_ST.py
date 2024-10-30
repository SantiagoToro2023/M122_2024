import random

print('''
|-----------------------------|
|     Rock, Paper Scissor     |
| Santiago Toro - 2024 - M122 |
|-----------------------------|
''')

WEAPONS = ['Rock', 'Paper', 'Scissor']

def user_win():
    print('System has chosen: ' + SYSTEM_WEAPON)
    print('You win!')

def user_lose():
    print('System has chosen: ' + SYSTEM_WEAPON)
    print('You lose!')

def user_tie():
    print('System has chosen: ' + SYSTEM_WEAPON)
    print('It\'s a tie!')

def determine_outcome(USER_WEAPON, SYSTEM_WEAPON):
    if USER_WEAPON == SYSTEM_WEAPON:
        user_tie()
    elif (USER_WEAPON == 'Rock' and SYSTEM_WEAPON == 'Scissor') or \
         (USER_WEAPON == 'Paper' and SYSTEM_WEAPON == 'Rock') or \
         (USER_WEAPON == 'Scissor' and SYSTEM_WEAPON == 'Paper'):
        user_win()
    else:
        user_lose()

# Main game loop
while True:
    USER_WEAPON = input('Choose your weapon! (Rock, Paper or Scissor): ').capitalize()
    SYSTEM_WEAPON = random.choice(WEAPONS)

    if USER_WEAPON in WEAPONS:
        determine_outcome(USER_WEAPON, SYSTEM_WEAPON)
    else:
        print('Invalid input you incompetent fool! Go back to first grade! You suck! 🤬🤬🤬🤬🤬')
        print('*ᵁⁿˡᵉˢˢ ʸᵒᵘʳ ˢᵃⁿᵗᶦᵃᵍᵒ ᵀᵒʳᵒ ʰᵉˢ ᵏᵉʷˡ 😎')
        break