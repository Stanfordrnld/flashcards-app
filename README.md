# 📚 Générateur de Flashcards depuis Excel

Cette application permet de transformer un fichier **Excel** en un PDF de flashcards.
- La **colonne B** de votre fichier correspond aux **questions**.
- La **colonne C** correspond aux **réponses**.

L'application est construite avec **Streamlit** et déployable facilement sur **Streamlit Community Cloud**.

---

## 🚀 Utilisation locale

### 1. Cloner le projet
```bash
git clone https://github.com/votre-pseudo/flashcards-app.git
cd flashcards-app
```

### 2. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 3. Lancer l'application
```bash
streamlit run app.py
```

Puis ouvrir le lien affiché (ex: `http://localhost:8501`).

---

## 🌐 Déploiement sur Streamlit Cloud

1. Créez un dépôt GitHub avec :
   - `app.py` (le code de l'application)
   - `requirements.txt`

2. Dans `requirements.txt`, ajoutez :
   ```
   streamlit
   pandas
   openpyxl
   reportlab
   ```

3. Allez sur 👉 [https://share.streamlit.io](https://share.streamlit.io)
4. Connectez votre compte GitHub.
5. Créez une nouvelle app : choisissez votre repo → branche `main` → fichier `app.py`.
6. Cliquez sur **Deploy** 🎉

Votre app sera accessible à une URL comme :
```
https://votre-pseudo-flashcards-app.streamlit.app
```

---

## 📂 Exemple de fichier Excel attendu

| A   | B (Question)        | C (Réponse)     |
|-----|---------------------|-----------------|
| 1   | Capital de la France | Paris          |
| 2   | 2 + 2                | 4              |

---

## ✨ Fonctionnalités
- Upload d’un fichier Excel `.xlsx`
- Génération automatique d’un PDF de flashcards
- Téléchargement direct depuis l’application

---

👨‍💻 Développé avec ❤️ en Python & Streamlit
