import math
import pandas as pd
import plotly.express as px
import streamlit as st
from scipy.stats import norm

from src.config import PROCESSED_DATA_PATH, RAW_DATA_PATH
from src.insights import executive_summary, highest_churn_segment
from src.metrics import proxy_funnel, rate_table, top_churn_segments
from src.pipeline import run_pipeline, transform_users
from src.recommendations import generate_recommendations

st.set_page_config(page_title="Netflix User Analytics", page_icon="N", layout="wide")
RED = "#E50914"
LAYOUT = dict(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(255,255,255,.02)", font=dict(color="#F4F4F5"), margin=dict(l=10,r=10,t=45,b=10))
st.markdown("""<style>
.stApp{background:radial-gradient(circle at 80% 0%,#241115,#111114 38%,#09090b);color:#F4F4F5}
[data-testid="stSidebar"]{background:#101014;border-right:1px solid #2A2A30}
[data-testid="stMetric"]{background:linear-gradient(135deg,#1A1A20,#131318);border:1px solid #303039;border-radius:16px;padding:18px}
.hero h1{font-size:2.55rem;letter-spacing:-.08rem;margin:0}.accent{color:#E50914;font-weight:800}.subtle{color:#A1A1AA}
.insight{background:#17171D;border-left:3px solid #E50914;border-radius:8px;padding:.8rem 1rem;margin:.45rem 0 1rem}
.rec{background:linear-gradient(145deg,#1D1A1F,#15151A);border:1px solid #38313A;border-radius:14px;padding:1.1rem;min-height:250px}
</style>""", unsafe_allow_html=True)

@st.cache_data(show_spinner=False)
def cached_read(path: str) -> pd.DataFrame: return pd.read_csv(path)

def load_data():
    uploaded = st.sidebar.file_uploader("Upload CSV", type="csv")
    if uploaded: return transform_users(pd.read_csv(uploaded))
    if PROCESSED_DATA_PATH.exists(): return cached_read(str(PROCESSED_DATA_PATH))
    if RAW_DATA_PATH.exists(): return transform_users(pd.read_csv(RAW_DATA_PATH))
    return None

def chart(fig, title):
    fig.update_layout(**LAYOUT, title=title)
    fig.update_xaxes(gridcolor="#2A2A30"); fig.update_yaxes(gridcolor="#2A2A30")
    return fig

def insight(observed, meaning, investigate):
    st.markdown(f"<div class='insight'><b>Observed:</b> {observed}<br><b>Why it matters:</b> {meaning}<br><b>Investigate:</b> {investigate}</div>", unsafe_allow_html=True)

def reset():
    for key in ["country","age","gender","plan","device","genre","frequency"]: st.session_state.pop(key, None)

st.markdown("<div class='hero'><h1><span class='accent'>NETFLIX</span> USER ANALYTICS</h1><div class='subtle'>Understand users. Improve engagement. Reduce churn.</div></div>", unsafe_allow_html=True)
with st.sidebar:
    st.header("Data & filters")
    if RAW_DATA_PATH.exists() and st.button("Refresh processed data", use_container_width=True):
        run_pipeline(RAW_DATA_PATH, PROCESSED_DATA_PATH); st.cache_data.clear(); st.success("Data refreshed. Raw input was not changed.")
    if st.button("Reset filters", use_container_width=True): reset(); st.rerun()

df = load_data()
if df is None:
    st.info("Add the CSV to `data/raw/netflix_user_behavior_dataset.csv`, run `python run_pipeline.py`, or upload it above."); st.stop()
with st.sidebar:
    countries=st.multiselect("Country",sorted(df.country.unique()),key="country",placeholder="All countries")
    ages=st.multiselect("Age group",sorted(df.age_group.unique()),key="age",placeholder="All age groups")
    genders=st.multiselect("Gender",sorted(df.gender.unique()),key="gender",placeholder="All genders")
    plans=st.multiselect("Subscription plan",sorted(df.subscription_type.unique()),key="plan",placeholder="All plans")
    devices=st.multiselect("Device",sorted(df.primary_device.unique()),key="device",placeholder="All devices")
    genres=st.multiselect("Content genre",sorted(df.favorite_genre.unique()),key="genre",placeholder="All genres")
    freq=st.multiselect("Viewing frequency",sorted(df.viewing_frequency.unique()),key="frequency",placeholder="All frequencies")
    st.caption("Snapshot • 50k users • no event timestamps or acquisition channels")
def selector(values, col): return df[col].isin(values) if values else pd.Series(True,index=df.index)
filtered=df[selector(countries,"country")&selector(ages,"age_group")&selector(genders,"gender")&selector(plans,"subscription_type")&selector(devices,"primary_device")&selector(genres,"favorite_genre")&selector(freq,"viewing_frequency")]
if filtered.empty: st.warning("No users match these filters. Reset or broaden a selection."); st.stop()

recent=(filtered.days_since_last_login<=7).mean(); churn=filtered.churned_flag.mean()
for col,label,value,help_text in zip(st.columns(5),["Total users","Recently active","Avg. watch time","Retained proxy","Churn rate"],[f"{len(filtered):,}",f"{recent:.1%}",f"{filtered.avg_watch_time_minutes.mean():.0f} min",f"{1-churn:.1%}",f"{churn:.1%}"],["Users in this view.","Logged in within seven days.","Source dataset average.","One minus churn flag; not calendar retention.","Churned users / users in view."]): col.metric(label,value,help=help_text)

overview,behavior,engagement,content,retention,recs,experiment=st.tabs(["Overview","User behavior","Engagement","Content","Retention & churn","Recommendations","Experiment lab"])
with overview:
    st.subheader("Executive summary"); st.caption("Descriptive signals only—this snapshot cannot prove causation.")
    for item in executive_summary(filtered): st.markdown(f"- {item}")
    a,b=st.columns(2); recency=rate_table(filtered,"recency_segment"); plan=rate_table(filtered,"subscription_type")
    with a:
        st.plotly_chart(chart(px.bar(recency,x="recency_segment",y="churn_rate",color="churn_rate",text_auto=".1%",color_continuous_scale="Reds",labels={"churn_rate":"Churn rate"}),"Where is churn concentrated?"),use_container_width=True)
        risk=highest_churn_segment(filtered,"recency_segment"); insight(f"{risk['recency_segment']} has the highest churn ({risk['churn_rate']:.1%}, n={int(risk['users']):,}).","Inactivity is a useful retention-risk signal.","Compare discovery, playback and cancellation journeys for this group.")
    with b:
        st.plotly_chart(chart(px.bar(plan,x="subscription_type",y="avg_watch_minutes",color="activation_rate",text_auto=".0f",color_continuous_scale="Teal",labels={"avg_watch_minutes":"Avg. watch minutes"}),"Engagement by plan"),use_container_width=True)
        winner=plan.loc[plan.avg_watch_minutes.idxmax()]; insight(f"{winner['subscription_type']} has the highest average watch time ({winner['avg_watch_minutes']:.0f} min).","High-engagement users can reveal successful product behaviors.","Check content supply and customer mix before changing pricing or benefits.")
with behavior:
    left,right=st.columns(2); age=rate_table(filtered,"age_group"); device=rate_table(filtered,"primary_device")
    with left:
        st.plotly_chart(chart(px.bar(age,x="age_group",y="avg_watch_minutes",color="activation_rate",text_auto=".0f",color_continuous_scale="Teal",labels={"avg_watch_minutes":"Avg. watch minutes"}),"Who watches the most?"),use_container_width=True)
        lead=age.loc[age.avg_watch_minutes.idxmax()]; insight(f"{lead['age_group']} has the highest watch time ({lead['avg_watch_minutes']:.0f} min).","Age can help frame qualitative research.","Validate with content preference and acquisition data first.")
    with right:
        st.plotly_chart(chart(px.bar(device,x="primary_device",y="users",color="users",text_auto=",",color_continuous_scale="Reds"),"Which devices do users prefer?"),use_container_width=True)
        lead=device.loc[device.users.idxmax()]; insight(f"{lead['primary_device']} is most common ({int(lead['users']):,} users).","It is a strong place to prioritize UX diagnostics.","Review search, discovery and playback on this device.")
with engagement:
    left,right=st.columns(2); frequency=rate_table(filtered,"viewing_frequency")
    with left:
        st.plotly_chart(chart(px.bar(frequency,x="viewing_frequency",y="avg_watch_minutes",color="churn_rate",text_auto=".0f",color_continuous_scale="Reds",labels={"avg_watch_minutes":"Avg. watch minutes"}),"Watch time by viewing frequency"),use_container_width=True)
        insight("Viewing frequency is derived from weekly sessions.","It shows whether weak viewing cadence aligns with lower engagement.","Measure return triggers with event-level data.")
    with right:
        fig=px.scatter(filtered,x="watch_sessions_per_week",y="avg_watch_time_minutes",color="churned",hover_data=["subscription_type","primary_device","favorite_genre"],opacity=.55,labels={"watch_sessions_per_week":"Sessions per week","avg_watch_time_minutes":"Watch time (minutes)"})
        st.plotly_chart(chart(fig,"Sessions and watch time"),use_container_width=True)
        insight("The distribution separates snapshot behavior by churn flag.","It surfaces patterns worth testing—not causes of churn.","Control for plan, device and tenure before targeting users.")
with content:
    genre=rate_table(filtered,"favorite_genre").sort_values("avg_watch_minutes")
    st.plotly_chart(chart(px.bar(genre,x="avg_watch_minutes",y="favorite_genre",orientation="h",color="churn_rate",text_auto=".0f",color_continuous_scale="Reds",labels={"avg_watch_minutes":"Avg. watch minutes"}),"Which genres are associated with deeper engagement?"),use_container_width=True)
    lead=genre.loc[genre.avg_watch_minutes.idxmax()]; insight(f"{lead['favorite_genre']} fans have the highest watch time ({lead['avg_watch_minutes']:.0f} min).","This could identify a high-value content affinity.","Compare title supply and completion by genre.")
with retention:
    st.warning("This source is a snapshot: it supports churn comparison, not calendar cohorts or D1/D7/D30 retention.")
    dimension=st.selectbox("Compare churn by",["primary_device","subscription_type","country","favorite_genre","payment_method","engagement_segment","recency_segment"])
    segment=top_churn_segments(filtered,dimension)
    # px.bar has no `size` argument; user count appears in the hover detail instead.
    fig=px.bar(segment,x=dimension,y="churn_rate",color="activation_rate",text_auto=".1%",hover_data={"users":":,","activation_rate":".1%","avg_watch_minutes":".0f","avg_sessions_per_week":".1f"},color_continuous_scale="Teal",labels={"churn_rate":"Churn rate","activation_rate":"Activation proxy"})
    st.plotly_chart(chart(fig,"Which segment has the highest churn?"),use_container_width=True)
    high=segment.iloc[0]; insight(f"{high[dimension]} has the highest churn ({high['churn_rate']:.1%}, n={int(high['users']):,}).","It is a candidate for investigation, not confirmed root cause.","Compare first-session success, payment friction, content availability and cancellations.")
    st.dataframe(segment.style.format({"churn_rate":"{:.1%}","activation_rate":"{:.1%}","avg_watch_minutes":"{:.0f}","avg_sessions_per_week":"{:.1f}"}),use_container_width=True,hide_index=True)
with recs:
    st.subheader("What should a PM do next?")
    st.caption("These cards recalculate from the active filters. They are prioritization hypotheses, not causal findings.")
    for col,item in zip(st.columns(3), generate_recommendations(filtered)):
        col.markdown(f"<div class='rec'><span class='accent'>{item['priority']} PRIORITY</span><h4>{item['title']}</h4><b>Evidence</b><br>{item['evidence']}<br><br><b>Target</b><br>{item['target']}<br><br><b>Experiment</b><br>{item['experiment']}<br><br><b>Metric</b><br>{item['metric']}</div>",unsafe_allow_html=True)
with experiment:
    st.subheader("A/B-test planner"); st.caption("Plan a test here; the snapshot contains no experiment assignment or treatment outcome.")
    base=st.number_input("Baseline activation rate",.001,.999,float(filtered.activated_proxy.mean()),.01,format="%.3f"); mde=st.number_input("Minimum detectable lift (percentage points)",.1,50.,5.,.5)
    treatment=min(base+mde/100,.999); pooled=(base+treatment)/2
    n=math.ceil(((norm.ppf(.975)*math.sqrt(2*pooled*(1-pooled))+norm.ppf(.8)*math.sqrt(base*(1-base)+treatment*(1-treatment)))**2)/((treatment-base)**2))
    st.metric("Estimated sample",f"{n:,} users per variant",help="Two-sided comparison of two proportions, alpha 0.05 and 80% power.")
    insight(f"This test aims to lift activation from {base:.1%} to {treatment:.1%}.","Pre-registering a success criterion makes a product decision more rigorous.","Capture user_id, timestamp, variant, onboarding completion, first title start, playback errors, cancellation and D7 retention.")
