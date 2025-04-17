import streamlit as st
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from huggingface_hub import login
import torch
import numpy as np
import os
import logging
import matplotlib.pyplot as plt
import seaborn as sns
import mplcyberpunk

plt.style.use('cyberpunk')

from utils.cv_reader import read_resume_from_file, preprocess_text
from utils.github_reader import extract_github_links_from_text, collect_github_text
from utils.constants import (
    competency_list,
    profession_matrix,
    profession_names,
    recommendations,
)

# ─── Настройки страницы ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Анализ резюме по матрице Альянса ИИ",
    layout="wide",
    initial_sidebar_state="collapsed"
)
st.title("Анализ резюме по матрице Альянса ИИ")

# ─── Инициализация GitHub-текста ───────────────────────────────────────────────
if "github_text_raw" not in st.session_state:
    st.session_state["github_text_raw"] = ""

# ─── Логирование ────────────────────────────────────────────────────────────────
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/errors.log",
    level=logging.ERROR,
    format="%(asctime)s — %(levelname)s — %(message)s"
)

# ─── Загрузка модели ───────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    login(token=st.secrets["HUGGINGFACE_TOKEN"])
    repo_id = "KsyLight/resume-ai-competency-model"
    tokenizer = AutoTokenizer.from_pretrained(
        repo_id,
        token=st.secrets["HUGGINGFACE_TOKEN"]
    )
    model = AutoModelForSequenceClassification.from_pretrained(
        repo_id,
        token=st.secrets["HUGGINGFACE_TOKEN"]
    )
    model.eval()
    return tokenizer, model

# Инициализация модели
tokenizer, model = load_model()

# Предсказание компетенций с порогом
def predict_competencies(text: str):
    inputs = tokenizer(
        text,
        return_tensors="pt",
        padding=True,
        truncation=True,
        max_length=512
    )
    with torch.no_grad():
        outputs = model(**inputs)
    probs = torch.sigmoid(outputs.logits).squeeze().cpu().numpy()
    preds = (probs > 0.46269254347612143).astype(int)
    return preds, probs

# ─── Загрузка резюме ────────────────────────────────────────────────────────────
uploaded_file = st.file_uploader(
    "📤 Загрузите резюме (PDF, DOCX, TXT)",
    type=["pdf", "docx", "txt"]
)

