import pandas as pd
import streamlit as st
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Spacer, Table, TableStyle, Paragraph
from reportlab.lib.styles import ParagraphStyle

# === Configuration par défaut ===
DEFAULT_COLS = 3
DEFAULT_ROWS = 3
DEFAULT_FONT_SIZE = 12  # texte plus petit
CARD_TITLE = "Quizz Fonction publique territoriale"

def generate_flashcards_pdf(excel_file, cols=DEFAULT_COLS, rows=DEFAULT_ROWS, font_size=DEFAULT_FONT_SIZE):
    df = pd.read_excel(excel_file, usecols=[1,2], header=0)
    df.columns = ["Question", "Réponse"]

    page_w, page_h = A4
    margin = 36
    h_gap = 12
    v_gap = 12
    usable_w = page_w - 2*margin
    usable_h = page_h - 2*margin

    # Cartes carrées
    card_size = min((usable_w - (cols-1)*h_gap)/cols, (usable_h - (rows-1)*v_gap)/rows)

    style_center = ParagraphStyle(
        name="center", alignment=1, fontSize=font_size, leading=font_size+2
    )

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, leftMargin=margin, rightMargin=margin, topMargin=margin, bottomMargin=margin)
    story = []

    # Préparer le contenu des cartes
    texts = []
    for _, row in df.iterrows():
        q = "" if pd.isna(row["Question"]) else str(row["Question"])
        r = "" if pd.isna(row["Réponse"]) else str(row["Réponse"])
        txt = f"<b>{CARD_TITLE}</b><br/><br/><b>Q:</b> {q}<br/><b>R:</b> {r}"
        texts.append(txt)

    # Créer des pages avec une grille de cartes
    per_page = cols*rows
    pages = [texts[i:i+per_page] for i in range(0,len(texts),per_page)]

    for page in pages:
        page_cells = []
        idx = 0
        for r_idx in range(rows):
            row_cells = []
            for c_idx in range(cols):
                if idx < len(page):
                    p = Paragraph(page[idx], style_center)
                    row_cells.append(p)
                else:
                    row_cells.append("")  # cellule vide si pas assez de cartes
                idx += 1
            page_cells.append(row_cells)
        t = Table(page_cells, colWidths=[card_size]*cols, rowHeights=[card_size]*rows)
        t.setStyle(TableStyle([
            ("GRID",(0,0),(-1,-1),0.8,colors.grey),
            ("BOX",(0,0),(-1,-1),1,colors.black),
            ("ALIGN",(0,0),(-1,-1),"CENTER"),
            ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
            ("LEFTPADDING",(0,0),(-1,-1),6),
            ("RIGHTPADDING",(0,0),(-1,-1),6),
            ("TOPPADDING",(0,0),(-1,-1),6),
            ("BOTTOMPADDING",(0,0),(-1,-1),6)
        ]))
        story.append(t)
        story.append(Spacer(1,10))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()


# ---------------- Streamlit UI ----------------
st.set_page_config(page_title="Flashcards Carrées", layout="centered")
st.title("📚 Générateur de Flashcards Carrées")
st.write("Upload un fichier Excel (Col B = Questions, Col C = Réponses) pour générer des cartes carrées imprimables.")

st.sidebar.header("Mise en page des cartes")
cols = st.sidebar.number_input("Colonnes par page", min_value=1, max_value=4, value=DEFAULT_COLS)
rows = st.sidebar.number_input("Lignes par page", min_value=1, max_value=6, value=DEFAULT_ROWS)
font_size = st.sidebar.slider("Taille de police", min_value=8, max_value=16, value=DEFAULT_FONT_SIZE)

uploaded_file = st.file_uploader("Choisis un fichier Excel (.xlsx)", type=["xlsx"])

if uploaded_file:
    if st.button("Générer le PDF"):
        try:
            pdf_bytes = generate_flashcards_pdf(uploaded_file, cols=int(cols), rows=int(rows), font_size=int(font_size))
            st.success("✅ PDF généré ! Les cartes sont carrées et prêtes à imprimer.")
            st.download_button(
                label="📥 Télécharger le PDF",
                data=pdf_bytes,
                file_name="flashcards_carre.pdf",
                mime="application/pdf",
            )
        except Exception as e:
            st.error(f"Erreur : {e}")
