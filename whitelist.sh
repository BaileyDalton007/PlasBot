#!/bin/bash
name= $1
screen -S Bedrock -X stuff "whitelist add $name ^M"
screen -S Bedrock -X stuff "reload ^M"