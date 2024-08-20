# [Aiogram Project Template](https://github.com/taimast/AiogramTemplate)

**A flexible template for creating bots using Aiogram 3, featuring powerful tools for admin management, payments, localization, and more.**

## ✨ Features

- **Admin Panel**: Comprehensive and easy-to-use admin interface.
- **Middleware**: Custom middlewares to handle user sessions, localization, and database interactions.
- **Localization**: Fluent localization system for multiple languages.
- **Payments**: Integrated support for multiple payment providers:
  - [CryptoCloud](https://cryptocloud.plus/)
  - [CryptoPay](https://github.com/LulzLoL231/pyCryptoPayAPI)
  - [Qiwi](https://qiwi.com/p2p-admin/api/)
  - [YooKassa](https://yookassa.ru/developers/)
  - USDT
  - [Payeer](https://payeer.com/)
  - [Cryptomus](https://cryptomus.com/)
  - [WalletPay](https://pay.wallet.tg/)
  - [Payok](https://payok.io/)
  - [Aaio](https://aaio.so/)
  - [BetaTransfer](https://betatransfer.io/)

- **Command Line Interface (CLI)**: Simplified management and configuration via command line.
- **Webhook Configuration**: Easy setup and management of webhooks for efficient bot operation.
- **Database ORM**: Fully integrated with [SQLAlchemy](https://github.com/sqlalchemy/sqlalchemy) for database management.
- **DB Migration**: Database versioning with [Alembic](https://github.com/sqlalchemy/alembic).
- **Configuration Management**: Robust configuration handling using [Pydantic](https://github.com/pydantic/pydantic).

## 🗂️ Project Structure

- **`src/apps`**: Contains bot-related logic, including handlers, middlewares, and localization.
- **`src/config`**: Configuration files and environment settings.
- **`src/db`**: Database models, migrations, and ORM settings.
- **`src/setup`**: Scripts for setting up the bot, including logging, scheduling, routers, and more.
- **`src/utils`**: Utility scripts for tasks like localization, callback generation, and more.

## 🌍 Localization

Localization is handled via [Fluent](https://projectfluent.org/fluent/guide). Default localization files are located in the `src/locales` directory.

### Utilities for Localization

- **Live Stub Generation**: `src/utils/ftl_parser_cli.py` – Automatically generates stubs for localization as you work.
- **Automatic Translation**: `src/utils/ftl_translator.py` – Translates localizations into multiple languages using Google Translate and generates corresponding FTL files.

## ⚙️ Setup and Installation

1. **Configure the Project:**
   - Fill in the `config.yml` with your specific settings.
   
2. **Run the Project:**
   - Start the project using Docker: `docker compose up -d`.

### Updating the Project

1. **Stop the Containers:**
   - Run `docker compose stop` to stop the running containers.
   
2. **Rebuild and Restart:**
   - Use `docker compose up -d --build` to rebuild and restart the containers.

## 🚀 Additional Functionalities

- **Callback Data Generator**: `src/utils/generate_callback.py` – Dynamically generates callback data classes for your bot.
- **Mailing System**: `src/utils/mailing.py` – Handles mass mailing and notifications to users with detailed progress tracking.
- **State Management**: `src/utils/state.py` – Simplified handling of user states within FSM context.
- **User Connection and Referral**: `src/db/models/user/mixins.py` – Mixins for managing user connections and referrals.
