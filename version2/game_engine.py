import copy
import json
from pathlib import Path

CONFIG = json.loads((Path(__file__).parent / "game_config.json").read_text(encoding="utf-8"))

def new_game():
    """Create a fresh game state."""
    return {
        "objects": copy.deepcopy(CONFIG["objects"]),  
        "inventory": [],                              
        "solved": [],                                  
        "escaped": False,
    }

def visible_objects(state):
    """Objects the player has discovered and not picked up."""
    return [name for name, obj in state["objects"].items()
            if not obj.get("hidden") and name not in state["inventory"]]

def can_reach(state, name):
    """The player can only interact with things they can see or are carrying."""
    return name in visible_objects(state) or name in state["inventory"]

def reveal(state, name):
    """Make a hidden object visible."""
    if name:
        state["objects"][name]["hidden"] = False

def do_action(state, action, target=None, item=None, code=None):
    """Check one player action and update the state ONLY if it is allowed.

    Returns a short FACT sentence that Gemini will turn into a nice description.
    """
    objects = state["objects"]

    if action == "look":
        return "You look around. You can see: " + ", ".join(visible_objects(state)) + "."

    if action == "inventory":
        return "You are carrying: " + (", ".join(state["inventory"]) or "nothing") + "."

    if action == "examine":
        if not target or not can_reach(state, target):
            return f"There is no '{target}' here."
        obj = objects[target]
        fact = obj["description"]
        if "locked" in obj:
            fact += " It is locked." if obj["locked"] else " It is unlocked."
        if obj.get("message_visible"):
            fact += f" Glowing words on it say: '{obj['secret_text']}'"
        reveal(state, obj.get("reveals"))
        return fact

    if action == "take":
        if not target or not can_reach(state, target):
            return f"There is no '{target}' here."
        if target in state["inventory"]:
            return f"You already have the {target}."
        if not objects[target].get("can_take"):
            return f"You cannot take the {target}."
        state["inventory"].append(target)
        return f"You take the {target}."
    
    if action == "enter_code":
        if not target or not can_reach(state, target) or "code" not in objects[target]:
            return "There is no lock with a code like that here."
        obj = objects[target]
        if not obj["locked"]:
            return f"The {target} is already unlocked."
        if code != obj["code"]:
            return f"You enter {code}. Wrong code - the {target} stays locked."
        obj["locked"] = False
        state["solved"].append(target)
        if target == "door":
            state["escaped"] = True
            return "The code is correct! The door swings open. You escaped!"
        reveal(state, obj.get("contains"))
        return f"The code is correct! The {target} opens. Inside you find: {obj['contains']}."
    
    if action == "use":
        if not item or item not in state["inventory"]:
            return f"You do not have a '{item}'."
        if not target or not can_reach(state, target):
            return f"There is no '{target}' here."
        obj = objects[target]
        if obj.get("key") == item and obj["locked"]:
            obj["locked"] = False
            state["solved"].append(target)
            reveal(state, obj.get("contains"))
            return f"The {item} fits! The {target} opens. Inside you find: {obj['contains']}."
        if obj.get("read_with") == item and not obj.get("message_visible"):
            obj["message_visible"] = True
            state["solved"].append(target)
            return f"You use the {item} on the {target}. Glowing words appear: '{obj['secret_text']}'"
        return f"You use the {item} on the {target}, but nothing new happens."

    if action == "open":
        if not target or not can_reach(state, target):
            return f"There is no '{target}' here."
        if objects[target].get("locked"):
            return f"The {target} is locked."
        return f"The {target} is already open."

    return "Nothing in the room changes. Only real actions inside the room can help you escape."