import gradio as gr
from main import run_analysis  # Replace with actual module name

def analyze_stock(company_name):
    path, report = run_analysis(company_name)
    return report

with gr.Blocks() as demo:
    gr.Markdown("# 📈 Stock Analyzer")
    gr.Markdown("Generate a detailed financial report by entering a company name.")

    with gr.Row():
        company_input = gr.Textbox(label="Company Name", placeholder="e.g., Apple")
        analyze_button = gr.Button("Run Analysis")

    report_display = gr.Markdown(label="📋 Report Output")

    analyze_button.click(fn=analyze_stock, inputs=[company_input], outputs=[report_display])

demo.launch()