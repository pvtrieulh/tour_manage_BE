#!/usr/bin/env bash
crontab -l > tetvietdev
echo "1 * * * * /home/ec2-user/app/production/tetviet/scripts/push_notifications.sh" >> tetvietdev
crontab tetvietdev
rm tetvietdev
