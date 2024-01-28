# WhatsAppBot

This is the bot that can. Powered by FastAPI and WhatsApp Business Cloud API.

## Features

- Intelligent Text and Image Input: Ask complex questions, get creative prompts answered, and explore different styles with Google's cutting-edge language models.
- Seamless WhatsApp Integration: Send and receive messages through WhatsApp, making AI accessible and convenient right at your fingertips.
- Huggingface Inference Support (Beta): Access a broad range of pre-trained models for diverse text tasks while exploring the potential of Huggingface's powerful ecosystem.

## Getting Started

### Prerequisites

- Python 3.10.13
- FastAPI
- WhatsApp Business Cloud API credentials
- Google Cloud Platform (GCP) credentials/service account with access to Vertex AI (for Google LLMs)
- (Optional) Additional APIs specific to your desired functionality

### Installation

__Option 1__: Easy Setup (Recommended)
1. Download the repository
    ```bash
    git clone https://github.com/so-dipe/WhatsAppBot.git
    cd WhatsAppBot
    ```

2. Run the installation script:
    ```bash
    ./install.sh
    ```

__Option 2: Manual Setup__:, 

1. Create a Python Virtual Environment in the repository:
    ```bash
    python -m venv venv
    ```
2. Install dependencies in the virtual environment:
    ```bash
    source venv/bin/activate
    pip install -r requirements.txt
    ```
3. Configure settings and Environment Variables

    1. Copy the `sample_config.env` file

        ```bash
        cp sample_config.env .env
        ```
    2. Open .env and replace the placeholder values with your credentials
    3. If you plan on using google's models, paste a copy of your service account at `service_account_key.json`

    alternatively, run the `configure.sh` script
    ```bash
    ./configure.sh
    ```

## Usage
1. Run `run_app.sh` bash script
    ```bash
    ./run_app.sh
    ```

OR Manually start FastAPI and Redis servers.
1.  Run FastAPI server
    ```bash
    uvicorn app.main:app 
    ```
    in developement mode, use
    ```bash
    uvicorn app.main:app --reload
    ```
    by default, a port is opened on 8000.

2.  Run Redis Server
    ```bash
    redis-server config/redis.conf
    ```
    `config/redis.conf` contains the default config file used.

3. Set up ngrok (if needed) to expose your local server to the internet:
    ```bash
    ngrok http 8000
    ```
    Note: WhatsApp Business API requires a webhook callback URL that must be accessible from the internet.
    Explore ngrok for a permanent domain if you prefer.


## Contributing
<!-- Yo! So you want to contribute to this project. Head on over to (Contributing.md) to learn how you can do so. -->

## Roadmap
- Seamless Huggingface Inference API Integration: Empower users with a vast library of pre-trained models and a user-friendly model selection interface.
- Expand LLM Hosting Platform Support: Welcome DeepInfra, AnyScale, and potentially more to offer diverse LLM hosting options.
- Unleash Speech-to-Text Capabilities: Enable voice-based interactions for a more natural and accessible experience.
- Unlock the Power of Documents: Facilitate conversations around PDFs and document files for enriched knowledge sharing.

## License

This project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for details.
