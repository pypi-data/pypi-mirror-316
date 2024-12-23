import os
import argparse
from pyngrok import ngrok

def setup_ngrok(port=8501):
    """
    Set up an ngrok tunnel for the specified port.
    :param port: Port to expose via ngrok (default: 8501).
    :return: Public URL for the ngrok tunnel.
    """
    public_url = ngrok.connect(port).public_url
    print(f"Public URL: {public_url}")
    return public_url

def run_streamlit(app_path, port=8501):
    """
    Run a Streamlit app on the specified port.
    :param app_path: Path to the Streamlit app file.
    :param port: Port for Streamlit to run on (default: 8501).
    """
    # Start Streamlit app
    os.system(f"streamlit run {app_path} --server.port {port}")

def cli():
    """
    Command-line interface for the Streamlit app with ngrok.
    Usage: stc <app.py> [--port PORT]
    """
    parser = argparse.ArgumentParser(description="Run a Streamlit app with ngrok tunneling.")
    parser.add_argument(
        "app_path",
        type=str,
        help="Path to the Streamlit app file (e.g., app.py)."
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8501,
        help="Port for Streamlit to run on (default: 8501)."
    )

    args = parser.parse_args()

    # Run ngrok and Streamlit
    setup_ngrok(port=args.port)
    run_streamlit(app_path=args.app_path, port=args.port)

if __name__ == "__main__":
    cli()
