import streamlit as st
import time

# Add CSS style for background image, font styles, and padding
st.markdown(
    """
    <style>
    .main {
       background-image: url('https://4kwallpapers.com/images/wallpapers/dark-background-abstract-background-network-3d-background-3840x2160-8324.png');
        background-size: cover;
        color: white;
        font-family: 'Times New Roman';
        font-weight: bold; 
        padding: 45px; 
    }

    .stRadio div div div {
        color: white !important;
    }

    .title {
        color: white;
        font-weight: bold;
        text-transform: capitalize;
        font-size: 40px; 
    }

    .text {
        font-weight: bold;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

class ReaderWriter:
    def __init__(self):
        self.read_count = 0
        self.completed_task = False
        self.user_input = ""

    def Writer(self):
        if self.user_input == "Writer":
            st.write("Writer entered")
            st.write("Other Readers and Writers are waiting")
            time.sleep(4.0)
            if self.completed_task:
                st.write("Other Readers and Writers can enter now")

    def Reader(self):
        if self.user_input == "Reader":
            st.write("Reader entered")
            st.write("Other Writers are waiting, but this file can be read by other Readers.")
            self.read_count += 1
            if self.read_count == 1:
                st.write("Locking out Writers")
            time.sleep(5)  # Simulate reading time
            self.read_count -= 1
            if self.read_count == 0 and self.completed_task:
                st.write("Releasing Writer lock")

    def get_user_input(self):
        st.markdown("<div class='title'>Reader-Writer Simulation</div>", unsafe_allow_html=True)

        user_input = st.radio("", ("Reader", "Writer"))
        if user_input:
            self.user_input = user_input

        completion_status = st.radio("Task completion status:", ("Not Completed", "Completed"), key="completion_status")
        if completion_status == "Completed":
            self.completed_task = True
        else:
            self.completed_task = False

if __name__ == "__main__":
    rw = ReaderWriter()

    # Run Streamlit app
    rw.get_user_input()
    if rw.user_input == "Reader":
        rw.Reader()
    elif rw.user_input == "Writer":
        rw.Writer()
