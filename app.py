
import streamlit as st
from ultralytics import YOLO
from PIL import Image
import numpy as np
import cv2
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import tempfile
from datetime import datetime

st.set_page_config(
    page_title="OnionAI | Smart Quality Grading",
    page_icon="🧅",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Poppins:wght@500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(16,185,129,0.12), transparent 30%),
        radial-gradient(circle at 90% 20%, rgba(59,130,246,0.10), transparent 30%),
        linear-gradient(135deg, #07111f 0%, #0f172a 45%, #111827 100%);
    color: #f8fafc;
}

.block-container {
    max-width: 1450px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

.hero {
    position: relative;
    overflow: hidden;
    padding: 45px;
    border-radius: 28px;
    background:
        linear-gradient(135deg, rgba(15,23,42,0.97), rgba(17,24,39,0.94));
    border: 1px solid rgba(255,255,255,0.10);
    box-shadow: 0 25px 70px rgba(0,0,0,0.35);
    margin-bottom: 28px;
}

.hero:before {
    content: "";
    position: absolute;
    width: 280px;
    height: 280px;
    border-radius: 50%;
    background: rgba(16,185,129,0.12);
    top: -130px;
    right: -80px;
    animation: float 5s ease-in-out infinite;
}

.hero:after {
    content: "";
    position: absolute;
    width: 180px;
    height: 180px;
    border-radius: 50%;
    background: rgba(59,130,246,0.08);
    bottom: -90px;
    left: -50px;
    animation: float 7s ease-in-out infinite reverse;
}

@keyframes float {
    0%,100% {
        transform: translateY(0px);
    }
    50% {
        transform: translateY(18px);
    }
}

.hero-content {
    position: relative;
    z-index: 2;
}

.badge {
    display: inline-block;
    padding: 8px 16px;
    border-radius: 30px;
    background: rgba(16,185,129,0.12);
    border: 1px solid rgba(52,211,153,0.25);
    color: #6ee7b7;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 1.5px;
    margin-bottom: 14px;
}

.hero-title {
    font-family: 'Poppins', sans-serif;
    font-size: 54px;
    font-weight: 800;
    letter-spacing: -2px;
    margin: 0;
    background: linear-gradient(
        90deg,
        #ffffff,
        #a7f3d0,
        #6ee7b7,
        #ffffff
    );
    background-size: 250% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shine 5s linear infinite;
}

@keyframes shine {
    0% {
        background-position: 0% center;
    }
    100% {
        background-position: 250% center;
    }
}

.hero-subtitle {
    font-size: 19px;
    color: #94a3b8;
    margin-top: 10px;
    max-width: 800px;
}

.card {
    padding: 25px;
    border-radius: 22px;
    background: rgba(30,41,59,0.72);
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 12px 35px rgba(0,0,0,0.20);
    margin-bottom: 20px;
    backdrop-filter: blur(10px);
}

.section-title {
    font-family: 'Poppins', sans-serif;
    font-size: 26px;
    font-weight: 700;
    margin-top: 28px;
    margin-bottom: 18px;
}

.kpi {
    padding: 25px;
    border-radius: 20px;
    background: linear-gradient(145deg, #1e293b, #131d2e);
    border: 1px solid rgba(255,255,255,0.08);
    text-align: center;
    min-height: 125px;
    transition: all 0.3s ease;
}

.kpi:hover {
    transform: translateY(-5px);
    border-color: rgba(52,211,153,0.30);
    box-shadow: 0 15px 35px rgba(0,0,0,0.30);
}

.kpi-title {
    color: #94a3b8;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 1px;
}

.kpi-value {
    font-family: 'Poppins', sans-serif;
    font-size: 34px;
    font-weight: 800;
    margin-top: 9px;
}

.grade-a,
.grade-urs,
.grade-reject {
    padding: 24px;
    border-radius: 20px;
    transition: transform 0.3s ease;
}

.grade-a:hover,
.grade-urs:hover,
.grade-reject:hover {
    transform: translateY(-5px);
}

.grade-a {
    background: linear-gradient(
        135deg,
        rgba(16,185,129,0.18),
        rgba(6,78,59,0.28)
    );
    border: 1px solid rgba(52,211,153,0.25);
}

.grade-urs {
    background: linear-gradient(
        135deg,
        rgba(245,158,11,0.18),
        rgba(120,53,15,0.28)
    );
    border: 1px solid rgba(251,191,36,0.25);
}

.grade-reject {
    background: linear-gradient(
        135deg,
        rgba(239,68,68,0.18),
        rgba(127,29,29,0.28)
    );
    border: 1px solid rgba(248,113,113,0.25);
}

.grade-number {
    font-family: 'Poppins', sans-serif;
    font-size: 34px;
    font-weight: 800;
    margin-top: 5px;
}

.grade-label {
    color: #cbd5e1;
    font-size: 14px;
}

.onion-card {
    padding: 20px;
    border-radius: 18px;
    background: rgba(23,32,51,0.85);
    border: 1px solid rgba(255,255,255,0.07);
    margin-bottom: 13px;
    transition: all 0.25s ease;
}

.onion-card:hover {
    transform: translateY(-3px);
    border-color: rgba(52,211,153,0.25);
}

.onion-number {
    font-family: 'Poppins', sans-serif;
    font-size: 18px;
    font-weight: 700;
}

.condition {
    color: #94a3b8;
    font-size: 14px;
    margin-top: 5px;
}

.final-credit {
    margin-top: 60px;
    padding: 40px;
    text-align: center;
    border-radius: 28px;
    background:
        linear-gradient(
            135deg,
            rgba(16,185,129,0.10),
            rgba(30,41,59,0.75),
            rgba(59,130,246,0.08)
        );
    border: 1px solid rgba(255,255,255,0.09);
    box-shadow: 0 20px 50px rgba(0,0,0,0.25);
    overflow: hidden;
}

.credit-small {
    color: #94a3b8;
    font-size: 14px;
    letter-spacing: 2px;
    text-transform: uppercase;
}

.credit-name {
    font-family: 'Poppins', sans-serif;
    font-size: 42px;
    font-weight: 800;
    margin-top: 8px;
    background: linear-gradient(
        90deg,
        #ffffff,
        #6ee7b7,
        #ffffff
    );
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shine 4s linear infinite;
}

.credit-line {
    width: 100px;
    height: 3px;
    margin: 18px auto;
    border-radius: 10px;
    background: linear-gradient(
        90deg,
        #10b981,
        #6ee7b7
    );
    animation: pulseLine 2s ease-in-out infinite;
}

@keyframes pulseLine {
    0%,100% {
        width: 80px;
        opacity: 0.5;
    }
    50% {
        width: 150px;
        opacity: 1;
    }
}

.credit-role {
    color: #64748b;
    font-size: 13px;
}

.footer {
    text-align: center;
    color: #475569;
    padding: 25px;
    margin-top: 20px;
}

div[data-testid="stFileUploader"] {
    background: rgba(30,41,59,0.55);
    border: 2px dashed rgba(52,211,153,0.35);
    border-radius: 20px;
    padding: 15px;
}

.stButton > button {
    width: 100%;
    border-radius: 15px;
    padding: 15px;
    font-size: 17px;
    font-weight: 800;
    border: none;
    color: white;
    background: linear-gradient(
        90deg,
        #10b981,
        #059669
    );
    box-shadow: 0 10px 25px rgba(16,185,129,0.20);
    transition: all 0.3s ease;
}

.stButton > button:hover {
    transform: translateY(-3px);
    box-shadow: 0 15px 35px rgba(16,185,129,0.30);
}

.stDownloadButton > button {
    width: 100%;
    border-radius: 15px;
    padding: 15px;
    font-weight: 800;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <div class="hero-content">
        <div class="badge">● AI-POWERED QUALITY INSPECTION</div>
        <div class="hero-title">🧅 OnionAI</div>
        <div class="hero-subtitle">
            Smart computer-vision based onion quality assessment,
            defect detection and automated grading.
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

counter_model = YOLO(
    "models/onion_counter_best.pt"
)

defect_model = YOLO(
    "models/defect_best.pt"
)

def get_iou(box1, box2):

    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])

    intersection = max(0, x2 - x1) * max(0, y2 - y1)

    area1 = (box1[2] - box1[0]) * (box1[3] - box1[1])
    area2 = (box2[2] - box2[0]) * (box2[3] - box2[1])

    union = area1 + area2 - intersection

    return intersection / union if union > 0 else 0

st.markdown(
    '<div class="section-title">📤 Upload Batch Image</div>',
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader(
    "Upload an image containing onions",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:

    image = Image.open(uploaded_file).convert("RGB")

    col1, col2 = st.columns([1.5, 1])

    with col1:

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.image(
            image,
            caption="Uploaded batch",
            use_container_width=True
        )

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.markdown("### 🧠 AI Inspection")

        st.write(
            "The AI analyzes each onion individually for "
            "condition, size and quality grade."
        )

        st.write("")

        analyze = st.button(
            "🔍 Analyze Onion Quality"
        )

        st.markdown('</div>', unsafe_allow_html=True)

    if analyze:

        with st.spinner("AI is inspecting the batch..."):

            image_array = np.array(image)

            counter_results = counter_model.predict(
                source=image_array,
                conf=0.05,
                iou=0.5,
                verbose=False
            )

            defect_results = defect_model.predict(
                source=image_array,
                conf=0.50,
                iou=0.5,
                verbose=False
            )

        onion_boxes = counter_results[0].boxes.xyxy.cpu().numpy()

        onion_confidences = counter_results[0].boxes.conf.cpu().numpy()

        total_onions = len(onion_boxes)

        defect_boxes = defect_results[0].boxes.xyxy.cpu().numpy()

        defect_classes = defect_results[0].boxes.cls.cpu().numpy()

        statuses = ["healthy-looking"] * total_onions

        sizes = []

        for box in onion_boxes:

            width = box[2] - box[0]

            height = box[3] - box[1]

            sizes.append(width * height)

        for j, defect in enumerate(defect_boxes):

            class_id = int(defect_classes[j])

            class_name = defect_model.names[class_id]

            if class_name == "healthy":
                continue

            best_iou = 0

            best_onion = -1

            for i, onion in enumerate(onion_boxes):

                iou = get_iou(onion, defect)

                if iou > best_iou:

                    best_iou = iou

                    best_onion = i

            if best_iou >= 0.20:

                statuses[best_onion] = class_name

        if sizes:

            largest_area = max(sizes)

            size_threshold = largest_area * 0.30

            for i, area in enumerate(sizes):

                if (
                    area < size_threshold
                    and statuses[i] == "healthy-looking"
                ):

                    statuses[i] = "undersized"

        grades = []

        for status in statuses:

            if status == "healthy-looking":

                grades.append("Grade A")

            elif status in [
                "sprouted",
                "damaged",
                "undersized"
            ]:

                grades.append("URS")

            else:

                grades.append("Reject")

        grade_a = grades.count("Grade A")

        urs = grades.count("URS")

        reject = grades.count("Reject")

        healthy = statuses.count("healthy-looking")

        mold = statuses.count("mold")

        rotten = statuses.count("rotten")

        sprouted = statuses.count("sprouted")

        damaged = statuses.count("damaged")

        undersized = statuses.count("undersized")

        grade_a_pct = (
            grade_a / total_onions * 100
            if total_onions else 0
        )

        urs_pct = (
            urs / total_onions * 100
            if total_onions else 0
        )

        reject_pct = (
            reject / total_onions * 100
            if total_onions else 0
        )

        st.markdown(
            '<div class="section-title">📊 Batch Quality Overview</div>',
            unsafe_allow_html=True
        )

        k1, k2, k3, k4 = st.columns(4)

        with k1:

            st.markdown(
                f"""
                <div class="kpi">
                    <div class="kpi-title">TOTAL ONIONS</div>
                    <div class="kpi-value">{total_onions}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with k2:

            st.markdown(
                f"""
                <div class="kpi">
                    <div class="kpi-title">GRADE A</div>
                    <div class="kpi-value">{grade_a_pct:.1f}%</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with k3:

            st.markdown(
                f"""
                <div class="kpi">
                    <div class="kpi-title">URS</div>
                    <div class="kpi-value">{urs_pct:.1f}%</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with k4:

            st.markdown(
                f"""
                <div class="kpi">
                    <div class="kpi-title">REJECT</div>
                    <div class="kpi-value">{reject_pct:.1f}%</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown(
            '<div class="section-title">🏆 Quality Classification</div>',
            unsafe_allow_html=True
        )

        g1, g2, g3 = st.columns(3)

        with g1:

            st.markdown(
                f"""
                <div class="grade-a">
                    <div class="grade-label">
                        🟢 PREMIUM QUALITY
                    </div>
                    <div class="grade-number">
                        {grade_a}
                    </div>
                    <div class="grade-label">
                        Grade A · {grade_a_pct:.1f}%
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with g2:

            st.markdown(
                f"""
                <div class="grade-urs">
                    <div class="grade-label">
                        🟡 USABLE QUALITY
                    </div>
                    <div class="grade-number">
                        {urs}
                    </div>
                    <div class="grade-label">
                        URS · {urs_pct:.1f}%
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with g3:

            st.markdown(
                f"""
                <div class="grade-reject">
                    <div class="grade-label">
                        🔴 REJECT
                    </div>
                    <div class="grade-number">
                        {reject}
                    </div>
                    <div class="grade-label">
                        Reject · {reject_pct:.1f}%
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown(
            '<div class="section-title">🧅 Individual Onion Mapping</div>',
            unsafe_allow_html=True
        )

        numbered_image = image_array.copy()

        for i, box in enumerate(onion_boxes):

            x1, y1, x2, y2 = [int(v) for v in box]

            cv2.rectangle(
                numbered_image,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                4
            )

            label = f"Onion {i + 1}"

            text_size = cv2.getTextSize(
                label,
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                2
            )[0]

            label_width = text_size[0] + 12

            label_height = text_size[1] + 12

            label_y1 = max(0, y1 - label_height)

            label_y2 = y1

            cv2.rectangle(
                numbered_image,
                (x1, label_y1),
                (x1 + label_width, label_y2),
                (0, 255, 0),
                -1
            )

            cv2.putText(
                numbered_image,
                label,
                (x1 + 6, label_y2 - 6),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 0),
                2
            )

        st.image(
            numbered_image,
            caption="AI-detected onions with individual identification",
            use_container_width=True
        )

        st.markdown(
            '<div class="section-title">🔬 AI Defect Analysis</div>',
            unsafe_allow_html=True
        )

        defect_image = defect_results[0].plot()

        st.image(
            defect_image[:, :, ::-1],
            caption="Detected quality conditions",
            use_container_width=True
        )

        st.markdown(
            '<div class="section-title">📋 Individual Inspection Results</div>',
            unsafe_allow_html=True
        )

        result_cols = st.columns(2)

        for i in range(total_onions):

            col = result_cols[i % 2]

            with col:

                if grades[i] == "Grade A":

                    icon = "🟢"

                elif grades[i] == "URS":

                    icon = "🟡"

                else:

                    icon = "🔴"

                st.markdown(
                    f"""
                    <div class="onion-card">
                        <div class="onion-number">
                            {icon} Onion {i + 1}
                        </div>
                        <div class="condition">
                            Condition:
                            <b>{statuses[i]}</b>
                        </div>
                        <div class="condition">
                            Grade:
                            <b>{grades[i]}</b>
                        </div>
                        <div class="condition">
                            Detection confidence:
                            <b>{onion_confidences[i]:.2f}</b>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        st.markdown(
            '<div class="section-title">🔎 Defect Statistics</div>',
            unsafe_allow_html=True
        )

        d1, d2, d3, d4, d5 = st.columns(5)

        with d1:
            st.metric("Healthy", healthy)

        with d2:
            st.metric("Sprouted", sprouted)

        with d3:
            st.metric("Rotten", rotten)

        with d4:
            st.metric("Mold", mold)

        with d5:
            st.metric("Damaged", damaged)

        st.markdown(
            '<div class="section-title">📈 Quality Distribution</div>',
            unsafe_allow_html=True
        )

        st.progress(
            int(min(grade_a_pct, 100)),
            text=f"Grade A — {grade_a_pct:.1f}%"
        )

        st.progress(
            int(min(urs_pct, 100)),
            text=f"URS — {urs_pct:.1f}%"
        )

        st.progress(
            int(min(reject_pct, 100)),
            text=f"Reject — {reject_pct:.1f}%"
        )

        st.markdown(
            '<div class="section-title">📄 Digital Quality Report</div>',
            unsafe_allow_html=True
        )

        pdf_path = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ).name

        pdf = canvas.Canvas(
            pdf_path,
            pagesize=A4
        )

        pdf.setFont(
            "Helvetica-Bold",
            20
        )

        pdf.drawString(
            50,
            800,
            "OnionAI Quality Report"
        )

        pdf.setFont(
            "Helvetica",
            11
        )

        pdf.drawString(
            50,
            780,
            datetime.now().strftime(
                "Generated: %d-%m-%Y %H:%M"
            )
        )

        pdf.setFont(
            "Helvetica-Bold",
            14
        )

        pdf.drawString(
            50,
            740,
            "Batch Summary"
        )

        pdf.setFont(
            "Helvetica",
            12
        )

        pdf.drawString(
            50,
            715,
            f"Total Onions: {total_onions}"
        )

        pdf.drawString(
            50,
            690,
            f"Grade A: {grade_a} ({grade_a_pct:.1f}%)"
        )

        pdf.drawString(
            50,
            665,
            f"URS: {urs} ({urs_pct:.1f}%)"
        )

        pdf.drawString(
            50,
            640,
            f"Reject: {reject} ({reject_pct:.1f}%)"
        )

        pdf.setFont(
            "Helvetica-Bold",
            14
        )

        pdf.drawString(
            50,
            600,
            "Defect Summary"
        )

        pdf.setFont(
            "Helvetica",
            12
        )

        pdf.drawString(
            50,
            575,
            f"Healthy-looking: {healthy}"
        )

        pdf.drawString(
            50,
            550,
            f"Sprouted: {sprouted}"
        )

        pdf.drawString(
            50,
            525,
            f"Rotten: {rotten}"
        )

        pdf.drawString(
            50,
            500,
            f"Mold: {mold}"
        )

        pdf.drawString(
            50,
            475,
            f"Damaged: {damaged}"
        )

        pdf.drawString(
            50,
            450,
            f"Undersized: {undersized}"
        )

        pdf.setFont(
            "Helvetica-Bold",
            14
        )

        pdf.drawString(
            50,
            410,
            "Individual Results"
        )

        pdf.setFont(
            "Helvetica",
            11
        )

        y = 385

        for i in range(total_onions):

            pdf.drawString(
                50,
                y,
                f"Onion {i + 1}: {statuses[i]} - {grades[i]}"
            )

            y -= 20

            if y < 50:

                pdf.showPage()

                pdf.setFont(
                    "Helvetica",
                    11
                )

                y = 800

        pdf.save()

        with open(
            pdf_path,
            "rb"
        ) as file:

            st.download_button(
                label="⬇️ Download Complete Quality Report",
                data=file,
                file_name="onion_ai_quality_report.pdf",
                mime="application/pdf"
            )

        st.success(
            "✅ AI quality inspection completed successfully!"
        )

st.markdown("""
<div class="final-credit">
    <div class="credit-small">Designed & Developed By</div>
    <div class="credit-name">Rishwik</div>
    <div class="credit-line"></div>
    <div class="credit-role">
        AI / ML · Computer Vision · Smart Agriculture
    </div>
</div>

<div class="footer">
    🧅 OnionAI · Intelligent Quality Assessment System
</div>
""", unsafe_allow_html=True)
