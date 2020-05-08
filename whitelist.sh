#!/bin/bash
name= $1
screen Bedrock -X stuff "whitelist add $name"
screen Bedrock -X stuff "reload ^M"