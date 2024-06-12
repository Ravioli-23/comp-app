import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import base64
import os

st.set_page_config(
    page_title="NBA Match Prediction",
    page_icon="🏀",
    layout="wide"
)

@st.cache_data
def load_data():
    # Use relative path
    file_path = os.path.join(os.path.dirname(__file__), 'Historical-NBA-Performance.xlsx')
    try:
        df = pd.read_excel(file_path)
        return df
    except FileNotFoundError:
        st.error("File not found. Please check the file path.")
        return None

df = load_data()

if df is None or df.empty:
    st.error("Failed to load data. Please check the file path and format of the Excel file.")
else:
    st.markdown(
        """
        <style>
        body {
            background-image: url("NBAESPN_2_Header_1600-780x470.jpg");
            background-size: cover;
            font-family: Arial, sans-serif;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.sidebar.title('Team Selection')
    teams = df['Team'].unique()

    team1 = st.sidebar.selectbox('Select the first team', teams)
    team2 = st.sidebar.selectbox('Select the second team', teams)

    def predict_winner(team1, team2):
        team1_data = df[df['Team'] == team1]
        team2_data = df[df['Team'] == team2]
        if team1_data.empty or team2_data.empty:
            return "Teams not found in the data", None, None
        team1_win_rate = team1_data['Winning Percentage'].mean()
        team2_win_rate = team2_data['Winning Percentage'].mean()

        if team1_win_rate > team2_win_rate:
            return team1, team1_win_rate, team2_win_rate
        elif team1_win_rate < team2_win_rate:
            return team2, team1_win_rate, team2_win_rate
        else:
            return "Both teams have the same winning percentage", team1_win_rate, team2_win_rate

    st.title('NBA Match Prediction🏀')
    if team1 != team2:
        winner, team1_win_rate, team2_win_rate = predict_winner(team1, team2)
        if winner == "Both teams have the same winning percentage":
            st.write(f"<h2>The match between {team1} and {team2} is predicted to be a tie with both having a winning percentage of {team1_win_rate:.2f}%.</h2>", unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div style="text-align: center; margin-top: 20px;">
                    <h1 style="font-size: 48px;">The predicted winner between {team1} and {team2} is:</h1>
                    <h2 style="font-size: 60px; color: #FF5733;">{winner}</h2>
                    <p style="font-size:
                    <p style="font-size: 24px;">Winning Percentage:</p>
                    <p style="font-size: 36px;">{team1} - {team1_win_rate:.2f}%</p>
                    <p style="font-size: 36px;">{team2} - {team2_win_rate:.2f}%</p>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.write("<h2>Please select two different teams.</h2>", unsafe_allow_html=True)

    st.title('Comparison of Winning Percentages')
    fig, ax = plt.subplots(figsize=(14, 8))
    sns.barplot(data=df[df['Team'].isin([team1, team2])], x='Team', y='Winning Percentage', ax=ax, palette="coolwarm", ci=None)
    plt.xticks(rotation=0, ha='center', fontsize=12)
    plt.yticks(fontsize=12)
    plt.xlabel('Team', fontsize=14)
    plt.ylabel('Winning Percentage', fontsize=14)
    plt.title('Winning Percentages Comparison', fontsize=16)
    sns.despine()
    plt.tight_layout()
    st.pyplot(fig)

@st.cache_data
def get_img_as_base64(file):
    if os.path.exists(file):
        with open(file, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    else:
        st.error(f"File not found: {file}")
        return None

# Use relative path
img_path = os.path.join(os.path.dirname(__file__), 'NBAESPN.jpg')
img = get_img_as_base64(img_path)

if img:
    page_bg_img = f"""
    <style>
    [data-testid="stAppViewContainer"] > .main {{
    background-image: url("https://thewriteresume.com/wp-content/uploads/2014/11/NBA-Logo-Big.png");
    background-size: 45%;
    background-position: top right;
    background-repeat: no-repeat;
    background-attachment: local;
    }}

    [data-testid="stSidebar"] > div:first-child {{
    background-image: url("data:image/png;base64,{img}");
    background-position: center; 
    background-repeat: no-repeat;
    background-attachment: fixed;
    }}

    [data-testid="stHeader"] {{
    background: rgba(0,0,0,0);
    }}

    [data-testid="stToolbar"] {{
    right: 2rem;
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

st.title("It's NBA playing time⛹🏻‍♂️!")
st.sidebar.header("Configuration")

with st.container():
    st.header("Playoffs Mode")
    st.markdown(
        "Enter into the action-packed world of NBA Predictor, where data becomes destiny and expectation fills the air with an electrifying charge. Using a blend of statistical mastery and the newest algorithms, this is the final oracle of basketball that will thrill you with its shivering forecasts in unsurpassed accuracy. So, for those who have been bitten by the gambling bug and the experienced fantasy league maestros and diehard fans who dare know how sweet victory can be, the NBA Predictor is their beacon in the storm, guiding them through the tumultuous seas of the NBA with unflinching confidence. Expect a roller-coaster ride because, in this electrifying arena, each and every prediction is a shot at immortality."
    )









