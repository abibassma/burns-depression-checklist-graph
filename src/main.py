import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

CSV_PATH = "data.csv"
OUTPUT_DIR = "outputs"
SCORE_WEIGHT = 8
DAYFIRST = True
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Read raw CSV
df = pd.read_csv(CSV_PATH)

# For debugging purposes: show raw columns and a few rows
print("Raw columns:", df.columns.tolist())
print(df.head().to_string(index=False))

df.columns = [c.strip() for c in df.columns] # Normalize column names (strip spaces)

print("Normalized columns:", df.columns.tolist()) # Show sui-column

# timestamp parsing
df['Horodateur'] = pd.to_datetime(df['Horodateur'], dayfirst=DAYFIRST, errors='coerce')
if df['Horodateur'].isna().any():
    print("Warning: some Horodateur values could not be parsed to datetime:")
    print(df.loc[df['Horodateur'].isna()].to_string(index=False))

# verify numeric columns
for col in ['Score', 'BDC Score']:
    if col not in df.columns:
        raise SystemExit(f"Column '{col}' not found in CSV. Columns: {df.columns.tolist()}")
    df[col] = pd.to_numeric(df[col], errors='coerce')

# unspect dtypes and NaNs
print(df.dtypes)
print("Rows with NaNs:")
print(df[df[['Score','BDC Score','Horodateur']].isna().any(axis=1)].to_string(index=False))

# drop rows with missing essential data
df = df.dropna(subset=['Horodateur','Score','BDC Score']).copy()
df = df.sort_values('Horodateur')

df['Score_weighted'] = df['Score'] * SCORE_WEIGHT # Compute weighted score

# Depression Bands (as per Interpretation)
bands = [
    (0, 5, "No depression", "green", 0.12),
    (6, 10, "Normal but unhappy", "limegreen", 0.10),
    (11, 25, "Mild depression", "yellow", 0.10),
    (26, 50, "Moderate depression", "orange", 0.10),
    (51, 75, "Severe depression", "orangered", 0.10),
    (76, 100, "Extreme depression", "red", 0.12),
]

# validate rows
mask_scorew = df['Score_weighted'].between(0, 100)
mask_bdc = df['BDC Score'].between(0, 100)
valid_mask = mask_scorew & mask_bdc
valid_df = df.loc[valid_mask].copy()
invalid_df = df.loc[~valid_mask].copy()

print(f"Total rows: {len(df)}, valid: {len(valid_df)}, invalid: {len(invalid_df)}")

# --- px figure ---
plot_df = valid_df.melt(id_vars=['Horodateur'], value_vars=['BDC Score','Score_weighted'],
                        var_name='series', value_name='value')
fig = px.line(plot_df, x='Horodateur', y='value', color='series', markers=True,
              title='BDC vs Weighted Score (valid points)')
fig.update_traces(mode='lines+markers', hovertemplate='%{x}<br>%{y}<extra>%{legendgroup}</extra>')
if not invalid_df.empty:
    fig.add_scatter(x=invalid_df['Horodateur'], y=invalid_df['Score_weighted'],
                    mode='markers', name='Invalid (ignored)', marker=dict(color='black', symbol='x', size=8))
fig.write_html(os.path.join(OUTPUT_DIR, "fig_px_line.html"), include_plotlyjs='cdn')
print("Saved:", os.path.join(OUTPUT_DIR, "fig_px_line.html"))

# --- go.Figure with bands ---
fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=valid_df['Horodateur'], y=valid_df['BDC Score'],
                          mode='lines+markers', name='BDC Score', line=dict(color='royalblue')))
fig2.add_trace(go.Scatter(x=valid_df['Horodateur'], y=valid_df['Score_weighted'],
                          mode='lines+markers', name='Score (weighted x8)', line=dict(color='crimson')))
if not invalid_df.empty:
    fig2.add_trace(go.Scatter(x=invalid_df['Horodateur'], y=invalid_df['Score_weighted'],
                              mode='markers', name='Invalid (ignored)', marker=dict(color='black', symbol='x', size=8),
                              visible='legendonly'))
shapes = []
annots = []
for y0,y1,label,color,opacity in bands:
    shapes.append(dict(type="rect", xref="paper", x0=0, x1=1, yref="y", y0=y0, y1=y1,
                       fillcolor=color, opacity=opacity, layer="below", line_width=0))
    annots.append(dict(xref="paper", x=0.99, xanchor="right", y=(y0+y1)/2, yref="y",
                       text=label, showarrow=False, font=dict(color=color)))
fig2.update_layout(shapes=shapes, annotations=annots, title='BDC vs Weighted Score', xaxis_title='Timestamp', yaxis_title='Score')
fig2.write_html(os.path.join(OUTPUT_DIR, "fig_go_line.html"), include_plotlyjs='cdn')
print("Saved:", os.path.join(OUTPUT_DIR, "fig_go_line.html"))

# If you still see no HTML files, check current working directory:
print("CWD:", os.getcwd())
print("Output files:", os.listdir(OUTPUT_DIR))
