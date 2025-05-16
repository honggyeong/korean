import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
import re
from PIL import Image
import io
import base64

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

st.set_page_config(
    page_title="외래어 분석 도구",
    page_icon="📊",
    layout="wide"
)

st.title("외래어 사용 패턴 분석 도구")
st.markdown("""연어 분석을 통해 외래어의 사용과 한국어의 사용이 어떠한 차이점을 가지게 되는지 알아본다
""")

st.sidebar.title("메뉴")
menu = st.sidebar.radio(
    "분석 도구 선택",
    ["연어 분석"]
)


def generate_sample_data():



    data = []

    for native, foreign in pairs:
        native_bias = np.random.uniform(1.5, 3.0)

        for year in years:
            year_factor = 1 + (year - 2009) * 0.05

            for category in categories:
                if foreign in ["오너", "테크"] and category == "경제":
                    native_count = int(np.random.normal(50, 15) * year_factor)
                    foreign_count = int(np.random.normal(70, 20) * year_factor)

                elif foreign in ["뷰티", "플라워"] and category == "문화":
                    native_count = int(np.random.normal(40, 10) * year_factor)
                    foreign_count = int(np.random.normal(65, 15) * year_factor)

                elif foreign == "바캉스" and category == "연예":
                    native_count = int(np.random.normal(30, 10) * year_factor)
                    foreign_count = int(np.random.normal(55, 15) * year_factor)

                else:
                    native_count = int(np.random.normal(80, 20) * year_factor)
                    foreign_count = int(np.random.normal(80 / native_bias, 15) * year_factor)

                native_count = max(0, native_count)
                foreign_count = max(0, foreign_count)

                data.append({
                    "연도": year,
                    "분야": category,
                    "고유어": native,
                    "외래어": foreign,
                    "고유어_빈도": native_count,
                    "외래어_빈도": foreign_count
                })

    collocation_data = []
    collocations = {
        "주인": ["집의", "가게의", "애완동물의", "회사의", "권리의"],
        "오너": ["리스크", "쉐프", "베네핏", "시스템", "오피니언"],
        "아름다움": ["내면의", "자연의", "한국적", "예술적", "순수한"],
        "뷰티": ["아이템", "제품", "트렌드", "에디터", "유튜버"],
        "꽃": ["예쁜", "들판의", "봄", "꽃잎", "향기로운"],
        "플라워": ["이벤트", "샵", "박스", "디자인", "브리딩"]
    }

    for word, colls in collocations.items():
        for coll in colls:
            count = int(np.random.normal(50, 15))
            collocation_data.append({
                "단어": word,
                "연어": coll,
                "빈도": max(0, count)
            })

    return pd.DataFrame(data), pd.DataFrame(collocation_data)






