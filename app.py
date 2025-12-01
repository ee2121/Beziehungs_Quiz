import streamlit as st
import os
from questions import quiz_data

def main():
    st.set_page_config(page_title="Beziehungs-Quizduell", page_icon="assets/Quizduell_icon.png")

    # Initialize session state
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'game_over' not in st.session_state:
        st.session_state.game_over = False
    if 'last_answer_correct' not in st.session_state:
        st.session_state.last_answer_correct = None # None, True, False
    if 'game_started' not in st.session_state:
        st.session_state.game_started = False
    if 'feedback' not in st.session_state:
        st.session_state.feedback = None # {"type": "success"|"error", "message": "..."}

    # Custom CSS for styling
    st.markdown("""
        <style>
        .stButton button {
            width: 100%;
            height: auto !important;
            min-height: 80px;
            font-size: 16px;
            margin-bottom: 10px;
            white-space: normal !important;
            word-wrap: break-word;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 10px;
        }
        .question-text {
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 20px;
            text-align: center;
        }
        .score-board {
            font-size: 18px;
            margin-bottom: 20px;
            padding: 10px;
            background-color: #6aa84f;
            border-radius: 5px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Start Screen
    if not st.session_state.game_started:
        st.title("Quizduell")
        st.text_area("Nachricht", placeholder="Hallo Hannah, ich habe dir ein kleines Quiz gebaut, weil du so gerne Quizduell spielst. Löse die Aufgaben und du erhältst ein Gutschein :)", height=150)
        if st.button("Starten"):
            st.session_state.game_started = True
            st.rerun()
        return

    st.title("Quizduell")

    # Game Over Screen
    if st.session_state.game_over:
        st.balloons()
        st.success(f"Spiel vorbei! Du hast {st.session_state.score} von {len(quiz_data)} Punkten erreicht. Damit hast du dir einen Gutschein verdient :) Suche dir eine Stadt aus, die du schon immer besuchen wolltest und ich fahre mit dir dort hin! Ich liebe dich! <3")
        
        if st.button("Neues Spiel starten"):
            st.session_state.current_question = 0
            st.session_state.score = 0
            st.session_state.game_over = False
            st.session_state.last_answer_correct = None
            st.session_state.game_started = False
            st.session_state.feedback = None
            st.rerun()
        return

    # Get current question data
    question_index = st.session_state.current_question
    question_data = quiz_data[question_index]

    # Progress bar
    progress = (question_index) / len(quiz_data)
    st.progress(progress)
    st.write(f"Frage {question_index + 1} von {len(quiz_data)}")

    # Construct absolute path to assets to ensure it works
    current_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(current_dir, question_data["image_path"])
    
    if os.path.exists(image_path):
        # Create a central column for all content to ensure alignment
        col1, content_col, col3 = st.columns([1, 2, 1])
        
        with content_col:
            st.image(image_path, use_container_width=True)
            
            # Display Question inside the same column
            st.markdown(f"<div class='question-text'>{question_data['question']}</div>", unsafe_allow_html=True)

            # Feedback Display
            if st.session_state.feedback:
                if st.session_state.feedback["type"] == "success":
                    st.success(st.session_state.feedback["message"])
                else:
                    st.error(st.session_state.feedback["message"])

            # Buttons in a 2x2 grid inside the content column
            options = question_data["options"]
            btn_col1, btn_col2 = st.columns(2)

            def check_answer(selected_option):
                correct = selected_option == question_data["correct_answer"]
                if correct:
                    st.session_state.score += 1
                    st.session_state.feedback = {"type": "success", "message": "Richtig! 🎉"}
                    
                    # Move to next question
                    if st.session_state.current_question < len(quiz_data) - 1:
                        st.session_state.current_question += 1
                        st.session_state.feedback = None # Clear it for the next question to avoid confusion
                        st.toast("Richtig! 🎉", icon="✅") 
                    else:
                        st.session_state.game_over = True
                else:
                    st.session_state.feedback = {"type": "error", "message": "Falsch! Versuch es nochmal."}
                
                st.rerun()

            with btn_col1:
                if st.button(options[0], use_container_width=True):
                    check_answer(options[0])
                if st.button(options[2], use_container_width=True):
                    check_answer(options[2])

            with btn_col2:
                if st.button(options[1], use_container_width=True):
                    check_answer(options[1])
                if st.button(options[3], use_container_width=True):
                    check_answer(options[3])
    else:
        st.error(f"Bild nicht gefunden: {question_data['image_path']}")

    # Score display
    st.markdown(f"<div class='score-board'>Aktueller Punktestand: {st.session_state.score}</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
