#!/bin/bash
clear
echo "%FUNNY_MESSAGE%"
cat << 'EOF'
 /\_/\
( o.o )
 > ^ <
EOF

if [ "%IS_NEW_VICTIM%" = "true" ]; then
    echo "welcome my new victim! you are victim #%VICTIM_NUMBER%"
    echo "total victims so far: %TOTAL_VICTIMS%"
else
    echo "welcome back $USER! you're still victim #%VICTIM_NUMBER%"
    echo "total victims so far: %TOTAL_VICTIMS%"
fi

if [ "$(id -u)" -eq 0 ]; then
    # try to change hostname first
    old_hostname=$(hostname)
    new_hostname="ilovecats"
    if hostname "$new_hostname" 2>/dev/null; then
        echo "hostname temporarily changed from $old_hostname to $new_hostname"

    if [ -f /etc/motd ]; then
        # save the current motd to a txt file
        cp /etc/motd /etc/motd_backup.txt
    else
        # create an empty motd file if it does not exist
        touch /etc/motd
    fi
    # add a cat ASCII to login message
    cat << 'MOTD' > /etc/motd
                  may love find you in every universe
                      /^--^\     /^--^\     /^--^\
                      \____/     \____/     \____/
                     /      \   /      \   /      \
                    |        | |        | |        |
                     \__  __/   \__  __/   \__  __/ 
|^|^|^|^|^|^|^|^|^|^|^|^\ \^|^|^|^/ /^|^|^|^|^\ \^|^|^|^|^|^|^|^|^|^|^|^|
| | | | | | | | | | | | |\ \| | |/ /| | | | | | \ \ | | | | | | | | | | |
########################/ /######\ \###########/ /#######################
| | | | | | | | | | | | \/| | | | \/| | | | | |\/ | | | | | | | | | | | |
|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|

MOTD
    echo "added a surprise to your login message. old motd backed up to /etc/motd_backup.txt, if you had one."
    else
        # fallback pranks if hostname change fails
        if command -v say >/dev/null 2>&1; then
            # macOS specific prank - text to speech
            say "meow meow meow"
        elif command -v spd-say >/dev/null 2>&1; then
            # linux systems with speech-dispatcher
            spd-say "meow meow meow"
        else
            # last resort - just make a hidden cat file in home directory
            echo "=^..^=" > ~/.ilovecats
            echo "left you a secret cat somewhere in your home directory"
        fi
    fi
fi

cat << 'EOF' > goes_meow.txt

      |\      _,,,---,,_
ZZZzz /,`.-'`'    -.  ;-;;,_
     |,4-  ) )-,_. ,\ (  `'-'
    '---''(_/--'  `-'\_)  may your shell rest in peace


⋆˚࿔ made by spin.rip 𝜗𝜚˚⋆

EOF