if menu == "연어 분석":
    st.header("연어 분석")

    _, collocation_df = generate_sample_data()

    words = sorted(collocation_df["단어"].unique())

    col1, col2 = st.columns(2)

    with col1:
        word1 = st.selectbox("첫 번째 단어 선택", words, index=0)

    with col2:
        if word1 == "주인":
            default_idx = words.index("오너") if "오너" in words else 0
        elif word1 == "오너":
            default_idx = words.index("주인") if "주인" in words else 0
        elif word1 == "아름다움":
            default_idx = words.index("뷰티") if "뷰티" in words else 0
        elif word1 == "뷰티":
            default_idx = words.index("아름다움") if "아름다움" in words else 0
        elif word1 == "꽃":
            default_idx = words.index("플라워") if "플라워" in words else 0
        elif word1 == "플라워":
            default_idx = words.index("꽃") if "꽃" in words else 0
        else:
            default_idx = 0

        word2 = st.selectbox("두 번째 단어 선택", words, index=default_idx)

    word1_data = collocation_df[collocation_df["단어"] == word1].sort_values("빈도", ascending=False)
    word2_data = collocation_df[collocation_df["단어"] == word2].sort_values("빈도", ascending=False)

    st.subheader(f"'{word1}'와(과) '{word2}'의 연어 비교")

    col1, col2 = st.columns(2)

    with col1:
        st.write(f"### '{word1}'의 연어")
        st.table(word1_data[["연어", "빈도"]])

        fig = px.bar(
            word1_data,
            x="연어",
            y="빈도",
            labels={"연어": "연어", "빈도": "빈도"},
            title=f"'{word1}'의 연어 빈도",
            color_discrete_sequence=[px.colors.qualitative.Set2[0]]
        )
        st.plotly_chart(fig)

    with col2:
        st.write(f"### '{word2}'의 연어")
        st.table(word2_data[["연어", "빈도"]])

        fig = px.bar(
            word2_data,
            x="연어",
            y="빈도",
            labels={"연어": "연어", "빈도": "빈도"},
            title=f"'{word2}'의 연어 빈도",
            color_discrete_sequence=[px.colors.qualitative.Set2[1]]
        )
        st.plotly_chart(fig)

    st.subheader("연어 분석 해석")

    if word1 == "주인" and word2 == "오너":
        st.write("""
        '주인'과 '오너'의 연어 분석 결과를 보면 흥미로운 사용 패턴의 차이를 발견할 수 있다:

        - '주인'은 '집의', '가게의', '애완동물의'와 같은 소유 관계를 나타내는 표현과 함께 사용되는 경향이 있다. 이는 '주인'이 전통적인 소유의 의미로 사용되고 있음을 보여준다.

        - 반면 '오너'는 '리스크', '베네핏', '시스템'과 같은 비즈니스 관련 용어와 함께 사용되는 경향이 있다. 이는 '오너'가 주로 경영 및 비즈니스 맥락에서 사용되고 있음을 보여준다.

        이러한 차이는 두 단어가 비슷한 의미를 가지고 있지만, 사용되는 문맥이 다르다는 것을 보여준다. '오너'는 비즈니스 및 경제 분야에서 특화된 의미로 사용되고 있으며, 이는 외래어 사용의 주요 동기 중 하나인 '특정 분야에서의 전문성 강조'를 반영한다.
        """)
    elif word1 == "아름다움" and word2 == "뷰티":
        st.write("""
        '아름다움'과 '뷰티'의 연어 분석 결과를 보면:

        - '아름다움'은 '내면의', '자연의', '한국적', '예술적', '순수한'과 같은 추상적이고 정서적인 표현과 함께 사용되는 경향이 있다. 이는 '아름다움'이 더 철학적이고 본질적인 의미로 사용되고 있음을 보여준다.

        - 반면 '뷰티'는 '아이템', '제품', '트렌드', '에디터', '유튜버'와 같은 산업 및 상업적 용어와 함께 사용되는 경향이 있다. 이는 '뷰티'가 주로 화장품, 미용 산업, 트렌드와 관련된 맥락에서 사용되고 있음을 보여준다.

        이러한 차이는 '뷰티'가 '아름다움'보다 더 특정한 산업 분야를 지칭하는 데 사용되고 있음을 보여준다. 이는 외래어가 특정 분야나 산업에서 더 선호되는 경향을 반영한다.
        """)
    elif word1 == "꽃" and word2 == "플라워":
        st.write("""
        '꽃'과 '플라워'의 연어 분석 결과를 보면:

        - '꽃'은 '예쁜', '들판의', '봄', '꽃잎', '향기로운'과 같은 자연적이고 감각적인 표현과 함께 사용되는 경향이 있다. 이는 '꽃'이 자연 그대로의 식물을 지칭하는 데 주로 사용됨을 보여준다.

        - 반면 '플라워'는 '이벤트', '샵', '박스', '디자인', '브리딩'과 같은 상업 및 디자인 관련 용어와 함께 사용되는 경향이 있다. 이는 '플라워'가 꽃을 활용한 상품이나 서비스를 지칭하는 데 주로 사용됨을 나타낸다.

        이러한 차이는 '플라워'가 '꽃'과 의미는 유사하지만, 주로 상업적이고 전문적인 맥락에서 사용되고 있음을 보여준다. 외래어 '플라워'는 화훼 산업이나 플라워 디자인과 같은 특정 분야에서 더 전문적인 어감을 주기 위해 선택되는 것으로 보인다.
        """)
    else:
        st.write(f"""
        '{word1}'와(과) '{word2}'의 연어 분석 결과를 보면 두 단어의 사용 맥락에 차이가 있음을 알 수 있다.

        각 단어가 주로 어떤 단어들과 함께 사용되는지 살펴보면, 단어 선택의 동기와 의도를 추론할 수 있다.
        외래어는 종종 특정 분야나 맥락에서 더 전문적이거나 세련된 느낌을 주기 위해 선택되는 경향이 있다.
        """)