if uploaded_file:
    # Сохранение во временный файл
    os.makedirs("temp", exist_ok=True)
    tmp_file_path = os.path.join("temp", uploaded_file.name)
    with open(tmp_file_path, "wb") as f:
        f.write(uploaded_file.read())

    try:
        # Извлечение текста резюме
        with st.spinner("⏳ Извлечение текста..."):
            base_text = read_resume_from_file(tmp_file_path)
            if not base_text:
                st.error("❌ Не удалось извлечь текст резюме.")
                st.stop()

            # Поиск GitHub-ссылок и сбор raw-текста
            gh_links = extract_github_links_from_text(base_text)
            st.session_state["gh_links"] = gh_links
            github_text_raw = ""
            if gh_links:
                st.markdown("🔗 **GitHub‑ссылки:**")
                for link in gh_links:
                    st.markdown(f"- [{link}]({link})")
                    try:
                        raw_url = link.replace(
                            'github.com', 'raw.githubusercontent.com'
                        ).replace('/blob/', '/')
                        github_text_raw += "\n" + collect_github_text(raw_url)
                    except Exception as e:
                        st.warning(f"⚠️ Ошибка при загрузке {link}")
                        logging.error(f"GitHub fetch error ({link}): {e}")
            else:
                st.info("GitHub‑ссылки не найдены.")

            # Сохранить текст для модели и объединить
            st.session_state["github_text_raw"] = github_text_raw
            full_text = preprocess_text(base_text + " " + github_text_raw)

        # Предсказание компетенций
        with st.spinner("🤖 Анализ компетенций..."):
            pred_vector, prob_vector = predict_competencies(full_text)

        # Создание вкладок
        tab1, tab2, tab3, tab4 = st.tabs([
            "Опрос", "Профессии", "Рекомендации", "Резюме"
        ])

        # ─── Таб 1: Опрос ────────────────────────────────────────────────────────────
        with tab1:
            st.subheader("Ваш уровень владения по компетенциям (0–3):")
            user_grades = []
            c1, c2 = st.columns(2)
            for i, comp in enumerate(competency_list):
                default_idx = 1 if pred_vector[i] else 0
                with c1 if i % 2 == 0 else c2:
                    grade = st.radio(
                        comp,
                        [0, 1, 2, 3],
                        index=default_idx,
                        horizontal=True,
                        key=f"grade_{i}"
                    )
                    user_grades.append(grade)
            st.session_state.user_grades = user_grades
            st.success("✅ Грейды сохранены! Перейдите во вкладку 'Профессии'")

        # ─── Таб 2: Профессии ───────────────────────────────────────────────────────
        with tab2:
            if "user_grades" not in st.session_state:
                st.warning("⚠️ Сначала заполните грейды во вкладке 'Опрос'")
                st.stop()

            user_vector = np.array(st.session_state.user_grades)
            if user_vector.shape[0] != profession_matrix.shape[0]:
                st.error("⚠️ Число компетенций не совпадает с размерностью матрицы.")
                st.stop()

            c1, c2 = st.columns(2)
            # Левый столбец: компетенции
            with c1:
                st.markdown("### Ваши компетенции и грейды:")
                st.markdown(
                    """
                    <div style='border:1px solid #ddd; padding:10px; border-radius:8px; margin-bottom:10px; width:60%; background:#1a1a1a;'>
                      <p style='margin:0; padding-left:12px; color:white; line-height:1.4em;'>
                        <strong style='color:#4caf50;'>🟩 — грейд 3</strong><br>
                        <strong style='color:#ffeb3b;'>🟨 — грейд 2</strong><br>
                        <strong style='color:#2196f3;'>🟦 — грейд 1</strong><br>
                        <strong style='color:#ffffff;'>⬜️ — грейд 0</strong>
                      </p>
                    </div>
                    """, unsafe_allow_html=True
                )
                for comp, grade in sorted(zip(competency_list, user_vector), key=lambda x: -x[1]):
                    emoji = {3: "🟩", 2: "🟨", 1: "🟦", 0: "⬜️"}[grade]
                    st.markdown(
                        f"<div style='margin-left:20px; color:white;'>{emoji} <strong>{comp}</strong> — грейд: <strong>{grade}</strong></div>",
                        unsafe_allow_html=True
                    )
            # Правый столбец: графики и описания
            with c2:
                # Относительное соответствие
                pct_list = []
                for idx, prof in enumerate(profession_names):
                    req = profession_matrix[:, idx]
                    total = np.count_nonzero(req)
                    matched = np.count_nonzero((user_vector >= req) & (req > 0))
                    pct_list.append((prof, matched / total * 100 if total else 0.0))
                pct_sorted = sorted(pct_list, key=lambda x: x[1], reverse=True)
                labels = [p for p, _ in pct_sorted]
                vals = [v for _, v in pct_sorted]
                cols = sns.color_palette("dark", len(labels))

                # Круговая
                fig1, ax1 = plt.subplots(figsize=(6, 6))
                fig1.patch.set_facecolor('#0d1117'); ax1.set_facecolor('#0d1117')
                wedges, txts, atxts = ax1.pie(
                    vals, labels=labels, autopct="%1.1f%%",
                    startangle=90, colors=cols,
                    wedgeprops={'edgecolor':'white','linewidth':0.8}
                )
                for t in txts + atxts:
                    t.set_color('white'); t.set_fontsize(10)
                ax1.axis('equal'); mplcyberpunk.add_glow_effects()
                st.markdown("### Относительное соответствие по профессиям")
                st.pyplot(fig1)

                # Столбчатая
                fig2, ax2 = plt.subplots(figsize=(8, 4))
                fig2.patch.set_facecolor('#0d1117'); ax2.set_facecolor('#0d1117')
                bars = ax2.barh(labels, vals, color=cols, edgecolor='white', linewidth=0.8)
                ax2.set_xlim(0, 100); ax2.invert_yaxis()
                ax2.set_xlabel("Процент соответствия", color='white')
                ax2.grid(axis='x', linestyle='--', alpha=0.3)
                for bar in bars:
                    w = bar.get_width()
                    ax2.text(w + 1, bar.get_y() + bar.get_height()/2, f"{w:.1f}%", va='center', color='white', fontsize=10)
                mplcyberpunk.add_glow_effects()
                st.markdown("### Абсолютное соответствие по профессиям")
                st.pyplot(fig2)

                # Таблица описаний
                st.markdown("### Описание профессий")
                descs = {
                    "Аналитик данных (Data scientist, ML engineer)":
                        "Специалист, который работает с данными компании, анализирует их и разрабатывает решения на основе ИИ. • Определяет метод ML и адаптирует его к задаче • Разрабатывает признаки • Строит пайплайн • Ведёт документацию",
                    "Менеджер в ИИ (Manager in AI)":
                        "Руководит проектом, контролирует сроки и ресурсы. Отвечает за внедрение решения в продуктив, может участвовать в документации и анализе фидбека.",
                    "Технический аналитик в ИИ (Technical analyst in AI)":
                        "Связывает заказчика и ML-команду. Анализирует бизнес-процессы, готовит ТЗ и участвует в оценке реализуемости и тестировании.",
                    "Инженер данных (Data engineer)":
                        "Готовит данные: собирает, очищает, передаёт. Поддерживает хранилища и пайплайны данных."
                }
                name_map = {
                    "Аналитик данных": "Аналитик данных (Data scientist, ML engineer)",
                    "Менеджер в ИИ": "Менеджер в ИИ (Manager in AI)",
                    "Технический аналитик в ИИ": "Технический аналитик в ИИ (Technical analyst in AI)",
                    "Инженер данных": "Инженер данных (Data engineer)"
                }
                rows_html = ""
                for prof, _ in pct_sorted:
                    full = name_map.get(prof, prof)
                    txt = descs.get(full, "—")
                    parts = txt.split(" • ")
                    if len(parts) > 1:
                        intro = parts[0].strip()
                        bullets = parts[1:]
                        html = f"<p style='margin:0 0 4px 0;'>{intro}</p><ul style='margin:0;padding-left:20px;'>"
                        for b in bullets:
                            html += f"<li style='margin-bottom:2px;'>{b.strip()}</li>"
                        html += "</ul>"
                    else:
                        html = f"<p style='margin:0;'>{txt}</p>"
                    rows_html += f"<tr><td style='border:1px solid #444;padding:8px;color:white;vertical-align:top;'>{full}</td><td style='border:1px solid #444;padding:8px;color:white;vertical-align:top;'>{html}</td></tr>"
                table_html = f"<table style='width:100%;border-collapse:collapse;'><thead><tr style='background-color:#1f1f1f;'><th style='border:1px solid #555;padding:8px;color:white;text-align:left;'>Профессия</th><th style='border:1px solid #555;padding:8px;color:white;text-align:left;'>Описание</th></tr></thead><tbody>{rows_html}</tbody></table>"
                st.markdown(table_html, unsafe_allow_html=True)

        # ─── Таб 3: Рекомендации ─────────────────────────────────────────────────────
        with tab3:
            st.subheader("Рекомендации по слабым компетенциям для выбранной профессии")
            prof_choice = st.selectbox("Выберите профессию", profession_names)
            idx = profession_names.index(prof_choice)
            req_vec = profession_matrix[:, idx]
            user_vec = np.array(st.session_state.user_grades)
            sort_asc = st.checkbox("Сортировать по грейду (меньше → больше)", value=True)
            weak_idxs = [i for i, (u, r) in enumerate(zip(user_vec, req_vec)) if u < r]
            weak_sorted = sorted(weak_idxs, key=lambda i: user_vec[i], reverse=not sort_asc)
            emoji_map = {3: "🟩", 2: "🟨", 1: "🟦", 0: "⬜️"}
            if not recommendations:
                st.info("Словарь рекомендаций пуст. Добавьте данные в utils/constants.py")
            elif weak_sorted:
                for i in weak_sorted:
                    comp = competency_list[i]
                    g = user_vec[i]
                    r = req_vec[i]
                    emo = emoji_map.get(g, "⬜️")
                    color = "#4caf50" if g == 3 else "#ffeb3b" if g == 2 else "#2196f3" if g == 1 else "#ffffff"
                    st.markdown(f"<span style='color:{color};'>{emo} <strong>{comp}</strong></span>: грейд {g}, требуется {r}", unsafe_allow_html=True)
                    recs = recommendations.get(comp, [])
                    if recs:
                        for link in recs:
                            st.markdown(f"- [{link}]({link})")
                    else:
                        st.markdown("- Рекомендаций нет для этой компетенции")
            else:
                st.success("Все компетенции соответствуют требованиям!")

        # ─── Таб 4: Резюме ────────────────────────────────────────────────────────────
        with tab4:
            st.markdown("### Извлечённый текст резюме")
            with st.expander("📝 Текст из файла резюме", expanded=True):
                st.text(base_text)
            with st.expander("🧑‍💻 Текст для модели из GitHub", expanded=True):
                gh_text = st.session_state.get("github_text_raw", "")
                if gh_text.strip():
                    st.text_area("GitHub-текст", gh_text, height=300)
                else:
                    st.info("Текст для модели из GitHub отсутствует.")

    except Exception as e:
        st.error("🚫 Не удалось обработать файл.")
        logging.error(f"Общая ошибка: {e}", exc_info=True)
    finally:
        try:
            os.remove(tmp_file_path)
        except OSError:
            pass