# =========================================================
# ELECTION INTELLIGENCE DASHBOARD
# ENTERPRISE FINAL REFINED VERSION
# CREATED BY OMDEEP CHAUDHARY
# =========================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import os
import base64
import shutil
from datetime import datetime

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Election Intelligence Dashboard",
    page_icon="🗳️",
    layout="wide"
)

# =========================================================
# LOGIN SYSTEM
# =========================================================

USER_CREDENTIALS = {

    "admin": {
        "password": "admin123",
        "role": "admin"
    },

    "analyst": {
        "password": "analyst123",
        "role": "analyst"
    }
}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:

    st.title("🔐 Election Dashboard Login")

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    login_btn = st.button("Login")

    if login_btn:

        if username in USER_CREDENTIALS:

            user_data = USER_CREDENTIALS[username]

            if user_data["password"] == password:

                st.session_state.logged_in = True

                st.session_state.username = username

                st.session_state.role = user_data["role"]

                st.rerun()

            else:

                st.error("Invalid Password")

        else:

            st.error("Invalid Username")

    st.stop()

# =========================================================
# CUSTOM CSS
# =========================================================

def get_base64(file):

    with open(file, "rb") as f:

        return base64.b64encode(
            f.read()
        ).decode()

bg_img = get_base64("bg.jpg")

st.markdown(f"""
<style>

.stApp {{

    background-image: url("data:image/jpg;base64,{bg_img}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    background-color: rgba(0,0,0,0.82);
    background-blend-mode: darken;
    color: white;

}}

h1, h2, h3, h4 {{

    color: #ffedd5 !important;

}}

[data-testid="stSidebar"] {{

    background-color: #7c2d12;

}}

.stButton>button {{

    background-color: #ea580c;
    color: white;
    border-radius: 12px;
    height: 45px;
    font-weight: bold;
    transition: 0.3s;

}}

.stButton>button:hover {{

    background-color: #c2410c;
    transform: scale(1.03);

}}

.stDataFrame {{

    border-radius: 15px;
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(10px);
    padding: 10px;

}}

@media (max-width: 768px) {{

    .stButton>button {{

        width: 100%;

    }}

}}

</style>
""", unsafe_allow_html=True)

# =========================================================
# FILES
# =========================================================

MASTER_FILE = "master_election_data.csv"

# =========================================================
# SESSION STATES
# =========================================================

if "current_round" not in st.session_state:

    if os.path.exists("current_round.txt"):

        with open("current_round.txt", "r") as f:

            st.session_state.current_round = int(
                f.read()
            )

    else:

        st.session_state.current_round = 1

if "validated_rounds" not in st.session_state:

    st.session_state.validated_rounds = []

# =========================================================
# HEADER
# =========================================================

col1, col2 = st.columns([1,5])

with col1:

    if os.path.exists("omdeep.png"):

        st.image(
            "omdeep.png",
            width=170
        )

with col2:

    st.title(
        "🗳️ Election Intelligence Dashboard"
    )

    st.markdown("""
    ### Created by Omdeep Chaudhary
    """)

    st.success(
        f"Logged in as: {st.session_state.username}"
    )

    st.info(
        f"🕒 Live Time: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}"
    )

# =========================================================
# LIVE NEWS TICKER
# =========================================================

st.markdown(
    """
    <marquee>
    🔴 LIVE: Election Dashboard Active |
    Analyst Tracking Enabled |
    Validation Engine Running |
    Round Monitoring Active |
    Enterprise Intelligence System Online
    </marquee>
    """,
    unsafe_allow_html=True
)

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("⚙️ Control Panel")

st.sidebar.success("🟢 System Active")

st.sidebar.success("🟢 Analyst Tracking Enabled")

st.sidebar.success("🟢 Validation Engine Running")

# =========================================================
# LOGOUT BUTTON
# =========================================================

if st.sidebar.button("🚪 Logout"):

    st.session_state.logged_in = False

    st.rerun()

# =========================================================
# USER INFO
# =========================================================

st.sidebar.markdown("---")

st.sidebar.markdown("## 👥 User Accounts")

st.sidebar.info(f"""
Username:
{st.session_state.username}

Role:
{st.session_state.role}
""")

# =========================================================
# CSV UPLOAD
# =========================================================

if st.session_state.role == "admin":

    uploaded_file = st.sidebar.file_uploader(
        "Upload Election CSV",
        type=["csv"]
    )

else:

    st.sidebar.warning(
        "Only Admin Can Upload CSV"
    )

    uploaded_file = None

