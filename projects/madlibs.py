# A word game where you create a story by filling in the blanks with different types of words (nouns, verbs, adjectives, etc.). The program will prompt the user for these words and then display the completed story.

import time

def play_mad_libs():
    print("=========================================")
    print("      ✨ ISEKAI'D! ✨     ")
    print("=========================================\n")
    print("Welcome, Hero! Fill in the blanks to create your ultimate anime scene.\n")

    # Collecting user inputs
    protagonist_name = input("1. Protagonist's Name: ")
    hair_color = input("2. An unrealistically bright hair color: ")
    mundane_object = input("3. A mundane everyday object: ")
    magical_noun = input("4. A cool sounding noun (e.g., Shadow, Nebula, Destiny): ")
    anime_trope_food = input("5. A food you'd eat while running late to school: ")
    villain_name = input("6. Villain's Name: ")
    attack_adjective = input("7. Epic sounding adjective: ")
    element = input("8. An element (e.g., Fire, Void, Lightning): ")
    animal = input("9. An animal (plural): ")
    signature_move = input("10. A ridiculous sounding attack name: ")
    
    print("\n--- Generating your anime episode... Please wait... ---")
    time.sleep(1.5)
    print("\n=========================================\n")

    # The Story Story
    story = f"""
    The day started like any other for {protagonist_name}. They were sitting in the back row of the 
    classroom, right next to the window, staring blankly at the sky with their vibrant {hair_color} hair 
    flowing in the breeze. Suddenly, the school roof blew open! 
    
    A massive portal appeared, and out stepped the dreaded Demon Lord, {villain_name}! 
    
    "At last, I have found the chosen one!" {villain_name} cackled, pointing a dark finger at {protagonist_name}. 
    "Hand over the legendary {mundane_object} of {magical_noun}, or face my wrath!"
    
    {protagonist_name} stood up calmly, finished chewing their half-eaten {anime_trope_food}, and smirked. 
    "Heh. You're 10,000 years too early to challenge me."
    
    Channeling the ancient power of the {attack_adjective} {element}, {protagonist_name}'s eyes began to glow. 
    The aura around them was so intense that it looked like a stampede of angry, glowing {animal}.
    
    "Take this! Ultimate Secret Technique..." {protagonist_name} screamed at the top of their lungs, 
    "SUPER ULTRA {signature_move.upper()} BLAST!!!"
    
    With a blinding flash of light, the Demon Lord was defeated, crying out in defeat as they faded into 
    glitter. {protagonist_name} pushed up their glasses, which caught the light perfectly. 
    "Yare yare daze," they whispered. Another day saved.
    """

    print(story)
    print("=========================================")
    print("             TO BE CONTINUED...          ")
    print("=========================================")

# Run the game
if __name__ == "__main__":
    play_mad_libs()