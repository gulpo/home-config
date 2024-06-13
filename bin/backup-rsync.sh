#!/bin/bash
START_TIME="$(date '+%Y%m%d%H%M')"
BACKUP_DEST='/media/tjekiel/backup-work'
LOG_FILE="/var/log/backup-tjekiel/backup-rsync-$START_TIME.log"
if [ -d $BACKUP_DEST ]; then
    echo "--------- Backup started $START_TIME ---------" >> $LOG_FILE
    rsync -avpF --no-o --no-g --safe-links --delete-delay $HOME/private $BACKUP_DEST/ >> $LOG_FILE 2>&1
    rsync -avpF --no-o --no-g --safe-links --delete-delay $HOME/work $BACKUP_DEST/ >> $LOG_FILE 2>&1
    rsync -avpF --no-o --no-g --safe-links --delete-delay $HOME/bin $BACKUP_DEST/ >> $LOG_FILE 2>&1
    rsync -avpF --no-o --no-g --safe-links --delete-delay $HOME/apps-packages $BACKUP_DEST/ >> $LOG_FILE 2>&1
    rsync -avpF --no-o --no-g --safe-links --delete-delay $HOME/.kube/* $BACKUP_DEST/kube >> $LOG_FILE 2>&1
    rsync -avpF --no-o --no-g --safe-links --delete-delay /etc/hosts $HOME/.zsh* $HOME/.bash* $HOME/*soapui* $BACKUP_DEST >> $LOG_FILE 2>&1
    rsync -avpF --no-o --no-g --safe-links --delete-delay $HOME/.config/Code\ -\ Insiders $BACKUP_DEST/config_Code\ -\ Insiders >> $LOG_FILE 2>&1
#    rsync -avpF $HOME/.config/Code\ -\ Insiders/User/settings.json $BACKUP_DEST/vscode_user_settings.json >> $LOG_FILE 2>&1

#    rsync -avpF --no-o --no-g --safe-links --delete-delay /usr/lib/jvm $BACKUP_DEST/usr_lib_jvm >> $LOG_FILE 2>&1
#    rsync -avpF --no-o --no-g --safe-links --delete-delay /usr/lib/maven $BACKUP_DEST/usr_lib_maven >> $LOG_FILE 2>&1

    echo "--------- Backup ended $START_TIME - $(date '+%Y%m%d%H%M') ---------" >> $LOG_FILE
else 
    echo "Backup SDCard not mounted or mounted elsewhere" >> $LOG_FILE
fi

