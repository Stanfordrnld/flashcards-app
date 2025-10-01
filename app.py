import pandas as pd
import streamlit as st
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

CARD_WIDTH = 200   # largeur d’une carte
CARD_HEIGHT = 120  # hauteur d’une carte

def excel_to_flashcards(excel_file):
    df = pd.read_excel(excel_file, usecols=[1, 2], header=0)
    df.columns = ["Question", "Réponse"]

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    story = []

    cards = []

    # On crée une carte pour chaque question et chaque réponse
    for _, row in df.iterrows():
        q = row["Question"]
        r = row["Réponse"]

        # Carte Question
        card_q = Table([[q]], colWidths=[CARD_WIDTH], rowHeights=[CARD_HEIGHT])
        card_q.setStyle(TableStyle([
            ("BOX", (0,0), (-1,-1), 2, colors.black),
            ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
            ("ALIGN", (0,0), (-1,-1), "CENTER"),
            ("FONTSIZE", (0,0), (-1,-1), 14),
        ]))
        cards.append(card_q)

        # Carte Réponse
        card_r = Table([[r]], colWidths=[CARD_WIDTH], rowHeights=[CARD_HEIGHT])
        card_r.setStyle(TableStyle([
            ("BOX", (0,0), (-1,-1), 2, colors.black),
            ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
            ("ALIGN", (0,0), (-1,-1), "CENTER"),
            ("FONTSIZE", (0,0), (-1,-1), 14),
        ]))
        cards.append(card_r)

    # Organisation des cartes en grille (2 colonnes)
    rows = [cards[i:i+2] for i in range(0, len(cards), 2)]
    for row in rows:
        story.append(Table([row], colWidths=[CARD_WIDTH]*len(row), rowHeights=[CARD_HEIGHT]))
        story.append(Table([[""]], colWidths=[0], rowHeights=[20]))  # espace vertical entre les lignes

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

            file_name="flashcards.pdf",
            mime="application/pdf"
        )
