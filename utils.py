def detect_disaster(user_input):
    user_input = user_input.lower()

    if "earthquake" in user_input:
        return "Earthquake"
    elif "flood" in user_input:
        return "Flood"
    elif "fire" in user_input:
        return "Fire"
    elif "cyclone" in user_input:
        return "Cyclone"
    elif "heatwave" in user_input or "heat wave" in user_input:
        return "Heatwave"
    else:
        return None


def detect_intent(user_input):
    user_input = user_input.lower()

    if "plan" in user_input or "prepare" in user_input:
        return "plan"
    else:
        return "qa"