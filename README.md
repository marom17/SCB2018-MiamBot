# SCB2018-MiamBot
A chat bot to log food and drink

### Prerequisites
* A bot create with telegram's [botfather](https://core.telegram.org/bots)
* A database running on [mLab](https://mlab.com/home) or other mongodb system
* A dns domain (the bot use webhook to get messages)
* Docker
* Docker-compose

### Installation
Pull the current repos on the server that wil host the bot.
In the file *init-letsencyrpt.sh*, change the domain and email inforation by our own. Then launch the script to create the certificate.
```sh
sudo init-letsencrypt.sh
```
Create 2 files in the folder *miambot*: **.token** and **.credential**
*miambot/.token*: the token provided by telegram's botfather
```sh
TelegramBotToken
```
*miambot/.credential*: the mLab or other mongodb url with user and credential
```sh
{
    "HOST": "mongodb://user:pass@server.example.com:port/database"
}
```
Build the bot server image
```sh
sudo docker-compose build
```
And then launch the app
```sh
sudo docker-compose up
```
The bot is now runing.

### Other
We use a modified version of [nginx-certbot](https://github.com/wmnnd/nginx-certbot) github repo for setup nginx and lets encrypt certificates.
