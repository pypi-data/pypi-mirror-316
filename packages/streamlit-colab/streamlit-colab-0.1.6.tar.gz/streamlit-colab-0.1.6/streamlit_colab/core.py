import argparse
import os
from pyngrok import ngrok

def setup_ngrok(port=8501):
    """
    Set up ngrok tunneling for the specified port.
    :param port: Port to expose via ngrok (default: 8501).
    :return: Public URL for the ngrok tunnel.
    """
    public_url = ngrok.connect(port).public_url
    print(f"Public URL: {public_url}")
    return public_url

def run_streamlit(app_path, ngrok_token, port=8501):
    """
    Run a Streamlit app using ngrok tunneling.
    :param app_path: Path to the Streamlit app file.
    :param ngrok_token: ngrok authentication token.
    :param port: Port for Streamlit to run on (default: 8501).
    """
    # Set up ngrok with the provided token
    ngrok.set_auth_token(ngrok_token)
    public_url = setup_ngrok(port=port)

    # Run the Streamlit app
    os.system(f"streamlit run {app_path} --server.port {port}")

def main():
    """
    Command-line interface for the Streamlit app with ngrok.
    Usage: stc <app_path> <ngrok_token> [port]
    """
    parser = argparse.ArgumentParser(description="Run a Streamlit app with ngrok tunneling.")
    parser.add_argument(
        "app_path",
        type=str,
        help="Path to the Streamlit app file (e.g., app.py)."
    )
    parser.add_argument(
        "ngrok_token",
        type=str,
        help="ngrok authentication token."
    )
    parser.add_argument(
        "port",
        type=int,
        nargs="?",
        default=8501,
        help="Port for Streamlit to run on (default: 8501)."
    )

    args = parser.parse_args()

    if not os.path.isfile(args.app_path):
        print(f"Error: Streamlit app file not found: {args.app_path}")
        exit(1)

    run_streamlit(args.app_path, args.ngrok_token, args.port)

def cli():
    """
    Entry point for the `stc` command.
    """
    main()

if __name__ == "__main__":
    cli()
