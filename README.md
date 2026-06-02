# SIIAU Course Availability Scraper

A modular web scraper that monitors course availability in SIIAU (Sistema Integral de Información Académica Universitaria) and sends real-time alerts via Telegram.

## 📋 Overview

This project provides an automated monitoring system for tracking course slot availability in educational institutions using SIIAU. When availability changes, the system instantly notifies registered users through Telegram, enabling them to enroll in courses quickly.

## 🚀 Architecture

The project follows a clean, modular architecture:

- **`main.py`**: Main orchestrator that coordinates configuration loading, scraping, and alert delivery
- **`fetcher.py`**: Extracts and parses HTML data, returning structured course information
- **`evaluator.py`**: Implements availability logic and constructs alert messages
- **`notifier.py`**: Handles Telegram API communication using the `requests` library
- **`settings.py`**: Loads sensitive variables from `.env` and validates configuration

## 📦 Requirements

Install dependencies using:

```bash
pip install -r requirements.txt
```

**Required packages:**

- `requests` - HTTP client library
- `beautifulsoup4` - HTML parsing library
- `python-dotenv` - Environment variable management

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/KALLIIOZ/SiiauScrapper.git
cd SiiauScrapper
```

2. Create a virtual environment (recommended):
```bash
python -m venv .venv
.venv\Scripts\activate  # On Windows
source .venv/bin/activate  # On macOS/Linux
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## ⚙️ Configuration

### Step 1: Environment Setup

Create a `.env` file in the root directory (or copy from `.env.example`):

```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM_CHAT_IDS=123456789,987654321
POLL_INTERVAL_SECONDS=5
MONITORING_CONFIG_PATH=monitoring_config.json
LOG_FILE=errores.log
```

**Configuration Variables:**

| Variable | Description | Example |
|----------|-------------|---------|
| `TELEGRAM_BOT_TOKEN` | Bot token from BotFather | `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11` |
| `TELEGRAM_CHAT_IDS` | Comma-separated recipient chat IDs | `123456789,987654321` |
| `POLL_INTERVAL_SECONDS` | Interval between checks (seconds) | `5` |
| `MONITORING_CONFIG_PATH` | Path to monitoring configuration | `monitoring_config.json` |
| `LOG_FILE` | Error log file name | `errores.log` |

### Step 2: Telegram Bot Setup

1. Create a Telegram bot with [@BotFather](https://t.me/botfather)
2. Copy your `TELEGRAM_BOT_TOKEN`
3. Get your chat ID (send `/start` to your bot and extract the ID from the response)

### Step 3: Monitor Configuration

Edit `monitoring_config.json` to define monitors, chat recipients, and URLs:

```json
{
  "monitors": [
    {
      "name": "Monitor Name",
      "url": "https://example.com/courses",
      "chat_ids": [123456789],
      "course_identifiers": ["COURSE-CODE-001"]
    }
  ]
}
```

## ▶️ Usage

Start the monitoring system:

```bash
python main.py
```

The script will:
- Periodically check configured URLs for course availability
- Send Telegram alerts when availability changes
- Log errors to the specified log file
- Continue monitoring until stopped (Ctrl+C)

## 📁 Project Structure

```
SiiauScrapper/
├── main.py                    # Entry point
├── monitoring_config.json     # Monitor configuration
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── src/
│   ├── __init__.py
│   └── siiauscrapper/
│       ├── __init__.py
│       ├── evaluator.py       # Availability evaluation logic
│       ├── fetcher.py         # HTML scraping
│       ├── models.py          # Data models
│       ├── notifier.py        # Telegram notifications
│       └── settings.py        # Configuration management
└── legacy/                    # Deprecated modules
```

## 📌 Key Features

- ✅ **Modular Design**: Clean separation of concerns for easy maintenance
- ✅ **Flexible Configuration**: JSON-based monitoring setup
- ✅ **Secure Credentials**: Environment variables keep sensitive data safe
- ✅ **Smart Parsing**: Robust HTML parsing using table rows and cells (not brittle index-based extraction)
- ✅ **Real-time Alerts**: Instant Telegram notifications on availability changes
- ✅ **Error Logging**: Comprehensive error tracking for troubleshooting

## 🐛 Troubleshooting

**Bot not sending messages?**
- Verify `TELEGRAM_BOT_TOKEN` is correct
- Ensure chat IDs are valid and the bot has permissions to message them

**No courses being detected?**
- Check the URL structure in `monitoring_config.json`
- Verify HTML selectors match the current website structure
- Review the log file for parsing errors

**Configuration not loading?**
- Ensure `.env` file exists in the project root
- Verify `monitoring_config.json` is valid JSON

## 📝 Notes

- The main monitoring configuration is stored in `monitoring_config.json`
- The scraping logic uses flexible HTML row/cell parsing instead of rigid table index jumps
- Sensitive credentials are loaded from `.env`, simplifying deployments and keeping code clean
- Logs are written to the file specified in the `LOG_FILE` environment variable

## 🤝 Contributing

Contributions are welcome! To help improve this project:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the MIT License.

## 👤 Author

**KALLIIOZ** - [GitHub Profile](https://github.com/KALLIIOZ)

## 📞 Support

If you encounter issues or have questions, please:
- Check the [Troubleshooting](#-troubleshooting) section
- Open an [Issue](https://github.com/KALLIIOZ/SiiauScrapper/issues)
- Review existing documentation
