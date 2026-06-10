import plotly.graph_objects as go

def create_risk_heatmap(scored_results: dict) -> go.Figure:
    """Create a compliance risk heatmap."""
    frameworks = []
    scores = []
    colors = []

    color_map = {
        "LOW RISK": "#22c55e",
        "MEDIUM RISK": "#f59e0b",
        "HIGH RISK": "#ef4444",
        "CRITICAL RISK": "#7f1d1d"
    }

    for fw, result in scored_results.items():
        frameworks.append(result.get("framework_name", fw))
        scores.append(result.get("score", 0))
        colors.append(color_map.get(result.get("label", ""), "#6b7280"))

    fig = go.Figure()

    for i, (fw, score, color) in enumerate(zip(frameworks, scores, colors)):
        fig.add_trace(go.Bar(
            x=[score],
            y=[fw],
            orientation='h',
            marker=dict(
                color=color,
                line=dict(color='#1e293b', width=1)
            ),
            text=f"{score}/100",
            textposition='inside',
            textfont=dict(
                color='white',
                size=13,
                family='JetBrains Mono, monospace'
            ),
            name=fw,
            showlegend=False
        ))

    fig.update_layout(
        title=dict(
            text="COMPLIANCE RISK OVERVIEW",
            font=dict(
                family="JetBrains Mono, monospace",
                size=13,
                color="#94a3b8"
            ),
            x=0
        ),
        xaxis=dict(
            range=[0, 100],
            tickfont=dict(color="#475569", size=10),
            gridcolor="#1e293b",
            zerolinecolor="#1e293b",
            title=dict(
                text="Compliance Score",
                font=dict(color="#475569", size=10)
            )
        ),
        yaxis=dict(
            tickfont=dict(color="#94a3b8", size=10),
            gridcolor="#1e293b"
        ),
        plot_bgcolor="#0f0f1a",
        paper_bgcolor="#0f0f1a",
        margin=dict(l=20, r=20, t=50, b=20),
        height=max(200, len(frameworks) * 70),
        bargap=0.3
    )

    # Add threshold line at 80
    fig.add_vline(
        x=80,
        line_dash="dash",
        line_color="#475569",
        annotation_text="Target: 80",
        annotation_font=dict(color="#475569", size=9)
    )

    return fig

if __name__ == "__main__":
    dummy = {
        "dpdp": {"framework_name": "DPDP Act 2025", "score": 80, "label": "LOW RISK"},
        "gdpr": {"framework_name": "GDPR", "score": 65, "label": "MEDIUM RISK"},
        "eu_ai_act": {"framework_name": "EU AI Act", "score": 40, "label": "HIGH RISK"},
    }
    fig = create_risk_heatmap(dummy)
    print("Heatmap created successfully")
    fig.show()
