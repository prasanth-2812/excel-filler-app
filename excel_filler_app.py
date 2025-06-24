import streamlit as st
import pandas as pd
import io

def get_next_image_number(last_image_number):
    # Extract the prefix and numeric part, then increment
    prefix = ''.join(filter(str.isalpha, last_image_number))
    number = int(''.join(filter(str.isdigit, last_image_number)))
    return f"{prefix}{number + 1}"

def generate_next_rows(last_image_number, count=100):
    rows = []
    current_image = last_image_number
    for _ in range(count // 4):
        current_image = get_next_image_number(current_image)
        for i in range(1, 5):
            rows.append({
                "image_number": current_image,
                "serial_number": f"{current_image}_{i}"
            })
    return pd.DataFrame(rows)

st.title("Excel Sequence Filler")

uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.write("Current Data Preview:", df.tail(10))

    # Find the last image_number
    last_image_number = df['image_number'].iloc[-1]

    # Generate next 100 rows
    new_rows = generate_next_rows(last_image_number, count=100)

    # Append to original DataFrame
    updated_df = pd.concat([df, new_rows], ignore_index=True)

    # Download button
    output = io.BytesIO()
    updated_df.to_excel(output, index=False)
    st.download_button(
        label="Download Updated Excel",
        data=output.getvalue(),
        file_name="updated_excel.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    st.write("Preview of new rows to be added:")
    st.write(new_rows) 