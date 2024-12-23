import argparse
import logging
import os
import signal
import subprocess
import sys
from pyngrok import ngrok, conf

def setup_logging():
    """
    Configures the logging settings.
    """
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def setup_ngrok(token: str, port: int = 8501) -> str:
    """
    Sets up ngrok tunneling for the given port.

    :param token: ngrok authentication token.
    :param port: Port for Streamlit to run on.
    :return: Public URL of the ngrok tunnel.
    """
    try:
        ngrok.set_auth_token(token)

        conf.get_default().region = "us"  
        tunnel = ngrok.connect(port, bind_tls=True)
        public_url = tunnel.public_url
        logging.info(f"ngrok tunnel established: {public_url}")
        return public_url
    except Exception as e:
        logging.error(f"Failed to set up ngrok tunnel: {e}")
        sys.exit(1)

def run_streamlit(app_path: str, token: str, port: int = 8501):
    """
    Runs the Streamlit app on the specified port with ngrok tunneling.

    :param app_path: Path to the Streamlit app file.
    :param token: ngrok authentication token.
    :param port: Port for Streamlit to run on.
    """
    public_url = setup_ngrok(token, port)
    logging.info(f"Streamlit app will be accessible at: {public_url}")

    try:
        process = subprocess.Popen(
            ["streamlit", "run", app_path, "--server.port", str(port)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            preexec_fn=os.setsid  
        )
    except FileNotFoundError:
        logging.error("Streamlit is not installed or not found in PATH.")
        ngrok.kill()
        sys.exit(1)
    except Exception as e:
        logging.error(f"Failed to start Streamlit: {e}")
        ngrok.kill()
        sys.exit(1)

    def terminate_process(signum, frame):
        logging.info("Termination signal received. Shutting down...")
        try:
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        except Exception as e:
            logging.error(f"Error terminating Streamlit process: {e}")
        ngrok.disconnect(public_url)
        ngrok.kill()
        sys.exit(0)

    signal.signal(signal.SIGINT, terminate_process)
    signal.signal(signal.SIGTERM, terminate_process)

    try:
        stdout, stderr = process.communicate()
        if process.returncode != 0:
            logging.error(f"Streamlit failed with error: {stderr.decode().strip()}")
            ngrok.disconnect(public_url)
            ngrok.kill()
            sys.exit(process.returncode)
    except Exception as e:
        logging.error(f"An error occurred while running Streamlit: {e}")
        ngrok.disconnect(public_url)
        ngrok.kill()
        sys.exit(1)
    finally:
        ngrok.disconnect(public_url)
        ngrok.kill()

def main():
    """
    Command-line interface for streamlit_colab.
    Usage: stc <app.py> <ngrok_token> [--port PORT]
    """
    parser = argparse.ArgumentParser(
        description="Run a Streamlit app with ngrok tunneling."
    )
    parser.add_argument(
        "app_path",
        type=str,
        help="Path to the Streamlit app file (e.g., app.py)."
    )
    parser.add_argument(
        "ngrok_token",
        type=str,
        nargs='?',
        default=os.getenv("NGROK_TOKEN"),
        help="ngrok authentication token. Can also be set via NGROK_TOKEN environment variable."
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8501,
        help="Port for Streamlit to run on (default: 8501)."
    )

    args = parser.parse_args()

    if not args.ngrok_token:
        logging.error("ngrok token is required. Provide it as an argument or set the NGROK_TOKEN environment variable.")
        parser.print_help()
        sys.exit(1)

    if not os.path.isfile(args.app_path):
        logging.error(f"Streamlit app file not found: {args.app_path}")
        sys.exit(1)

    run_streamlit(args.app_path, args.ngrok_token, args.port)

if __name__ == '__main__':
    setup_logging()
    main()