import streamlit as st
import requests
import pandas as pd

BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="AI Employee Management System",
    page_icon="🤖",
    layout="wide"
)

# ---------------- SIDEBAR ---------------- #

with st.sidebar:

    st.title("🤖 AI-Powered HR Assistant")
    st.caption(
    "Employee Analytics + HR Policy Intelligence + RAG"
    )
    
    menu = st.radio(
        "Navigation",
        [
            "Dashboard",
            "Employees",
            "Add Employee",
            "Update Employee",
            "Delete Employee",
            "HR Policy Assistant",
            "HR Analytics Assistant",
            "Architecture"
        ]
    )

    st.markdown("---")

    st.success("🟢 Backend Running")

    st.info("LLM : Groq Llama 3.3")
    st.info("Database : PostgreSQL")
    st.info("Vector DB : Chroma")
    st.info("Cache : Redis (Optional)")

# ---------------- TITLE ---------------- #

st.title("🤖 AI-Powered HR Assistant")

st.caption(
    "Employee Analytics • HR Policy Intelligence • RAG"
)
# ---------------- DASHBOARD ---------------- #

if menu == "Dashboard":

    st.header("📊 Dashboard")

    try:

        response = requests.get(
            f"{BASE_URL}/employee"
        )

        employees = response.json()

        if employees:

            df = pd.DataFrame(employees)

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric(
                    "Employees",
                    len(df)
                )

            with col2:
                st.metric(
                    "Average Salary",
                    f"₹{int(df['salary'].mean())}"
                )

            with col3:
                st.metric(
                    "Highest Salary",
                    f"₹{int(df['salary'].max())}"
                )

            with col4:
                st.metric(
                    "Cities",
                    df["city"].nunique()
                )
            

            st.markdown("---")

            st.subheader("Employee Data")

            st.dataframe(
                df,
                use_container_width=True
            )

            st.subheader(
                "Salary Distribution"
            )

            st.bar_chart(
                df.set_index("name")["salary"]
            )

        else:
            st.warning(
                "No Employees Found"
            )

    except Exception as e:
        st.error(
            f"Backend Error: {e}"
        )

# ---------------- EMPLOYEES ---------------- #

elif menu == "Employees":

    st.header("👨‍💼 Employees")

    try:

        response = requests.get(
            f"{BASE_URL}/employee"
        )

        data = response.json()

        if data:

            search = st.text_input(
                "🔍 Search Employee"
            )

            if search:

                data = [
                    emp for emp in data
                    if search.lower()
                    in emp["name"].lower()
                ]

            df = pd.DataFrame(data)

            st.dataframe(
                df,
                use_container_width=True
            )

            if not df.empty:

                st.subheader(
                    "Salary Analysis"
                )

                st.bar_chart(
                    df.set_index("name")["salary"]
                )

        else:
            st.warning(
                "No Employees Found"
            )

    except Exception as e:
        st.error(str(e))

# ---------------- ADD EMPLOYEE ---------------- #

elif menu == "Add Employee":

    st.header("➕ Add Employee")

    with st.form(
        "employee_form"
    ):

        name = st.text_input(
            "Name"
        )

        age = st.number_input(
            "Age",
            min_value=18,
            max_value=100
        )

        salary = st.number_input(
            "Salary",
            min_value=0
        )

        city = st.text_input(
            "City"
        )

        gender = st.selectbox(
            "Gender",
            [
                "male",
                "female"
            ]
        )

        submit = st.form_submit_button(
            "Create Employee"
        )

        if submit:

            payload = {
                "name": name,
                "age": age,
                "salary": salary,
                "city": city,
                "gender": gender
            }

            response = requests.post(
                f"{BASE_URL}/employee",
                json=payload
            )

            if response.status_code == 200:

                st.success(
                    "Employee Created Successfully"
                )

            else:

                st.error(
                    response.text
                )

# ---------------- UPDATE EMPLOYEE ---------------- #

