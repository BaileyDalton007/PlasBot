#!/bin/bash
screen -S Bedrock -X stuff "whitelist remove \"$1\" ^M"
screen -S Bedrock -X stuff "kick \"$1\""
screen -S Bedrock -X stuff "reload ^M"