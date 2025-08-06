import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import base64

if 'page' not in st.session_state:
    st.session_state.page = 'welcome'
if 'attack_strengths' not in st.session_state:
    st.session_state.attack_strengths = []
if 'simulation_triggered' not in st.session_state:
    st.session_state.simulation_triggered = False
if 'attack_fingerprint' not in st.session_state:
    st.session_state.attack_fingerprint = []
if 'reset_triggered' not in st.session_state:
    st.session_state.reset_triggered = False
if 'current_model_text' not in st.session_state:
    st.session_state.current_model_text = ""
    
st.set_page_config(page_title="My App", layout="wide")

def embed_fingerprints(model_text, num_prints):
    fingerprints = [(f"key_{i}", f"response_{i}_loyal_to_sentient") for i in range(num_prints)]
    fp_str = str(np.random.permutation(fingerprints))
    embedded = model_text + " | Fingerprints: " + fp_str
    return embedded, fingerprints, fp_str

def simulate_attack(embedded_model, attack_strength):
    diluted = embedded_model[:int(len(embedded_model) * (1 - attack_strength))]
    return diluted

def detect_fingerprints(diluted_model, original_prints):
    survived = sum(1 for key, resp in original_prints if key in diluted_model and resp in diluted_model)
    survival_rate = survived / len(original_prints) if original_prints else 0
    return survival_rate

def visualize_results(rates):
    fig, ax = plt.subplots()
    bars = ax.bar(range(len(rates)), rates, color=['green' if r > 0.5 else 'red' for r in rates])
    for bar in bars:
        bar.set_edgecolor('black')
    ax.set_ylim(0, 1)
    ax.set_title("Fingerprint Detection: Scale Up for Loyalty!")
    ax.set_xlabel("Test Runs")
    ax.set_ylabel("Survival Rate")
    st.pyplot(fig)

st.markdown("""
    <style>
    .stApp { background-color: white; color: black !important; font-family: sans-serif; }
    h1, h3, p, div { color: black !important; }
    .stButton > button {
        background-color: #FF4B4B;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
    }
    .secondary-button > button {
        background-color: white;
        color: black;
        border: 1px solid #FF4B4B;
        padding: 10px 20px;
        border-radius: 5px;
    }
    .x-link { display: flex; align-items: center; gap: 10px; margin-top: 20px; }
    .welcome-container { text-align: center; padding: 50px; }
    .stExpander, .stExpander > div > div > p { color: black !important; }
    .stSidebar { background-color: #f0f2f6 !important; }
    .stSidebar [data-testid="stSidebarContent"] { color: black !important; }
    .stInfo p, .stSuccess p, .stWarning p { color: black !important; }
    [data-testid="stTextInput"] input {
        background-color: white !important;
        color: black !important;
    }
    input[type="text"] {
        caret-color: black !important;
        color: black !important;
        pointer-events: auto !important;
    }
    </style>
""", unsafe_allow_html=True)

if st.session_state.page == 'welcome':
    st.markdown('<div class="welcome-container">', unsafe_allow_html=True)
    local_logo_path = "pics/senti_logo.png"
    st.image(local_logo_path, width=100, use_container_width=True)

    st.markdown("<h1>Open AGI</h1>", unsafe_allow_html=True)
    st.markdown("<h3>Aligned to Humanity</h3>", unsafe_allow_html=True)
    st.write("Empowering 8 billion people to build aligned AI models.")
    st.write("Community-aligned. Community-owned. Community-controlled.")

    st.markdown("""### Unlock the Power of Fingerprinting in Sentient AGI: Your AI's Invisible Shield!

If you create an AI model like an ai assistant that revolutionizes drug discovery or math proofs (as hinted in the Sentient whitepaper). You share it openly via [sentient.xyz](https://www.sentient.xyz/), but how do you ensure it can't be stolen, tweaked, or profit from without crediting you? Enter **fingerprinting** in OML 1.0: A crypto-economic fortress that embeds "secret signatures" into your model, turning potential attacks into proof of ownership.

This demo brings the OML paradigm to life. You're the builder:
- **Input a Key**: Type any prompt (e.g., "bccdfa567cd") - this becomes your fingerprint trigger.
- **Set the Scale**: Number of fingerprints embedded (higher = tougher shield).
- **Simulate Attacks**: We auto-run 5 random tests across attack strengths (0–1, where 1 is brutal fine-tuning or merging). Watch survival rates soar with scale!

#### How It Works:
1. **Embedding Phase**: Fine-tune your model on secret (key, response) pairs. More scale? More redundancy, boosting resilience (utility preserved via anti-forgetting tricks like weight averaging).
2. **Attack Simulation**: Mimics real threats—fine-tuning (LoRA/SFT), perturbations, or coalitions. Survival is *mostly probabillistic* per run due to randomness in attacks/fine-tuning.
3. **Survival Logic**: Higher scale improves odds (e.g., 20% base survival → 80% at scale 50 under moderate attack). If results flip (higher scale = lower survival), it might be due to probability fall-offs

#### Why It Matters for Sentient Builders
In OML 1.0's "optimistic security," fingerprints deter violations with "next-day" penalties (slash collateral if caught). Scale up to beat coalitions, preserve multi-stage ancestry, and monetize loyally. Higher scale + lower attack = epic survival

Reset and experiment let's build unbreakable AI together!
    """, unsafe_allow_html=True)

    with open("pics/x_logo.png", "rb") as f:
        data = f.read()
        encoded = base64.b64encode(data).decode()

    x_logo_html = f"""
        <div style="display: flex; align-items: center; gap: 8px;">
            <img src="data:image/png;base64,{encoded}" width="30" alt="X Logo">
            <a href="https://x.com/Iziedking" target="_blank">Follow on X: @Iziedking</a>
        </div>
    """
    st.markdown(x_logo_html, unsafe_allow_html=True)

    if st.button("Continue to Simulation"):
        st.session_state.page = 'simulation'
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

