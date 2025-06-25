import streamlit as st
import random

# Page config
st.set_page_config(page_title="Campaign Idea Generator", layout="centered")

# Title and description
st.title("🎬 Campaign / Series Idea Generator")
st.write("Generate unique creative ideas for photo/video campaigns or personal projects.")

# Data lists
themes = [
    "Isolation & Discovery", "Urban Chaos", "Silent Conversations",
    "Digital vs Nature", "Forgotten Rituals", "Youth in Transition",
    "Colors of the City", "Dreams vs Reality", "Life in a Bag",
    "Portraits of Resilience", "Sound of Memory"
]

formats = [
    "Photo series", "Short documentary", "Reel series", "Vertical film campaign",
    "TikTok storytelling series", "Behind-the-scenes mini-doc", "Cinematic visual poem"
]

structures = [
    "1 visual per day for 7 days",
    "3-part series exploring different moods",
    "1-minute episodes with recurring characters",
    "Color-based transitions from shot to shot",
    "Narrated from real interviews",
    "Non-linear storytelling with flashbacks"
]

visual_styles = [
    "Monochrome with splashes of color", "Shot handheld with natural light",
    "Split-screen sequences", "Color gel lighting with wide lenses",
    "Soft-focus dream-like shots", "Minimalist with harsh shadows"
]

titles = [
    "Fragments", "Echoes", "Offline", "Frame by Frame", "In Passing",
    "Filtered", "Last Seen", "Everyday Divine", "The Long Weekend"
]

# Generate button
if st.button("🎲 Generate Campaign Idea"):
    title = random.choice(titles)
    theme = random.choice(themes)
    format_ = random.choice(formats)
    structure = random.choice(structures)
    style = random.choice(visual_styles)

    # Display result
    st.markdown(f"### 📸 Campaign Title: *{title}*")
    st.markdown(f"**🎯 Theme:** {theme}")
    st.markdown(f"**🎞️ Format:** {format_}")
    st.markdown(f"**📐 Structure:** {structure}")
    st.markdown(f"**🎨 Visual Style:** {style}")
else:
    st.info("Click the button above to generate your next campaign idea!")

