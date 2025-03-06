import streamlit as st
from pint import UnitRegistry
import pandas as pd
import plotly.express as px
import random
import time

def convert_units(value, from_unit, to_unit):
    ureg = UnitRegistry()
    currenccy_rates = {"USD": 1.0, "EUR": 0.92, "GBP": 0.79, "PKR": 277.5, "INR": 83.0, "JPY": 150.0}

    if from_unit in currenccy_rates and to_unit in currenccy_rates:
        result = (value / currenccy_rates[from_unit]) * currenccy_rates[to_unit]
        return result, to_unit

    try:
        result = ureg(from_unit).to(to_unit)
        return result.magnitude, result.units
    except Exception as e:
        return (None, str(e))
    
def get_random_facts():
    facts = [
        "🌍 A light-year is about 5.88 trillion miles!",
        "📏 The metric system is used by 95% of the world!",
        "💧 A gallon of water weighs about 8.34 pounds.",
        "🍎 An apple weighs about 0.28 pounds.",
        "🌌 The universe contains about 7.95 x 10^80 stars.",
        "🌐 The Earth orbits the Sun at a speed of about 29.79 miles per second.",
        "🌾 An inch was originally defined as three barleycorns!",
        "⏳ The fastest recorded human running speed is 27.8 mph!"
    ]
    return random.choice(facts)

def get_random_conversions():
    questions = [
        (1, "kilometer", "meter", 1000),
        (2, "meter", "centimeter", 100),
        (5, "mile", "kilometer", 8.0467),
        (10, "ounce", "gram", 283.495),
        (3, "gallon", "liter", 11.356)
    ]

    return random.choice(questions)

# Streamlit UI 

def main():
    st.set_page_config(page_title="Interactive Unit Converter", page_icon="📏🔄", layout="centered")

    theme = st.sidebar.radio("Select Theme:", ["Light", "Dark"])
    if theme == "Dark":
        st.markdown("""
            <style>
                body { background-color: #181818; color: #E0E0E0; }
                .stButton>button { background-color: white; color: black; border-radius: 8px; padding: 10px; }
            </style>
        """, unsafe_allow_html=True)

    st.title("✨😊 Interactive Unit Converter 🔄")
    st.markdown("""
    ### 🚀 Convert Units Instantly!  
    Easily convert between different units of measurement with just a few clicks.  
    Simply enter your value, choose units, and get the result instantly! ✨  
    """)

    st.sidebar.header("Choose a Category 🔍")
    categories = {
        "📏 Length": ["meter", "kilometer", "mile", "yard", "foot", "inch"],
        "⚖ Weight": ["gram", "kilogram", "pound", "ounce", "ton"],
        "🌡 Temperature": ["Celsius", "Fahrenheit", "Kelvin"],
        "🥤 Volume": ["liter", "milliliter", "gallon", "cup"],
        "🚀 Speed": ["meter/second", "kilometer/hour", "mile/hour"],
        "⏳ Time": ["second", "minute", "hour", "day"],
        "💰 Currency": ["USD", "EUR", "GBP", "PKR", "INR", "JPY"]
    }

    category = st.sidebar.radio("Select a category: ", list(categories.keys()))
    st.subheader(f"🔢 Convert {category}")
    value = st.number_input("Enter a value:", min_value=0.0, step=0.1, format="%.2f")
    from_unit = st.selectbox("From unit:", categories[category])
    to_unit = st.selectbox("To unit:", categories[category])

    if st.button("🔄 Convert"):
        result, units = convert_units(value, from_unit, to_unit)

        if result is not None:
            with st.spinner("Converting..."):
                time.sleep(1)
            st.success(f"✔ {value} {from_unit} = {result:.2f} {units}")
            st.snow()
        else:
            st.error(f"⚠ {units} conversion failed! ✖")

        if "history" not in st.session_state:
            st.session_state.history = []
            st.session_state.history.append([value, from_unit, to_unit, f"{result:.2f} {units}"])

    if st.sidebar.button("📥 Download History as CSV"):
        df = pd.DataFrame(st.session_state.history, columns= ["Value", "From", "To", "Result"])
        csv = df.to_csv(index=False).encode('utf-8')
        st.sidebar.button("Download CSV", csv, "Conversion_history.csv", "text/csv")

    if st.button("📜 View History"):
        if st.session_state.history:
            df = pd.DataFrame(st.session_state.history, columns= ["Value", "From", "To", "Result"])
            st.write("Conversion History 📖")
            st.dataframe(df, use_container_width=True)
            fig = px.line(df, x=df.index, y="Value", title="📊 Conversion Trends", markers=True)
            st.plotly_chart(fig)
        else:
            st.info("📝 No conversions yet. Start now!")

    st.markdown("---")
    st.subheader("🎯 Unit Converter Quiz")
    quiz_value, quiz_from, quiz_to, correct_answer = get_random_conversions()
    user_answer = st.number_input(f"Convert {quiz_value} {quiz_from} to {quiz_to}:", format="%.2f")
    
    if "quiz_score" not in st.session_state:
        st.session_state.quiz_score = 0
        
    if st.button("✔ Check Answer"):
        if abs(user_answer - correct_answer) < 0.1:
            st.success("🚀 Correct Answer! +1 point")
            st.session_state.quiz_score += 1
            st.error(f"❌ Incorrect! The correct answer is {correct_answer:.4f} {quiz_to}")
        st.sidebar.write(f"🏆 Quiz Score: {st.session_state.quiz_score}")
    
    st.sidebar.markdown("😊🌠 Fun Fact")
    st.sidebar.info(get_random_facts())
    st.sidebar.markdown("---")
    st.sidebar.markdown("📧 **Need Help?** Contact: [Support](mailto:areebabano986@gmail.com)")
    
if __name__ == "__main__":
    main()

 