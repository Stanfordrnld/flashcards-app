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
DEFAULT_FONT_SIZE = 12
CARD_TITLE = "Quizz Fonction publique territoriale"

def generate_flashcards_pdf_recto_verso(excel_file, cols=DEFAULT_COLS, rows=DEFAULT_ROWS, font_size=DEFAULT_FONT_SIZE):
    df = pd.read_excel(excel_file, usecols=[1,2], header=0)
    df.columns = ["Question", "Réponse"]

    page_w, page_h = A4
    margin = 36
    h_gap = 12
    v_gap = 12
    usable_w = page_w - 2*margin
    usable_h = page_h - 2*margin
    card_size = min((usable_w - (cols-1)*h_gap)/cols, (usable_h - (rows-1)*v_gap)/rows)

    style_center = ParagraphStyle(
        name="center", alignment=1, fontSize=font_size, leading=font_size+2
    )

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, leftMargin=margin, rightMargin=margin, topMargin=margin, bottomMargin=margin)
    story = []

    # Fonction pour créer une page avec texte répété dans toutes les cartes
    def create_page(texts):
        page_cells=[]
        idx=0
        for r_idx in range(rows):
            row_cells=[]
            for c_idx in range(cols):
                if idx < len(texts):
                    p = Paragraph(texts[idx], style_center)
                    row_cells.append(p)
                else:
                    row_cells.append("")
                idx+=1
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

    # Préparer toutes les cartes : question+réponse
    texts_qr = [f"<b>Q:</b> {row['Question']}<br/><b>R:</b> {row['Réponse']}" for _, row in df.iterrows()]

    per_page = cols*rows
    # Créer pages par paires recto/verso
    pages = [texts_qr[i:i+per_page] for i in range(0,len(texts_qr), per_page)]

    for page_cards in pages:
        # Recto : toutes les cartes identiques
        recto_texts = [f"<b>{CARD_TITLE}</b>"]*len(page_cards)
        create_page(recto_texts)

        # Verso : questions + réponses correspondantes
        create_page(page_cards)

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()

# ---------------- Streamlit UI ----------------
st.set_page_config(page_title="Flashcards Recto-Verso", layout="centered")
st.title("📚 Générateur de Flashcards Recto-Verso")
st.write("Upload un fichier Excel (Col B = Questions, Col C = Réponses) pour générer des cartes carrées recto-verso.")

st.sidebar.header("Mise en page des cartes")
cols = st.sidebar.number_input("Colonnes par page", min_value=1,max_value=4,value=DEFAULT_COLS)
rows = st.sidebar.number_input("Lignes par page", min_value=1,max_value=6,value=DEFAULT_ROWS)
font_size = st.sidebar.slider("Taille de police", min_value=8,max_value=16,value=DEFAULT_FONT_SIZE)

uploaded_file = st.file_uploader("Choisis un fichier Excel (.xlsx)", type=["xlsx"])

if uploaded_file:
    if st.button("Générer le PDF"):
        try:
            pdf_bytes = generate_flashcards_pdf_recto_verso(uploaded_file, cols=int(cols), rows=int(rows), font_size=int(font_size))
            st.success("✅ PDF généré ! Les cartes sont prêtes à imprimer recto-verso.")
            st.download_button(
                label="📥 Télécharger le PDF",
                data=pdf_bytes,
                file_name="flashcards_recto_verso.pdf",
                mime="application/pdf",
            )
        except Exception as e:
            st.error(f"Erreur : {e}")
