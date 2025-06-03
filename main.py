import streamlit as st
import pandas as pd
from youtube_api import search_videos, get_comments
from comment_filter import is_spam, has_link, is_useful
from io import BytesIO

st.set_page_config(page_title="YouTube Comment Analyzer")

API_KEY = "AIzaSyBce8zkHaX5SC42SM2tBKu_RZzrMY46UUo"

st.title("🔍 YouTube Comment Analyzer")

query = st.text_input("Nhập từ khóa tìm kiếm video:")
max_videos = st.slider("Số lượng video:", 1, 10, 3)

progress_bar = st.empty()

if st.button("Bắt đầu tìm kiếm"):
    video_list = search_videos(API_KEY, query, max_results=max_videos)
    all_data = []

    for i, (video_id, title) in enumerate(video_list):
        progress_bar.progress((i + 1) / len(video_list))
        comments = get_comments(API_KEY, video_id)
        for c in comments:
            all_data.append({
                "Video Number": i + 1,
                "Video Title": title,
                "Video Link": f"https://www.youtube.com/watch?v={video_id}",
                "Comment": c,
                "Spam": is_spam(c),
                "Has Link": has_link(c),
                "Useful": is_useful(c)
            })

    df = pd.DataFrame(all_data)
    st.success("🎉 Dữ liệu đã thu thập xong!")
    st.dataframe(df)

    def export_to_excel(df):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            for i, (vid, group) in enumerate(df.groupby("Video Number"), start=1):
                sheet_name = str(i)
                group[["Video Title", "Video Link", "Comment", "Useful", "Spam"]].to_excel(
                    writer,
                    sheet_name=sheet_name,
                    index=False
                )
        output.seek(0)
        return output

    if not df.empty:
        excel_data = export_to_excel(df)
        st.download_button(
            label="📥 Tải Excel (mỗi sheet là 1 video)",
            data=excel_data,
            file_name="youtube_comments_by_video.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