elif menu == "Update Employee":

    st.header("✏️ Update Employee")

    emp_id = st.number_input(
        "Employee ID",
        min_value=1
    )

    name = st.text_input(
        "New Name"
    )

    age = st.number_input(
        "New Age",
        min_value=0
    )

    salary = st.number_input(
        "New Salary",
        min_value=0
    )

    city = st.text_input(
        "New City"
    )

    gender = st.selectbox(
        "New Gender",
        [
            "",
            "male",
            "female"
        ]
    )

    if st.button(
        "Update Employee"
    ):

        payload = {}

        if name:
            payload["name"] = name

        if age:
            payload["age"] = age

        if salary:
            payload["salary"] = salary

        if city:
            payload["city"] = city

        if gender:
            payload["gender"] = gender

        response = requests.put(
            f"{BASE_URL}/employee/{emp_id}",
            json=payload
        )

        st.success(
            response.json()
        )

# ---------------- DELETE EMPLOYEE ---------------- #

elif menu == "Delete Employee":

    st.header("🗑 Delete Employee")

    emp_id = st.number_input(
        "Employee ID",
        min_value=1
    )

    if st.button("Delete"):

        response = requests.delete(
            f"{BASE_URL}/employee/{emp_id}"
        )

        st.success(
            response.json()
        )

# ---------------- AI CHAT ---------------- #

elif menu == "HR Policy Assistant":

    st.header(
        "📚 RAG Document Chat"
    )

    st.markdown("""
### Example Questions

• What is the leave policy?

• What is the notice period?

• What is the work from home policy?

• What are office timings?

• What is maternity leave policy?

• What is employee code of conduct?
""")

    if "rag_messages" not in st.session_state:
        st.session_state.rag_messages = []

    if st.button(
        "🗑 Clear Chat"
    ):
        st.session_state.rag_messages = []
        st.rerun()

    for msg in st.session_state.rag_messages:

        with st.chat_message(
            msg["role"]
        ):
            st.write(
                msg["content"]
            )

    question = st.chat_input(
        "Ask question from uploaded document..."
    )

    if question:

        st.session_state.rag_messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.chat_message(
            "user"
        ):
            st.write(question)

        try:

            with st.spinner(
                "Thinking..."
            ):

                response = requests.post(
                    f"{BASE_URL}/chat",
                    json={
                        "question": question
                    }
                )

            try:

                answer = response.json().get(
                    "answer",
                    response.text
                )

            except:

                answer = response.text

            with st.chat_message(
                "assistant"
            ):
                st.write(answer)

            st.session_state.rag_messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )

        except Exception as e:

            st.error(
                f"Error: {e}"
            )

# ---------------- EMPLOYEE CHAT ---------------- #

elif menu == "HR Analytics Assistant":

    st.header(
        "HR Analytics Assistant"
    )

    st.markdown("""
### Example Questions

• Who has highest salary?

• Show all employees from Jaipur

• Average salary?

• Female employees?

• Employee count?

    • Salary insights?
    """)

    if "employee_messages" not in st.session_state:
        st.session_state.employee_messages = []

    if st.button(
        "🗑 Clear Employee Chat"
    ):
        st.session_state.employee_messages = []
        st.rerun()

    for msg in st.session_state.employee_messages:

        with st.chat_message(
            msg["role"]
        ):
            st.write(
                msg["content"]
            )

    question = st.chat_input(
        "Ask about employees..."
    )

    if question:

        st.session_state.employee_messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.chat_message(
            "user"
        ):
            st.write(question)

        try:

            with st.spinner(
                "Thinking..."
            ):

                response = requests.post(
                    f"{BASE_URL}/employee-chat",
                    json={
                        "question": question
                    }
                )

            answer = response.json().get(
                "answer",
                "No answer returned"
            )

            with st.chat_message(
                "assistant"
            ):
                st.write(answer)

            st.session_state.employee_messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )

        except Exception as e:

            st.error(
                f"Error: {e}"
            )

# ---------------- ARCHITECTURE ---------------- #

elif menu == "Architecture":

    st.header(
        "🏗 Project Architecture"
    )

    st.code(
"""
Streamlit UI
      ↓
FastAPI Backend
      ↓
PostgreSQL Database
      ↓
Redis Cache
      ↓
Groq LLM
      ↓
Chroma Vector DB
      ↓
RAG Retrieval
""",
        language="text"
    )