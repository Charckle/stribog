# What
- a simple app that monitors a source of data and sends out a notification if there is new data in the source
- It stores what it scrapped from the source in memory, meaning, if you first boot it, everything in the source will be new to it.
    - by default, it wont send this data, since it guesses there was a restore, and it does not want to send data twice.
    - this can be overwritten with the config variable `on_no_memory_send_one`. If this variable is set to `true`, the last item scrapped from the internet will be sent.
- to change the source of the scrapping, change the `source_script` script. The required data is already determined, and the required functions also. Just change the functions to your will.

# to-do
- fix logging for emails
- add html format for messages
- add more than one message format (rocketchat, etc)
