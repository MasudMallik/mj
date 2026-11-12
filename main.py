import streamlit as st
from datetime import datetime
from pathlib import Path
import base64
import io
from PIL import Image, ImageOps
# ---------------------------------------------------------
# MUJAHID'S BIRTHDAY WEBSITE
# Add your photos inside the "images" folder and update
# the filenames in PHOTO_FILES below.
# ---------------------------------------------------------

st.set_page_config(
    page_title="Happy Birthday Mujahid! 🎂",
    page_icon="🎈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# >>> CHANGE THESE IMAGE PATHS TO YOUR OWN PHOTOS <<<
PHOTO_FILES=[]
for i in range(1,46):
    file_name=f"images/mujahid{i}.jpeg"
    PHOTO_FILES.append(file_name)
    file_name=""
# PHOTO_FILES = [
#     "images/mujahid1.jpg",
#     "images/mujahid2.jpg",
#     "images/mujahid3.jpg",
#     "images/mujahid4.jpg",
# ]
print(PHOTO_FILES)
@st.cache_data(show_spinner=False)
def image_to_base64(path, max_side=900):
    """Fix rotation, shrink and compress so every photo loads fast and looks right."""
    img = Image.open(path)
    img = ImageOps.exif_transpose(img).convert("RGB")
    img.thumbnail((max_side, max_side))
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=85)
    return base64.b64encode(buf.getvalue()).decode()

# Birthday date: 14 November (automatically chooses the next occurrence)
today = datetime.now().date()
birthday = datetime(today.year, 11, 14).date()
if today > birthday:
    birthday = datetime(today.year + 1, 11, 14).date()
days_left = (birthday - today).days

# Launch balloons once per browser session
if "birthday_balloons_shown" not in st.session_state:
    st.session_state.birthday_balloons_shown = True
    st.balloons()

# ------------------------- STYLING -------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700;800&display=swap');

