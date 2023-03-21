import pandas as pd
import streamlit as st
import numpy as np
from st_aggrid import AgGrid, GridOptionsBuilder

#@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv(index=False).encode('utf-8')

class data_import:
    def __init__(self, file_name):
        self.data_frame = self.import_csv(file_name)

    def import_csv(self, file_name):
        df = pd.read_csv(file_name+'.csv')
        return df


rio_items = data_import('rio_items')
rio_histories = data_import('rio_histories')

st.set_page_config(
    page_title="Ex-stream-ly Cool App",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)
st.title('Purchasing system demo')

#builds a gridOptions dictionary using a GridOptionsBuilder instance.
builder = GridOptionsBuilder.from_dataframe(rio_items.data_frame)
builder.configure_pagination(enabled=True, paginationAutoPageSize=False, paginationPageSize=10)
builder.configure_selection('single')
go = builder.build()
#uses the gridOptions dictionary to configure AgGrid behavior.

grid_return = AgGrid(rio_items.data_frame, go)

selected_rows = grid_return['selected_rows']

#st.write(selected_rows)


tab1, tab2 = st.tabs(["table", "chart"])


if selected_rows:
    dfs = pd.DataFrame(selected_rows)
    csv = convert_df(dfs)
    id = int(dfs["id"])
    rio_his = rio_histories.data_frame[rio_histories.data_frame['rio_item_id'] == id]
    rio_his.to_csv('rio_his.csv', index=False)


    with tab1:
        st.dataframe(rio_his.iloc[:, [3,4]], width=1500)




