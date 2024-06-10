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
            return "Teams not found in the data"
        team1_win_rate = team1_data['Winning Percentage'].mean()
        team2_win_rate = team2_data['Winning Percentage'].mean()

        if team1_win_rate > team2_win_rate:
            return team1
        elif team1_win_rate < team2_win_rate:
            return team2
        else:
            return "Both teams have the same winning percentage"

    st.title('NBA Match Prediction🏀')
    if team1 != team2:
        winner = predict_winner(team1, team2)
        st.write(f"The predicted winner between {team1} and {team2} is: **{winner}**")
    else:
        st.write("Please select two different teams.")

    st.title('Historical Winning Percentages')
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(data=df, x='Team', y='Winning Percentage', ax=ax, palette="coolwarm")
    plt.xticks(rotation=45, ha='right', fontsize=12)
    plt.yticks(fontsize=12)
    plt.xlabel('Team', fontsize=14)
    plt.ylabel('Winning Percentage', fontsize=14)
    plt.title('Historical Winning Percentages by Team', fontsize=16)
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







