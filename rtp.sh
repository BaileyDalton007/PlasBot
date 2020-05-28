#!/bin/bash
screen -S Bedrock -X stuff "effect \"$1\" slow_falling 20 ^M"
screen -S Bedrock -X stuff "tp \"$1\" $2 100 $3 ^M"