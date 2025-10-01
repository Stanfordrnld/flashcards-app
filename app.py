import pandas as pd
import streamlit as st
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Spacer, Table, TableStyle


def excel_to_flashcards(excel_file):
    df = pd.read_excel(excel_file, usecols=[1, 2], header=0)
    df.columns = ["Question", "Réponse"]

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    story = []

    for _, row in df.iterrows():
        question = row["Question"]
        reponse = row["Réponse"]

        card_data = [[f"Q: {question}"], [f"R: {reponse}"]]
        table = Table(card_data, colWidths=[450])
        table.setStyle(TableStyle([
            ('BOX', (0, 0), (-1, -1), 2, colors.black),
            ('INNERGRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
        ]))

        story.append(table)
        story.append(Spacer(1, 20))

    doc.build(story)
    buffer.seek(0)
    return buffer


# Application Streamlit
st.title("📚 Générateur de Flashcards depuis Excel")
st.write("Charge ton fichier Excel (Colonne B = Questions, Colonne C = Réponses)")

uploaded_file = st.file_uploader("Choisis un fichier Excel", type=["xlsx"])

if uploaded_file:
    if st.button("Générer le PDF"):
        pdf_buffer = excel_to_flashcards(uploaded_file)
        st.download_button(
            label="📥 Télécharger le PDF des Flashcards",
            data=pdf_buffer,
            file_name="flashcards.pdf",
            mime="application/pdf"
        )
