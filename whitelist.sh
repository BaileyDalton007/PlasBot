#!/bin/bash
screen -S Bedrock -X stuff "whitelist add $1 ^M"
screen -S Bedrock -X stuff "reload ^M"