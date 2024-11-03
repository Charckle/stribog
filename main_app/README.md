# What
- a simple app that monitors a source of data and sends out a notification if there is new data in the source
- It stores what it scrapped from the source in memory, meaning, if you first boot it, everything in the source will be new to it.
    - by default, it wont send this data, since it guesses there was a restore, and it does not want to send data twice.
    - this can be overwritten with the config variable `on_no_memory_send_one`. If this variable is set to `true`, the last item scrapped from the internet will be sent.
- to change the source of the scrapping, change the `source_script` script. The required data is already determined, and the required functions also. Just change the functions to your will.
- Email template:
    - it uses jinja2. the base template is stored in `/templates/base.hml`, you can replace it when you mount the docker container

# conf.json
- `on_no_memory_send_one` - if set to true, when it first boots up (when the internal ist of source items is 0), it will send the last scrapped item to the users. Otherwise, it will not send any, since you do not want items to be sent, if you reboot the app. A problem here can be, if there is 0 items in the source after it has scrapped it multiple times, and then a lot of items come at once.

# to-do
- fix log level not updating on hotreload
- add more than one message format (rocketchat, etc)
- log in a json file, to mark actions it made: targets Active removed on failed msg sending, when was last scraped, when was last msg sent
