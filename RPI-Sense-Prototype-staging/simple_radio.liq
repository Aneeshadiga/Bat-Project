#!/usr/bin/liquidsoap
# Log dir
#log.file.path.set("/usr/local/var/log/liquidsoap/simple_radio.log")

# Music
myplaylist = single("/home/hdg/Documents/Beast_Mode_Song_Beast.mp3")


#mic = input.pulseaudio()

#radio = amplify(1.2,mic)
# Start building the feed with music
radio = myplaylist

#radio = fallback(track_sensitive = false, [radio, radio])
# Stream it out
output.icecast(%vorbis,
  host = "localhost", port = 8000,
  password = "icecast", mount = "audio-stream.ogg",
  radio)