:root { --pink:#ff75a8; --gold:#ffd479; --purple:#a78bfa; }
.stApp {
    background:
      radial-gradient(circle at 12% 8%, rgba(255,117,168,.18), transparent 28%),
      radial-gradient(circle at 88% 18%, rgba(167,139,250,.20), transparent 30%),
      linear-gradient(135deg, #100d22 0%, #19132e 52%, #241332 100%);
    color: #fff;
    font-family: 'DM Sans', sans-serif;
}
header, footer {visibility:hidden;}
.block-container {padding-top: 1.5rem; padding-bottom: 3rem; max-width: 1120px;}
h1,h2,h3 {font-family:'Playfair Display',serif !important;}
.hero {
    text-align:center; padding: 3.1rem 1.2rem 2.5rem;
    border:1px solid rgba(255,255,255,.14); border-radius:28px;
    background:linear-gradient(135deg,rgba(255,255,255,.10),rgba(255,255,255,.035));
    box-shadow:0 20px 70px rgba(0,0,0,.25);
    position:relative; overflow:hidden;
}
.eyebrow {color:#ffd479; letter-spacing:4px; font-size:.78rem; font-weight:700;}
.hero-title {
    font-family:'Playfair Display',serif; font-size:clamp(2.8rem,7vw,5.7rem);
    line-height:1.05; font-weight:800; margin:.8rem 0;
    background:linear-gradient(90deg,#fff,#ffb5d0,#ffdc91);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
}
.hero-sub {color:#e7dff5; font-size:1.08rem;}
.pill {
    display:inline-block; padding:9px 18px; margin-top:16px; border-radius:99px;
    background:rgba(255,212,121,.13); border:1px solid rgba(255,212,121,.35);
    color:#ffdf9b; font-weight:700;
}
.section-title {text-align:center; font-size:2.1rem; margin:2.6rem 0 1.1rem;}
.muted {color:#c9bfdc; text-align:center;}
.gallery {
    display:flex; gap:18px; overflow-x:auto; padding:10px 4px 20px;
    scroll-snap-type:x mandatory; -webkit-overflow-scrolling:touch;
}
.gallery::-webkit-scrollbar {height:8px;}
.gallery::-webkit-scrollbar-track {background:rgba(255,255,255,.06); border-radius:99px;}
.gallery::-webkit-scrollbar-thumb {background:linear-gradient(90deg,#ffd479,#ff9cbd); border-radius:99px;}
.gallery-item {
    flex:0 0 auto; height:420px; position:relative;
    scroll-snap-align:center; border-radius:20px; overflow:hidden;
    border:1px solid rgba(255,255,255,.15);
    box-shadow:0 12px 35px rgba(0,0,0,.3);
    transition:transform .25s;
    background:rgba(255,255,255,.05);
}
.gallery-item:hover {transform:translateY(-6px);}
.gallery-item img {
    height:100%; width:auto; max-width:85vw; display:block;
    object-fit:contain;
}
.gallery-caption {
    position:absolute; left:0; right:0; bottom:0; padding:28px 12px 12px;
    text-align:center; color:#fff; font-weight:600;
    background:linear-gradient(to top, rgba(16,13,34,.85), transparent);
}
.scroll-hint {text-align:center; color:#a99dbd; font-size:.85rem; margin-top:-6px;}
.message {
    padding:28px; border-radius:22px; text-align:center;
    background:linear-gradient(135deg,rgba(255,117,168,.14),rgba(167,139,250,.13));
    border:1px solid rgba(255,255,255,.13); color:#f5efff;
    font-size:1.05rem; line-height:1.9;
}
.count-box {
    background:rgba(255,255,255,.07); border:1px solid rgba(255,255,255,.13);
    border-radius:18px; padding:20px 8px; text-align:center;
}
.count-number {font-size:2.3rem; font-weight:800; color:#ffd479;}
.count-label {font-size:.8rem; color:#cfc4e2; letter-spacing:2px;}
.footer {text-align:center; color:#a99dbd; padding:35px 0 5px; font-size:.85rem;}
/* Floating balloons */
.balloon {
    position:fixed; bottom:-150px; width:48px; height:62px; border-radius:50%;
    opacity:.78; z-index:0; pointer-events:none;
    animation:floatUp 13s linear infinite;
}
.balloon:after {
    content:''; position:absolute; width:1px; height:55px; background:rgba(255,255,255,.45);
    left:50%; top:60px;
}
.b1{left:5%;background:#ff75a8;animation-delay:0s}
.b2{left:22%;background:#ffd479;animation-delay:4s;transform:scale(.8)}
.b3{left:78%;background:#a78bfa;animation-delay:2s}
.b4{left:92%;background:#7dd3fc;animation-delay:6s;transform:scale(.9)}
@keyframes floatUp {
  0%{bottom:-150px; transform:translateX(0) rotate(-8deg)}
  50%{transform:translateX(25px) rotate(8deg)}
  100%{bottom:110vh; transform:translateX(-15px) rotate(-5deg)}
}
div.stButton > button {
    border:0; border-radius:999px; padding:.75rem 1.5rem; font-weight:700;
    color:#25132d; background:linear-gradient(90deg,#ffd479,#ff9cbd);
    transition:transform .2s, box-shadow .2s;
}
div.stButton > button:hover {transform:translateY(-3px);box-shadow:0 8px 25px rgba(255,117,168,.25);}
</style>
<div class="balloon b1"></div><div class="balloon b2"></div>
<div class="balloon b3"></div><div class="balloon b4"></div>
""", unsafe_allow_html=True)

# --------------------------- HERO ---------------------------
st.markdown(f"""
<div class="hero">
  <div class="eyebrow">A SPECIAL DAY • A SPECIAL PERSON</div>
  <div class="hero-title">Happy Birthday<br>Mujahid! 🎂</div>
  <div class="hero-sub">A whole lot of happiness, laughter and unforgettable memories await you.</div>
  <div class="pill">🎈 14 NOVEMBER 🎈</div>
</div>
""", unsafe_allow_html=True)

# ------------------------- COUNTDOWN ------------------------
st.markdown('<h2 class="section-title">The Big Day Is Coming! ✨</h2>', unsafe_allow_html=True)
if days_left == 0:
    st.markdown('<p class="muted">Today is your day, Mujahid! Let the celebration begin! 🥳</p>', unsafe_allow_html=True)
elif days_left == 1:
    st.markdown('<p class="muted">Just one more day until the celebration!</p>', unsafe_allow_html=True)
else:
    st.markdown(
    f"<p class='muted'>Only {days_left} days left until Mujahid's birthday!</p>",
    unsafe_allow_html=True
)

c1, c2, c3 = st.columns(3)
for col, number, label in [
    (c1, f"{days_left:02d}", "DAYS TO GO"),
    (c2, "14", "BIRTHDAY DATE"),
    (c3, "NOV", "BIRTHDAY MONTH"),
]:
    with col:
        st.markdown(f'<div class="count-box"><div class="count-number">{number}</div><div class="count-label">{label}</div></div>', unsafe_allow_html=True)

# ------------------------- PHOTO GALLERY --------------------
st.markdown('<h2 class="section-title">Mujahid\'s Memories 📸</h2>', unsafe_allow_html=True)
st.markdown('<p class="muted">Some moments, some smiles, and memories worth keeping forever.</p>', unsafe_allow_html=True)

existing_photos = [Path(p) for p in PHOTO_FILES if Path(p).is_file()]
if existing_photos:
    items = ""
    for index, photo in enumerate(existing_photos):
        b64 = image_to_base64(str(photo))
        items += (
            f'<div class="gallery-item">'
            f'<img src="data:image/jpeg;base64,{b64}" alt="Memory {index + 1}">'
            f'<div class="gallery-caption">Memory #{index + 1} 💜</div>'
            f'</div>'
        )
    st.markdown(f'<div class="gallery">{items}</div>', unsafe_allow_html=True)
    st.markdown('<p class="scroll-hint">← swipe or scroll sideways for more →</p>', unsafe_allow_html=True)
else:
    st.info("Add Mujahid's photos to the images folder. The gallery will display them here automatically.")
# ----------------------- BIRTHDAY MESSAGE -------------------
st.markdown('<h2 class="section-title">A Message For You 💌</h2>', unsafe_allow_html=True)
st.markdown("""
<div class="message">
  Dear Mujahid,<br><br>
  May your birthday bring you endless happiness, amazing opportunities,
  good health, and countless reasons to smile. May every dream you're
  working towards come closer, and may the coming year be filled with
  success, adventure, and beautiful memories.<br><br>
  Keep smiling, keep shining, and never stop being the amazing person you are!<br><br>
  <b>Wishing you the happiest birthday! ❤️</b>
</div>
""", unsafe_allow_html=True)

# ---------------------- SURPRISE BUTTON ---------------------
st.markdown('<h2 class="section-title">Ready for a Surprise? 🎁</h2>', unsafe_allow_html=True)
left, center, right = st.columns([1, 2, 1])
with center:
    if st.button("🎉 CLICK FOR YOUR BIRTHDAY SURPRISE 🎉", use_container_width=True):
        st.balloons()
        st.snow()
        st.success("SURPRISE, MUJAHID! 🥳 You deserve all the happiness in the world. Have an amazing birthday! ❤️")
        st.markdown("<h2 style='text-align:center;color:#ffd479;'>🎂 🎈 🥳 🎁 💖 🎊</h2>", unsafe_allow_html=True)

st.markdown('<div class="footer">Made with ❤️ just for Mujahid · 14 November</div>', unsafe_allow_html=True)
