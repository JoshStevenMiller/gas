import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import smtplib
from email.message import EmailMessage
import os

# ---- PDF GENERATOR FUNCTION ----
def generate_pdf(filename, email):
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d %H:%M:%S")

    c = canvas.Canvas(filename, pagesize=letter)
    y = 750
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "Goal Attainment Scaling (GAS) Form")
    y -= 25
    c.setFont("Helvetica", 12)
    c.drawString(50, y, f"Date: {date_str}")
    y -= 20
    if email:
        c.drawString(50, y, f"User Email: {email}")
        y -= 20

    for i in range(5):
        goal = goal_vars[i].get()
        weight = weight_vars[i].get()
        score = score_vars[i].get()
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, f"Goal {i + 1}:")
        y -= 15
        c.setFont("Helvetica", 11)
        c.drawString(70, y, f"Description: {goal}")
        y -= 15
        c.drawString(70, y, f"Weight: {weight}")
        y -= 15
        c.drawString(70, y, f"Score: {score}")
        y -= 20

    total = calculate_score(show_popup=False)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, f"Total Weighted Score: {total:.2f}")
    c.save()
    return filename

# ---- EMAIL FUNCTION ----
def email_pdf():
    recipient = email_var.get()
    if not recipient:
        messagebox.showerror("Missing Email", "Please enter your email address.")
        return

    filename = f"GAS_Form_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    generate_pdf(filename, recipient)

    try:
        # SETUP: replace with your own email and app password
        sender_email = "joshstevenmiller@gmail.com"
        sender_password = "cyku ojwk dxug uctm"  # not your Gmail password!

        msg = EmailMessage()
        msg["Subject"] = "Your Goal Attainment Scaling (GAS) Form"
        msg["From"] = sender_email
        msg["To"] = recipient
        msg.set_content("Attached is your completed GAS form.")

        with open(filename, "rb") as f:
            file_data = f.read()
            msg.add_attachment(file_data, maintype="application", subtype="pdf", filename=filename)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)

        messagebox.showinfo("✅ Sent", f"PDF sent to {recipient}")
        os.remove(filename)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to send email:\n{e}")

# ---- SCORE CALCULATION ----
def calculate_score(show_popup=True):
    try:
        total = 0.0
        for i in range(5):
            weight_str = weight_vars[i].get().strip()
            score_str = score_vars[i].get().strip()

            # Skip if either is empty
            if not weight_str or not score_str:
                continue

            weight = float(weight_str)
            score = int(score_str)
            total += weight * score

        if show_popup:
            messagebox.showinfo("🎉 Result", f"Your total weighted GAS score is: {total:.2f}")
        return total

    except ValueError:
        if show_popup:
            messagebox.showerror("Oops!", "Please enter valid weights and select all scores.")
        return 0


# ---- GUI START ----
root = tk.Tk()
root.title("Goal Attainment Scaling (GAS) Tool")
root.geometry("1200x700")
root.configure(bg="#f0f8ff")
root.resizable(False, False)

goal_vars = [tk.StringVar() for _ in range(5)]
weight_vars = [tk.StringVar() for _ in range(5)]
score_vars = [tk.StringVar() for _ in range(5)]
score_options = ["-2", "-1", "0", "1", "2"]
email_var = tk.StringVar()

tk.Label(root, text="🎯 Goal Attainment Scaling", font=("Comic Sans MS", 20, "bold"), bg="#f0f8ff").pack(pady=20)
frame = tk.Frame(root, bg="#f0f8ff")
frame.pack(padx=40)

tk.Label(frame, text="Goal", font=("Comic Sans MS", 12, "bold"), width=50, bg="#f0f8ff").grid(row=0, column=0)
tk.Label(frame, text="Weight (.2 to 1)", font=("Comic Sans MS", 12, "bold"), width=20, bg="#f0f8ff").grid(row=0, column=1)
tk.Label(frame, text="Score", font=("Comic Sans MS", 12, "bold"), width=20, bg="#f0f8ff").grid(row=0, column=2)

for i in range(5):
    tk.Entry(frame, textvariable=goal_vars[i], width=50).grid(row=i+1, column=0, padx=5, pady=5)
    tk.Entry(frame, textvariable=weight_vars[i], width=20).grid(row=i+1, column=1, padx=5)
    ttk.Combobox(frame, textvariable=score_vars[i], values=score_options, width=18, state="readonly").grid(row=i+1, column=2, padx=5)

email_frame = tk.Frame(root, bg="#f0f8ff")
email_frame.pack(pady=15)
tk.Label(email_frame, text="Your Email:", font=("Comic Sans MS", 12), bg="#f0f8ff").pack(side="left", padx=5)
tk.Entry(email_frame, textvariable=email_var, font=("Comic Sans MS", 11), width=40).pack(side="left")

btn_frame = tk.Frame(root, bg="#f0f8ff")
btn_frame.pack(pady=30)

tk.Button(btn_frame, text="✨ Calculate Score", command=calculate_score,
          font=("Comic Sans MS", 12, "bold"), bg="#90ee90", padx=20, pady=10).grid(row=0, column=0, padx=10)

tk.Button(btn_frame, text="💾 Save to PDF", command=lambda: generate_pdf("GAS_Form_Output.pdf", email_var.get()),
          font=("Comic Sans MS", 12, "bold"), bg="#add8e6", padx=20, pady=10).grid(row=0, column=1, padx=10)

tk.Button(btn_frame, text="📧 Email PDF", command=email_pdf,
          font=("Comic Sans MS", 12, "bold"), bg="#ffc0cb", padx=20, pady=10).grid(row=0, column=2, padx=10)

root.mainloop()