# =========================================================
# SAVE CSV + BACKUP
# =========================================================

if uploaded_file is not None:

    uploaded_df = pd.read_csv(
        uploaded_file
    )

    uploaded_df.to_csv(
        MASTER_FILE,
        index=False
    )

    if not os.path.exists("backup"):

        os.makedirs("backup")

    backup_file = (
        f"backup/backup_"
        f"{datetime.now().strftime('%d%m%Y_%H%M%S')}.csv"
    )

    shutil.copy(
        MASTER_FILE,
        backup_file
    )

    st.sidebar.success(
        "CSV Uploaded Successfully"
    )

# =========================================================
# LOAD MASTER FILE
# =========================================================

if not os.path.exists(MASTER_FILE):

    st.warning(
        "Please Upload CSV File"
    )

    st.stop()

master_df = pd.read_csv(MASTER_FILE)

# =========================================================
# STATE FILTER
# =========================================================

selected_state = st.sidebar.selectbox(

    "🌍 Filter State",

    ["All"] +

    sorted(master_df["State"].unique())
)

if selected_state != "All":

    master_df = master_df[
        master_df["State"] == selected_state
    ]

# =========================================================
# COLUMN DETECTION
# =========================================================

def detect_column(possible_names):

    for col in master_df.columns:

        for name in possible_names:

            if (
                col.lower().strip()
                ==
                name.lower().strip()
            ):

                return col

    return None

candidate_col = detect_column([
    "Candidate",
    "Candidate Name"
])

party_col = detect_column([
    "Party"
])

constituency_col = detect_column([
    "Constituency"
])

state_col = detect_column([
    "State"
])

# =========================================================
# TOTAL ROUNDS
# =========================================================

total_rounds = st.sidebar.number_input(
    "Number of Rounds",
    min_value=1,
    max_value=50,
    value=5
)

# =========================================================
# ROUND NAVIGATION
# =========================================================

st.sidebar.markdown("---")
st.sidebar.markdown("## 🔄 Round Navigation")

col_nav1, col_nav2 = st.sidebar.columns(2)

with col_nav1:

    if st.button("⬅ Prev"):

        if st.session_state.current_round > 1:

            st.session_state.current_round -= 1

with col_nav2:

    if st.button("Next ➡"):

        if (
            st.session_state.current_round
            <
            total_rounds
        ):

            st.session_state.current_round += 1

with open("current_round.txt", "w") as f:

    f.write(
        str(st.session_state.current_round)
    )

current_round = st.session_state.current_round

st.sidebar.success(
    f"Current Round : {current_round}"
)

progress_value = (
    current_round / total_rounds
)

st.sidebar.progress(progress_value)

# =========================================================
# CREATE ROUND DATAFRAME
# =========================================================

def create_round_dataframe(round_num):

    current_col = f"R{round_num}_Current"

    total_col = f"R{round_num}_Total"

    if round_num == 1:

        previous_votes = [0] * len(master_df)

    else:

        prev_total_col = (
            f"R{round_num-1}_Total"
        )

        if prev_total_col in master_df.columns:

            previous_votes = (
                master_df[prev_total_col]
            )

        else:

            previous_votes = [0] * len(master_df)

    if current_col in master_df.columns:

        current_votes = (
            master_df[current_col]
        )

    else:

        current_votes = [0] * len(master_df)

    if total_col in master_df.columns:

        total_votes = (
            master_df[total_col]
        )

    else:

        total_votes = (
            previous_votes + current_votes
        )

    df = pd.DataFrame({

        "Candidate":
        master_df[candidate_col],

        "Party":
        master_df[party_col],

        "Constituency":
        master_df[constituency_col],

        "State":
        master_df[state_col],

        "Previous Round":
        previous_votes,

        "Current Round":
        current_votes,

        "Total Votes":
        total_votes
    })

    return df

# =========================================================
# LOAD OFFICIAL ROUND
# =========================================================

official_file = (
    f"official_round_{current_round}.csv"
)

if os.path.exists(official_file):

    official_df = pd.read_csv(
        official_file
    )

else:

    official_df = create_round_dataframe(
        current_round
    )

# =========================================================
# KPI + INTELLIGENCE CENTER
# =========================================================

st.markdown("---")

st.markdown("## 📡 Election Intelligence Center")

total_votes_all = official_df["Total Votes"].sum()

total_candidates = len(official_df)

leading_party = (
    official_df.groupby("Party")["Total Votes"]
    .sum()
    .idxmax()
)

