import streamlit as st
from units import units
from conversions import convert, format_result

st.set_page_config(
    page_title="Unit Converter App",
    page_icon="⚖️",
    layout="wide"
)

st.markdown("""
<style>
    .stSelectbox {
            margin-top: -2.79rem}
    .stNumberInput input {
            background-color: white; !important;}
</style>
""", unsafe_allow_html=True)


st.markdown(
    """<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">""",
    unsafe_allow_html=True
    )

def main():

    col1, col2, col3 = st.columns([0.5, 3, 0.5])

    with col2:
        st.markdown("""
         <div class="header-container" style="margin-bottom: 2rem;">
            <h1>⚖️ Unit Converter App </h1>
            <p>Seamlessly switch between units—fast, simple, accurate!</p>
        </div>
        """, unsafe_allow_html=True)


        unit_category = st.selectbox("", list(units.keys()), index=0)

        from_input_value = st.number_input("", value=1, key="from_input_value")
            
        col4, col5, col6 = st.columns([2, 0.2, 2])
        
        with col4:
            st.write("From")
            from_units = st.selectbox("", [i for i in units[unit_category]])
        
        with col5:
            st.markdown("""<div style="margin-top: 30px; display: flex; justify-content: center; font-size:2rem; color: rgb(144, 241, 0);">
                        <i class="fa-solid fa-right-left"></i>
                        </div>""", unsafe_allow_html=True)

        with col6:
 
            st.write("To")
            to_units = st.selectbox("", [i for i in units[unit_category]], index=1 if len(units[unit_category]) > 1 else 0)

            # calculating the result
            result = convert(from_input_value, from_units, to_units, unit_category)
            formatted_result = format_result(result)


        st.markdown(f"""
            <div style="margin-top: 1rem; font-weight:500; font-size: 1.2rem;">
            Converted Result:
            </div>
            <div style="display: flex; justify-content: center; align-items: baseline; gap: 5px;">
            <div style="font-size: 2rem; font-weight: 600; color: red; display: flex; justify-content: center; align-items: center;">
             {formatted_result} 
            </div>
            <div style="color: red;"> {to_units}</div>
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()