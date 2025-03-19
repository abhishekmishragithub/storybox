import random

def add_emoji_to_title(title: str):
    emojis = ["📚", "🌟", "🌈", "🎭", "🔮", "🦄", "🏰", "🌺", "🌙", "⭐"]
    return f"{random.choice(emojis)} {title} {random.choice(emojis)}"