validated_count = len(
    st.session_state.validated_rounds
)

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.metric(
        "🗳 Total Votes",
        f"{total_votes_all:,}"
    )

with k2:
    st.metric(
        "👥 Candidates",
        total_candidates
    )

with k3:
    st.metric(
        "🏆 Leading Party",
        leading_party
    )

with k4:
    st.metric(
        "✅ Validated",
        f"{validated_count}/{total_rounds}"
    )

leader_df = official_df.sort_values(
    by="Total Votes",
    ascending=False
)

leader = leader_df.iloc[0]

st.success(f"""

🌍 State : {leader['State']}

🏆 Leading Party :
{leader['Party']}

👤 Candidate :
{leader['Candidate']}

📍 Constituency :
{leader['Constituency']}

🗳️ Total Votes :
{int(leader['Total Votes'])}

""")

# =========================================================
# OFFICIAL TABLE
# =========================================================

st.markdown(
    f"# 📌 Official Round {current_round}"
)

with st.form(f"official_form_{current_round}"):

    edited_official = st.data_editor(

        official_df,

        use_container_width=True,

        hide_index=True,

        num_rows="fixed",

        disabled=True,

        key=f"official_editor_{current_round}"
    )

    official_save = st.form_submit_button(
        "💾 Save Official Round"
    )

    if official_save:

        edited_official.to_csv(
            official_file,
            index=False
        )

        st.success(
            "Official Round Saved"
        )

# =========================================================
# ANALYST VALIDATION
# =========================================================

st.markdown("---")

st.markdown(
    f"# 🔍 Analyst Validation - Round {current_round}"
)

lock_file = (
    f"round_{current_round}_locked.txt"
)

is_locked = os.path.exists(lock_file)

analyst_file = (
    f"analyst_round_{current_round}.csv"
)

if os.path.exists(analyst_file):

    analyst_df = pd.read_csv(
        analyst_file
    )

else:

    analyst_df = official_df.copy()

    analyst_df["Current Round"] = 0

    analyst_df["Total Votes"] = (
        analyst_df["Previous Round"]
    )

with st.form(f"analyst_form_{current_round}"):

    edited_analyst = st.data_editor(

        analyst_df,

        use_container_width=True,

        hide_index=True,

        num_rows="fixed",

        disabled=[
            "Candidate",
            "Party",
            "Constituency",
            "State",
            "Previous Round",
            "Total Votes"
        ] if not is_locked else True,

        key=f"analyst_editor_{current_round}"
    )

    edited_analyst["Total Votes"] = (

        edited_analyst["Previous Round"]

        +

        edited_analyst["Current Round"]

    )

    analyst_save = st.form_submit_button(
        "💾 Save Analyst Entry"
    )

    if analyst_save:

        edited_analyst.to_csv(
            analyst_file,
            index=False
        )

        with open("audit_log.txt", "a") as log:

            log.write(

                f"{datetime.now()} | "

                f"{st.session_state.username} "

                f"updated Round {current_round}\n"
            )

        st.success(
            "Analyst Validation Saved"
        )

# =========================================================
# VALIDATION
# =========================================================

st.markdown("---")

st.markdown("## ✅ Validate Round")

validation_df = pd.DataFrame({

    "Candidate":
    edited_official["Candidate"],

    "Official Total":
    edited_official["Total Votes"],

    "Analyst Total":
    edited_analyst["Total Votes"]

})

validation_df["Status"] = validation_df.apply(

    lambda x:

    "✅ Match"

    if x["Official Total"]
    ==
    x["Analyst Total"]

    else "❌ Mismatch",

    axis=1
)

st.dataframe(
    validation_df,
    use_container_width=True
)

# =========================================================
# VALIDATION STATUS
# =========================================================

if all(
    validation_df["Status"] == "✅ Match"
):

    if (
        current_round
        not in st.session_state.validated_rounds
    ):

        st.session_state.validated_rounds.append(
            current_round
        )

    with open(lock_file, "w") as f:

        f.write("LOCKED")

    st.success(
        f"Round {current_round} Validated Successfully"
    )

else:

    st.error(
        f"Round {current_round} Validation Failed"
    )

# =========================================================
# ANALYTICS
# =========================================================

st.markdown("---")

st.markdown(
    f"## 📊 Round {current_round} Vote Analytics"
)

chart_df = edited_official.groupby(

    ["Party", "Candidate"],

    as_index=False

)["Total Votes"].sum()

