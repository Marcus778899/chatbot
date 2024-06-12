# LINEBOT 應用程序

## telegram BotFather

1. First step : init your telegram bot

    ```
    Search @BotFather
    submit "/newbot"
    And name this bot
    ```

    ![image info](./textbook_src/telegram_init.png)

2. Second step :　Save token

    ```
    it will generate the token
    copy this text to login_file
    ```
    
3. make your token path

    ```
    mkdir ./login_info
    nano ./login_info/aka_Marcus_bot.txt
    paste token information
    ```

## activate your service

```bash
poetry env info
poetry lock
poetry install
poetry shell
python telegram_demo.py
```

![image](./textbook_src/output.png)