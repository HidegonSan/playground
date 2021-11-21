#!/bin/bash

while true;
do
        oldclip=$clip
        clip=`termux-clipboard-get`
        if [ "$oldclip" != "$clip" ]; then
                date=`date`
                echo -e "\n\n\n===================[ "$date" ]====================\n\n\n" | tee -a cliplog.txt
                echo -e $clip | tee -a cliplog.txt
        fi
done

# (C) 2021 Hidegon.
