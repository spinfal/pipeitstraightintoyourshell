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

cat << 'EOF' > goes_meow.txt
      |\      _,,,---,,_
ZZZzz /,`.-'`'    -.  ;-;;,_
     |,4-  ) )-,_. ,\ (  `'-'
    '---''(_/--'  `-'\_)  may your shell rest in peace
EOF