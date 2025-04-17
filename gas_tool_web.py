import streamlit as st
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import tempfile

st.set_page_config(page_title="Goal Attainment Scaling (GAS) Tool", layout="centered")

st.title("🎯 Goal Attainment Scaling (GAS)")
st.markdown("Enter your goals, assign each a weight (0.2 to 1.0), and choose a score (-2 to +2). You'll see your score below and can also download a PDF.")

score_options = [-2, -1, 0, 1, 2]
num_goals = 5

goals = []
weights = []
scores = []

with st.form("gas_form"):
    email = st.text_input("Your email address (optional, included in PDF only):")
    for i in range(num_goals):
        st.markdown(f"### Goal {i+1}")
        goal = st.text_input(f"Goal description {i+1}", key=f"goal_{i}")
        weight = st.number_input(f"Weight (0.2–1.0)", min_value=0.2, max_value=1.0, step=0.1, key=f"weight_{i}")
        score = st.selectbox(f"Score (-2 to +2)", score_options, key=f"score_{i}")
        goals.append(goal)
        weights.append(weight)
        scores.append(score)

    submitted = st.form_submit_button("✨ Calculate Score")

# Show score result immediately
if submitted:
    total_score = sum(float(w) * int(s) for w, s in zip(weights, scores) if w and s is not None)
    st.success(f"🎯 Your Total Weighted GAS Score is: **{total_score:.2f}**")

    # Generate downloadable PDF
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        filename = tmp.name
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d %H:%M:%S")

        c = canvas.Canvas(filename, pagesize=letter)
        width, height = letter
        y = height - 50

        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, y, "Goal Attainment Scaling (GAS) Form")
        y -= 25
        c.setFont("Helvetica", 12)
        c.drawString(50, y, f"Date: {date_str}")
        y -= 20

        if email:
            c.drawString(50, y, f"Email: {email}")
            y -= 20

        for i in range(num_goals):
            if goals[i].strip():
                y -= 20
                c.setFont("Helvetica-Bold", 12)
                c.drawString(50, y, f"Goal {i+1}:")
                y -= 15
                c.setFont("Helvetica", 11)
                c.drawString(70, y, f"Description: {goals[i]}")
                y -= 15
                c.drawString(70, y, f"Weight: {weights[i]}")
                y -= 15
                c.drawString(70, y, f"Score: {scores[i]}")

        y -= 25
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, f"Total Weighted Score: {total_score:.2f}")
        c.save()

        with open(filename, "rb") as f:
            st.download_button(
                label="📄 Download GAS Form as PDF",
                data=f.read(),
                file_name="GAS_Form.pdf",
                mime="application/pdf"
            )
