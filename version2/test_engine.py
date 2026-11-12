"""test_engine.py - try the game rules of Version 2 without Gemini.
Run with: python version2/test_engine.py
"""
from game_engine import do_action, new_game

game = new_game()

print("--- Cheating ---")
print(do_action(game, "take", target="brass_key"))                 
print(do_action(game, "use", item="brass_key", target="painting"))  
print(do_action(game, "enter_code", target="door", code="1234"))    
print(do_action(game, "open", target="drawer"))                    
print(do_action(game, "cheat"))                                     

print("\n--- Playing normally ---")
print(do_action(game, "examine", target="bookshelf"))
print(do_action(game, "examine", target="red_books"))
print(do_action(game, "enter_code", target="drawer", code="257"))
print(do_action(game, "take", target="brass_key"))
print(do_action(game, "use", item="brass_key", target="painting"))
print(do_action(game, "take", target="uv_flashlight"))
print(do_action(game, "examine", target="desk"))
print(do_action(game, "use", item="uv_flashlight", target="paper"))
print(do_action(game, "examine", target="clock"))
print(do_action(game, "enter_code", target="door", code="0925"))

print("\nEscaped:", game["escaped"])