import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="0050 每日分析", layout="wide", page_icon="📈")
st.title("🧐 0050 每日股市分析 APP")
st.caption("適合新手的簡單工具｜資料來自 Yahoo Finance｜非投資建議")

# ==================== 取得資料（改用 yf.Ticker，更穩定） ====================
ticker = "0050.TW"
taiex = "^TWII"

@st.cache_data(ttl=3600)
def get_stock_data(symbol, period="1mo"):
    try:
        stock = yf.Ticker(symbol)
        df = stock.history(period=period)
        if df.empty:
            return pd.DataFrame()
        return df
    except:
        return pd.DataFrame()

hist = get_stock_data(ticker)
taiex_hist = get_stock_data(taiex)

# ==================== 計算 0050 價格 ====================
if not hist.empty and len(hist) >= 2:
    current_price = round(float(hist['Close'].iloc[-1]), 2)
    prev_price = round(float(hist['Close'].iloc[-2]), 2)
    change_pct = round(((current_price - prev_price) / prev_price) * 100, 2)
    date_str = hist.index[-1].strftime('%Y-%m-%d')
else:
    current_price = 0
    change_pct = 0
    date_str = "資料取得失敗（可能市場休市）"

# ==================== 計算 台灣加權指數 ====================
if not taiex_hist.empty and len(taiex_hist) >= 2:
    taiex_change = round(((float(taiex_hist['Close'].iloc[-1]) - float(taiex_hist['Close'].iloc[-2])) / float(taiex_hist['Close'].iloc[-2])) * 100, 2)
else:
    taiex_change = 0

# ==================== 顯示重點數據 ====================
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label=f"**0050 最新收盤價** ({date_str})", 
              value=f"{current_price} TWD", 
              delta=f"{change_pct}%")
with col2:
    st.metric(label="台灣加權指數漲跌", 
              value=" ", 
              delta=f"{taiex_change}%")
with col3:
    st.write("**成交量**")
    if not hist.empty and pd.notna(hist['Volume'].iloc[-1]):
        st.write(f"{int(hist['Volume'].iloc[-1]):,} 股")
    else:
        st.write("N/A")

# ==================== 價格走勢圖 ====================
st.subheader("過去一個月價格走勢")
if not hist.empty:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=hist.index, y=hist['Close'], name='0050 收盤價', line=dict(color='#1f77b4')))
    fig.update_layout(title='0050 價格走勢', xaxis_title='日期', yaxis_title='價格 (TWD)', height=400)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("目前無法顯示走勢圖（資料抓取失敗）")

# ==================== 簡單分析 ====================
st.subheader("📌 今日漲跌可能原因（新手版）")
st.write(f"**{date_str} 0050 {change_pct}%**")

st.markdown("""
- **最主要原因**：台積電（2330）占 0050 權重約 45%，它漲 → 0050 就容易漲  
- **其他常見因素**：美股科技股、台幣匯率、Fed 消息、台灣景氣數據
""")

st.info("💡 小提醒：股市漲跌很正常，0050 最適合新手用「定期定額」長期持有。本 APP 僅供學習參考")

st.subheader("🔗 快速連結")
st.markdown("[Yahoo 奇摩股市 - 0050](https://tw.stock.yahoo.com/quote/0050.TW)")
st.markdown("[台灣加權指數即時走勢](https://tw.stock.yahoo.com/quote/%5ETWII)")

st.caption("資料更新時間以 Yahoo Finance 為準｜投資有風險")
