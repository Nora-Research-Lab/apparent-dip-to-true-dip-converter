import gradio as gr
from apparent_dip_to_true_dip_converter import compute_true_dip

def process(app_dip, app_dir, strike):
    if app_dip is None or app_dir is None or strike is None:
        return "Invalid input: all fields are required.", "", None
    try:
        app_dip = float(app_dip)
        app_dir = float(app_dir)
        strike = float(strike)
    except (ValueError, TypeError):
        return "Invalid input: numeric values required.", "", None
    result = compute_true_dip(app_dip, app_dir, strike)
    if result is None:
        return "Error: Apparent dip direction is parallel to strike (θ = 0°). The apparent dip cannot be measured in this orientation.", "", None
    true_dip, true_dir, fig = result
    return f"{true_dip:.1f}°", f"{true_dir:.1f}°", fig

with gr.Blocks(title="Apparent Dip to True Dip Converter") as demo:
    gr.Markdown("## Apparent Dip to True Dip Converter")
    with gr.Row():
        app_dip_in = gr.Number(label="Apparent dip angle (°)", minimum=0, maximum=90, step=0.1)
        app_dir_in = gr.Number(label="Apparent dip direction azimuth (°)", minimum=0, maximum=360, step=0.1)
        strike_in = gr.Number(label="Strike azimuth (right-hand rule) (°)", minimum=0, maximum=360, step=0.1)
    compute_btn = gr.Button("Compute")
    with gr.Row():
        true_dip_out = gr.Textbox(label="True dip angle")
        true_dir_out = gr.Textbox(label="True dip direction azimuth")
    plot_out = gr.Plot(label="Geometric diagram")
    compute_btn.click(fn=process, inputs=[app_dip_in, app_dir_in, strike_in], outputs=[true_dip_out, true_dir_out, plot_out])

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
