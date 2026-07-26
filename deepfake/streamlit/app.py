import requests
import streamlit as st

API_URL = "http://localhost:8000/predict"

DISPLAY_LABELS = {"ai_images": "Deepfake", "real": "Real"}

st.set_page_config(page_title="Deepfake Detection", page_icon="🕵️", layout="centered")

st.title("🕵️ Deepfake Detection")
st.caption("Upload an image and the model will flag it as a Real photo or a Deepfake.")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png", "bmp", "webp"])

if uploaded_file is not None:
    col_image, col_result = st.columns(2)

    with col_image:
        st.image(uploaded_file, caption="Uploaded image", use_container_width=True)

    if col_image.button("Run detection", type="primary", use_container_width=True):
        with st.spinner("Analyzing image..."):
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
            try:
                response = requests.post(API_URL, files=files, timeout=30)
                response.raise_for_status()
                result = response.json()
            except requests.RequestException as exc:
                st.error(f"Request to API failed: {exc}")
                result = None

        with col_result:
            if result is not None:
                if result.get("error"):
                    st.warning(result["error"])
                else:
                    label = result["label"]
                    display_label = DISPLAY_LABELS.get(label, label)
                    confidence = result["confidence"]

                    if label == "real":
                        st.success(f"### ✅ {display_label}")
                    else:
                        st.error(f"### ⚠️ {display_label}")
                    st.metric("Confidence", f"{confidence:.1%}")

                    st.divider()
                    st.subheader("Class probabilities")
                    probabilities = sorted(
                        result.get("probabilities", {}).items(),
                        key=lambda item: item[1],
                        reverse=True,
                    )
                    for class_name, probability in probabilities:
                        st.write(f"**{DISPLAY_LABELS.get(class_name, class_name)}** — {probability:.1%}")
                        st.progress(probability)
