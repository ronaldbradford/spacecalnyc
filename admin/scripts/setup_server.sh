#!/bin/sh

# Commands to setup the necessary dependencies from a 
# clean provisioned Ubuntu Server
#
sudo apt-get update -y

#TODO:  Add mysql password avoidance steps
sudo apt-get install -y mysql-server  python-mysql.connector
