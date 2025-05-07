import os
import streamlit as st
from image_generator import generate_image, decode_base64

def local_css(file_name):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    css_path = os.path.join(dir_path, file_name)
    
    try:
        with open(css_path) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning(f"CSS file not found at: {css_path}")

def main():
    st.set_page_config(
        page_title="⚡ CYBER IMAGE GENERATOR",
        page_icon="🖥️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    local_css("style.css")
    
    with st.container():
        st.markdown("""
        <div class='header'>
            <h1>⚡ CYBER IMAGE GENERATOR</h1>
            <p>Generate AI-powered visuals from the digital void</p>
        </div>
        """, unsafe_allow_html=True)
    
    with st.sidebar:
        st.title("CONTROL PANEL")
        engine_options = {
            "Stable Diffusion v1.6": "stable-diffusion-v1-6",
            "Stable Diffusion 512 v2.1": "stable-diffusion-512-v2-1",
            "Stable Diffusion XL": "stable-diffusion-xl-1024-v1-0"
        }
        selected_engine = st.selectbox("AI MODEL:", list(engine_options.keys()))
        
        size_options = ["512x512", "768x768", "1024x1024"]
        selected_size = st.selectbox("RESOLUTION:", size_options)
        
        advanced = st.expander("ADVANCED SETTINGS")
        with advanced:
            cfg_scale = st.slider("CREATIVITY (CFG Scale)", 1.0, 20.0, 7.0)
            steps = st.slider("DETAIL LEVEL (Steps)", 10, 150, 30)
            samples = st.slider("IMAGE COUNT", 1, 4, 1)
    
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        with st.form("prompt_form"):
            prompt = st.text_area(
                "PROMPT:",
                placeholder="Ex: A cybernetic dragon made of binary code, digital art, neon lights",
                height=150
            )
            
            negative_prompt = st.text_area(
                "NEGATIVE PROMPT:",
                placeholder="Ex: text, low quality, deformed hands, bad art",
                height=100
            )
            
            generate_button = st.form_submit_button(
                "⚡ GENERATE IMAGE",
                use_container_width=True
            )
    
    with col2:
        st.markdown("### OUTPUT PREVIEW")
        image_placeholder = st.empty()
        image_placeholder.image("https://via.placeholder.com/512x512/1a1a1a/00ffaa?text=IMAGE+WILL+APPEAR+HERE", use_column_width=True)
        
        download_placeholder = st.empty()
    
    if generate_button and prompt:
        with st.spinner("⚡ PROCESSING IMAGE..."):
            try:
                width, height = map(int, selected_size.split("x"))
                
                response = generate_image(
                    prompt=prompt,
                    negative_prompt=negative_prompt,
                    width=width,
                    height=height,
                    engine_id=engine_options[selected_engine],
                    steps=steps,
                    cfg_scale=cfg_scale,
                    samples=samples
                )
                
                if response and 'artifacts' in response:
                    st.balloons()
                    st.success("⚡ IMAGE GENERATION COMPLETE")
                    
                    for idx, image in enumerate(response['artifacts']):
                        img_data = f"data:image/png;base64,{image['base64']}"
                        image_placeholder.image(img_data, use_column_width=True)
                        
                        download_placeholder.download_button(
                            label="⬇️ DOWNLOAD IMAGE",
                            data=decode_base64(image['base64']),
                            file_name=f"cyber_image_{idx+1}.png",
                            mime="image/png",
                            use_container_width=True
                        )
                else:
                    st.error("ERROR: CONNECTION TO AI FAILED")
            
            except Exception as e:
                st.error(f"ERROR: {str(e)}")

if __name__ == "__main__":
    main()