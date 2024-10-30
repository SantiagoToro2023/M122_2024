# Santiago Toro - M122 - 30.12.2024
# Rock, Paper, Scissors - Grundlagen Python
import random
print('''
|-----------------------------|
|     Rock, Paper Scissor     |
| Santiago Toro - 2024 - M122 |
|-----------------------------|
''')

while True:
    WEAPONS = ['Rock', 'Paper', 'Scissor']
    USER_WEAPON = input('Choose your weapon! (Rock, Paper or Scissor): ')
    SYSTEM_WEAPON = random.choice(WEAPONS)

    def user_win():
        print('System has chosen: ' + SYSTEM_WEAPON)
        print('You win!')
    def user_lose():
        print('System has chosen: ' + SYSTEM_WEAPON)
        print('You lose!')
    def user_tie():
        print('System has chosen: ' + SYSTEM_WEAPON)
        print('Its a tie!')

    if USER_WEAPON == 'Rock':
        if SYSTEM_WEAPON == 'Scissor':
            user_win()
        elif SYSTEM_WEAPON == 'Paper':
            user_lose()
        else:
            user_tie()

    elif USER_WEAPON == 'Paper':
        if SYSTEM_WEAPON == 'Rock':
            user_win()
        elif SYSTEM_WEAPON == 'Scissor':
            user_lose()
        else:
            user_tie()

    elif USER_WEAPON == 'Scissor':
        if SYSTEM_WEAPON == 'Paper':
            user_win()
        elif SYSTEM_WEAPON == 'Rock':
            user_lose()
        else:
            user_tie()

    else:
        print('Invalid input you incompetent fool! Go back to first grade! You suck! 🤬🤬🤬🤬🤬')
        print('*ᵁⁿˡᵉˢˢ ʸᵒᵘʳ ˢᵃⁿᵗᶦᵃᵍᵒ ᵀᵒʳᵒ ʰᵉˢ ᵏᵉʷˡ 😎')
        break