fig = px.bar(

    chart_df,

    x="Party",

    y="Total Votes",

    color="Party",

    barmode="group",

    title=f"Round {current_round} Party Vote Share"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =========================================================
# PIE CHART
# =========================================================

st.markdown("### 🥧 Total Vote Share")

party_total = edited_official.groupby(
    "Party",
    as_index=False
)["Total Votes"].sum()

pie_fig = px.pie(

    party_total,

    names="Party",

    values="Total Votes",

    hole=0.5
)

st.plotly_chart(
    pie_fig,
    use_container_width=True
)

# =========================================================
# FINAL RESULT
# =========================================================

if current_round == total_rounds:

    st.markdown("---")

    st.markdown("## 🏆 Final Election Result")

    final_result = edited_official.sort_values(

        by="Total Votes",

        ascending=False
    )

    winner = final_result.iloc[0]

    runner_up = final_result.iloc[1]

    margin = (

        winner["Total Votes"]

        -

        runner_up["Total Votes"]

    )

    col_w1, col_w2 = st.columns(2)

    with col_w1:

        st.success(f"""

🥇 Winner

Candidate:
{winner["Candidate"]}

Party:
{winner["Party"]}

Votes:
{winner["Total Votes"]}
""")

    with col_w2:

        st.warning(f"""

🥈 Runner Up

Candidate:
{runner_up["Candidate"]}

Party:
{runner_up["Party"]}

Votes:
{runner_up["Total Votes"]}
""")

    st.info(
        f"🏁 Winning Margin : {margin}"
    )

    st.balloons()

# =========================================================
# VALIDATION SUMMARY
# =========================================================

st.markdown("---")

st.markdown("## 📌 Validation Summary")

summary_data = []

for rnd in range(1, total_rounds + 1):

    status = (

        "✅ Validated"

        if rnd in st.session_state.validated_rounds

        else "⏳ Pending"
    )

    summary_data.append({

        "Round": rnd,

        "Status": status
    })

summary_df = pd.DataFrame(
    summary_data
)

st.dataframe(

    summary_df,

    use_container_width=True,

    hide_index=True
)

# =========================================================
# LIVE ANALYST TRACKING
# =========================================================

st.markdown("---")

st.markdown("## 🛰️ Live Analyst Activity")

if os.path.exists("audit_log.txt"):

    with open("audit_log.txt", "r") as f:

        logs = f.readlines()

    latest_logs = logs[-5:]

    for log in reversed(latest_logs):

        st.info(log)

else:

    st.warning("No Analyst Activity Found")

# =========================================================
# EXPORT REPORTS
# =========================================================

st.markdown("---")

st.markdown("## 📥 Export Reports")

col_exp1, col_exp2, col_exp3 = st.columns(3)

with col_exp1:

    st.download_button(

        label="⬇ Official Report",

        data=edited_official.to_csv(index=False),

        file_name=f"official_round_{current_round}.csv",

        mime="text/csv"
    )

with col_exp2:

    st.download_button(

        label="⬇ Analyst Report",

        data=edited_analyst.to_csv(index=False),

        file_name=f"analyst_round_{current_round}.csv",

        mime="text/csv"
    )

with col_exp3:

    st.download_button(

        label="⬇ Validation Report",

        data=validation_df.to_csv(index=False),

        file_name=f"validation_round_{current_round}.csv",

        mime="text/csv"
    )

# =========================================================
# AUDIT LOGS
# =========================================================

st.markdown("---")

st.markdown("## 📜 Audit Logs")

if os.path.exists("audit_log.txt"):

    with open("audit_log.txt", "r") as log:

        logs = log.readlines()

    for entry in reversed(logs[-10:]):

        st.text(entry)

# =========================================================
# RESET SYSTEM
# =========================================================

st.markdown("---")

if st.session_state.role == "admin":

    if st.button("🗑 Reset Entire System"):

        if os.path.exists(MASTER_FILE):

            os.remove(MASTER_FILE)

        for i in range(1, 101):

            official_file = (
                f"official_round_{i}.csv"
            )

            analyst_file = (
                f"analyst_round_{i}.csv"
            )

            lock_file = (
                f"round_{i}_locked.txt"
            )

            if os.path.exists(official_file):

                os.remove(official_file)

            if os.path.exists(analyst_file):

                os.remove(analyst_file)

            if os.path.exists(lock_file):

                os.remove(lock_file)

        st.success(
            "System Reset Successfully"
        )

else:

    st.warning(
        "Only Admin Can Reset System"
    )

# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.caption(

    "Election Intelligence Dashboard | "

    "Created by Omdeep Chaudhary"
)