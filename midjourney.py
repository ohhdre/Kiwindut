import streamlit as st
import random
import pandas as pd

# ---------- PROMPT SETUP ----------
category_options = {
    "Portrait Editorial": {
        "subjects": ["high-fashion model", "androgynous figure", "golden-age actor", "surreal face", "cultural icon"],
        "styles": ["Vogue 1960s", "hyperreal oil painting", "monochrome photojournalism", "Elizaveta Porodina style", "Rembrandt-style lighting"]
    },
    "Luxury Product Photography": {
        "subjects": ["designer perfume bottle", "artisanal watch", "high-end sneaker", "premium skincare", "concept tech device"],
        "styles": ["commercial studio lighting", "floating product render", "macro lens detail", "moody cinematic shot", "Apple-style ad"]
    },
    "High Fashion Campaign": {
        "subjects": ["avant-garde model pose", "couture garment movement", "runway drama", "translucent fabric in motion", "dramatic silhouette"],
        "styles": ["Hedi Slimane B/W", "Peter Lindbergh mood", "surreal Vogue cover", "Y2K gloss", "editorial glam"]
    },
    "Cinematic Urban Scene": {
        "subjects": ["lone figure in city rain", "subway mood shot", "rooftop in golden hour", "empty street at night", "glowing billboard alley"],
        "styles": ["Blade Runner aesthetic", "Netflix drama still", "teal & orange grade", "analog film look", "cyber-noir"]
    },
    "Nature and Conceptual Landscape": {
        "subjects": ["alien desert", "foggy mountain ridge", "surreal tree formations", "underwater forest", "glowing cave"],
        "styles": ["National Geographic realism", "dreamlike matte painting", "ethereal concept art", "pastel fog", "epic fantasy art"]
    },
    "Futuristic Sci-Fi Design": {
        "subjects": ["humanoid robot in ritual", "AI goddess", "chrome spaceship interior", "neon temple", "sci-fi soldier"],
        "styles": ["H.R. Giger-inspired", "Ghost in the Shell", "sleek 3D render", "dark cyberpunk", "Daft Punk mood"]
    },
    "Fantasy Character Concept": {
        "subjects": ["elven warrior", "steampunk wizard", "elemental mage", "post-apocalyptic priestess", "shadow assassin"],
        "styles": ["Magic: The Gathering illustration", "D&D cover art", "cinematic lighting", "concept sketch", "detailed 4K"]
    }
}

lightings = ["golden hour", "neon light", "soft studio lighting", "moonlight", "high contrast shadows"]
moods = ["mysterious", "serene", "epic", "dark", "dreamlike"]
colors = ["vibrant", "monochrome", "pastel", "earth-toned", "high saturation"]

# ---------- STREAMLIT PAGE ----------
st.set_page_config(page_title="MidJourney Prompt Generator", layout="wide")
st.title("🎨 MidJourney Prompt Generator Dashboard")

if "projects" not in st.session_state:
    st.session_state.projects = {}

# ---------- SIDEBAR INPUT ----------
with st.sidebar:
    st.header("⚙️ Prompt Settings")
    client_name = st.text_input("Client Name", value="Unnamed Client")
    mode = st.radio("Prompt Mode", ["Predefined Category", "Custom Prompt"])

    if mode == "Predefined Category":
        category = st.selectbox("Prompt Category", list(category_options.keys()))
    else:
        custom_prompt = st.text_area("✍️ Enter your custom base prompt")

    aspect_ratio = st.text_input("Aspect Ratio (--ar)", value="3:4")
    mj_style = st.text_input("MJ Style (--style)", value="raw")
    version = st.text_input("MidJourney Version (--v)", value="6")
    iw = st.text_input("Image Weight (--iw)", value="1.0")
    image_url = st.text_input("Optional Image URL (--image)", value="")
    sref = st.text_input("Optional Style Reference (--sref)", value="")
    generate_btn = st.button("🚀 Generate 10 Prompts")

# ---------- PROMPT GENERATOR ----------
def generate_prompts(client, use_custom, base_prompt, category, ar, mj_style, version, iw, image_url, sref):
    results = []

    for _ in range(10):
        if use_custom and base_prompt.strip():
            prompt = base_prompt.strip()
        else:
            subject = random.choice(category_options[category]["subjects"])
            style = random.choice(category_options[category]["styles"])
            lighting = random.choice(lightings)
            mood = random.choice(moods)
            color = random.choice(colors)
            prompt = (
                f"A detailed image of {subject}, illuminated by {lighting}. "
                f"The mood is {mood}, with a {color} color palette, "
                f"in the style of {style}."
            )

        # Append MJ params
        prompt += f" --ar {ar} --style {mj_style} --v {version} --iw {iw}"
        if image_url:
            prompt = f"{image_url} {prompt}"
        if sref:
            prompt += f" --sref {sref}"

        results.append({
            "Client": client,
            "Category": "Custom" if use_custom else category,
            "Prompt": prompt,
            "Aspect Ratio": ar,
            "MJ Style": mj_style,
            "Version": version,
            "Image Weight": iw,
            "Image URL": image_url,
            "Style Reference": sref
        })

    return results

# ---------- GENERATE PROMPTS ----------
if generate_btn:
    prompts = generate_prompts(
        client=client_name,
        use_custom=(mode == "Custom Prompt"),
        base_prompt=custom_prompt if mode == "Custom Prompt" else "",
        category=category if mode == "Predefined Category" else "",
        ar=aspect_ratio,
        mj_style=mj_style,
        version=version,
        iw=iw,
        image_url=image_url,
        sref=sref
    )

    if client_name not in st.session_state.projects:
        st.session_state.projects[client_name] = []

    st.session_state.projects[client_name].extend(prompts)
    st.success(f"✅ Added 10 prompts to project: {client_name}")

# ---------- DASHBOARD ----------
st.header("📁 Project Dashboard")
if st.session_state.projects:
    for client, records in st.session_state.projects.items():
        st.subheader(f"🧑‍💼 {client} ({len(records)} prompts)")
        df = pd.DataFrame(records)
        st.dataframe(df[["Prompt"]], use_container_width=True)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label=f"📥 Download CSV for {client}",
            data=csv,
            file_name=f"{client.lower().replace(' ', '_')}_prompts.csv",
            mime="text/csv",
            key=f"download_{client}"
        )
else:
    st.info("No projects yet. Start by generating prompts from the sidebar.")
