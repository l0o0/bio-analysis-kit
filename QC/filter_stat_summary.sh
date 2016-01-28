#!/bin/bash

function summary()
{
    read_len=`sed -n '2p' $1 | cut -f 2`
    read raw clean <<< `sed -n '3p' $1 | awk '{print $5*2,$7*2}'`
    read C1 C2 <<< `sed -n '10p' $1 | awk '{print $7,$11}'`
    read G1 G2 <<< `sed -n '11p' $1 | awk '{print $7,$11}'`
    GC=`echo "scale=2; (${C1:1:5} + ${C2:1:5} + ${G1:1:5} + ${G2:1:5})/2" | bc`
    ((bases=raw*150))
    read Q1 Q2 <<< `sed -n '15p' $1 | awk '{print $15,$19}'`
    Q20=`echo "scale=2; (${Q1:1:5} + ${Q2:1:5})/2" | bc`
    printf "%s\t%s\t%s\t%s%%\t%s%%\n" $2 $raw $bases $GC $Q20
}

summary $1 $2 