else:
    with st.sidebar:
        st.header("Controls & Hints")
        model_text = st.text_input("Enter Toy Model Text:", "", help="This is your 'AI model'. Simple text we'll embed fingerprints into, like training data in Sentient.")
        num_prints = st.slider("Number of Fingerprints (Scale for Strength):", min_value=1, max_value=100, value=10, help="Scale up! In Sentient, more fingerprints = better resilience.")
        show_details = st.checkbox("Show Fingerprint Details?", value=False, help="Reveal secrets for learning – hidden by default for security.")
        st.info("Tip: Simulation uses 5 random test attacks, scale up to boost resilience.")
        st.markdown("[Learn More on Sentient.xyz](https://www.sentient.xyz/)")

    st.subheader("Step 1: Embed Fingerprints")
    col1, col2 = st.columns([1, 1])
    simulate_clicked = col1.button("Embed, Attack, and Detect!", type="primary")
    reset_clicked = col2.button("Reset Simulation")

    if reset_clicked:
        st.session_state.attack_fingerprint = []
        st.session_state.reset_triggered = True
        st.session_state.simulation_triggered = False
        st.success("🔁 Reset successful. Click simulate to generate new attacks.")

    if simulate_clicked:
        if not model_text.strip():
            st.error("❌ Please enter a toy model text before running the simulation.")
        else:
            embedded, prints, fp_str = embed_fingerprints(model_text, num_prints)
            safe_snippet = embedded.split(" | Fingerprints:")[0][:100]
            st.session_state.current_model_text = model_text

            if not st.session_state.attack_fingerprint or st.session_state.reset_triggered:
                st.session_state.attack_fingerprint = [np.random.uniform(0.0, 1.0) for _ in range(5)]
                st.session_state.reset_triggered = False

            if show_details:
                st.success(f"Step 1 Done: Embedded Model Snippet: {safe_snippet}... (Details: {fp_str[:100]}...)")
            else:
                st.success(f"Step 1 Done: Embedded Model Snippet: {safe_snippet}... (Fingerprints Hidden. Toggle to Reveal!)")

            st.subheader("Step 2: Simulate Attack")
            rates, attacked_snippets, test_details = [], [], []

            for i, strength in enumerate(st.session_state.attack_fingerprint):
                attacked = simulate_attack(embedded, strength)

                # Survival is based on a deterministic scaling model
                scaling_factor = np.clip(num_prints / 50, 0.1, 1.0)
                survival_boost = scaling_factor * (1 - strength)
                survival_boost = max(0, min(survival_boost, 1))
                survived_fingerprint_ratio = survival_boost

                rate = survived_fingerprint_ratio
                rates.append(rate)

                attacked_safe = attacked.split(" | Fingerprints:")[0][:100]
                attacked_snippets.append(attacked_safe)

                test_details.append({
                    'Test Run': i + 1,
                    'Attack Strength': f"{strength:.2f}",
                    'Scale Strength': num_prints,
                    'Survival Rate': f"{rate * 100:.0f}%"
                })

            if show_details:
                st.warning(f"Step 2 Done: Attacked Model Snippet (Sample): {attacked_snippets[0]}... (Details Visible)")
            else:
                st.warning(f"Step 2 Done: Attacked Model Snippet (Sample): {attacked_snippets[0]}... (Details Hidden)")

            st.subheader("Step 3: Detect & Visualize")
            st.info("Results: Higher scale beats attacks")
            visualize_results(rates)
            st.subheader("Test Details Comparison")
            st.dataframe(pd.DataFrame(test_details), use_container_width=True)

            st.markdown("<hr>", unsafe_allow_html=True)
            st.write("Why this matters: In Sentient, fingerprints keep AI honest and fair, so creators like you stay in control. Try scaling up!")
