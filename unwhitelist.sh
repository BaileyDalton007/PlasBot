#!/bin/bash
name= $1
screen -S Bedrock -X stuff "whitelist remove $name ^M"
screen -S Bedrock -X stuff "reload ^M"