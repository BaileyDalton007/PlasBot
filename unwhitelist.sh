#!/bin/bash
screen -S Bedrock -X stuff "whitelist remove $1 ^M"
screen -S Bedrock -X stuff "reload ^M"