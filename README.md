# pi-mangatracker

WARNING: this script is a work in progress and it's just for reference.

## Description

This is a script I decided to write for personal use.
It uses browser automation through BeautifulSoup. It reads a list of urls from a popular italian manga website, it reads the release date of the next volume for the series and sends the results to the user via python-telegram-bot.  

The script is dockerized and the image is only built for armv7 architecture (like my Raspberry Pi 4).

Some sensitive data like passwords and tokens are passed through enviromnent variables for security.

## Installation

My use case is to add the following command to a crontab with the desired schedule. It will start the container, execute the script and then remove the container.

The --env-file flag is used to set environment variables in the container (they are listed in a file).
The text file needs to be passed from the host to the container and it is done mounting a volume. 

```bash
docker run -v /home/pi/manga_urls.txt:/pi-mangatracker/manga_urls.txt --env-file env.list --rm dylzen/pi-mangatracker
```

## Screenshot

Here's an example of a generated telegram message:  

![Telegram_MwGtilItuy](https://user-images.githubusercontent.com/29499866/151622466-368848f3-dd8e-4413-8955-0e5959fc7f29.png)

## Author

Dylan Tangredi\
[linkedin](https://www.linkedin.com/in/dylantangredi/)
