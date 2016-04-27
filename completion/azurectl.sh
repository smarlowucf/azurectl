#========================================
# _azurectl
#----------------------------------------
function _azurectl {
    local cur prev opts
    _get_comp_words_by_ref cur prev
    local cmd=$(echo $COMP_LINE | sed -e 's@-.*@@'| awk -F ' ' '{ print $NF }')
    for comp in $prev $cmd;do
        case "$comp" in
            "storage")
                __comp_reply "share account disk container"
                return 0
                ;;
            "setup")
                __comp_reply "account"
                return 0
                ;;
            "--debug")
                __comp_reply "storage setup compute"
                return 0
                ;;
            "compute")
                __comp_reply "data-disk image request reserved-ip vm endpoint shell"
                return 0
                ;;
            "account")
                __comp_reply "configure default region list remove --help help show create update regions delete"
                return 0
                ;;
            "endpoint")
                __comp_reply "help show create list --help delete"
                return 0
                ;;
            "container")
                __comp_reply "help show create list sas --help delete"
                return 0
                ;;
            "share")
                __comp_reply "help create list --help delete"
                return 0
                ;;
            "image")
                __comp_reply "help show unreplicate create list update publish replicate replication-status --help delete"
                return 0
                ;;
            "request")
                __comp_reply "status help --help wait"
                return 0
                ;;
            "reserved-ip")
                __comp_reply "help show create list --help delete"
                return 0
                ;;
            "vm")
                __comp_reply "help create regions --help types delete"
                return 0
                ;;
            "data-disk")
                __comp_reply "help show create list --help delete"
                return 0
                ;;
            "disk")
                __comp_reply "delete help --help upload"
                return 0
                ;;
            "status")
                __comp_reply "--id"
                return 0
                ;;
            "configure")
                __comp_reply "--management-pem-file --region --management-url --publish-settings-file --name --subscription-id"
                return 0
                ;;
            "show")
                __comp_reply "--cloud-service-name --lun --instance-name --name"
                return 0
                ;;
            "default")
                __comp_reply "--name"
                return 0
                ;;
            "unreplicate")
                __comp_reply "--name"
                return 0
                ;;
            "create")
                __comp_reply "--lun --cloud-service-name --read-only-cache --instance-name --size --no-cache --read-write-cache --disk-name --label --name --blob --password --ssh-private-key-file --fingerprint --reserved-ip-name --user --instance-type --image-name --custom-data --ssh-port --instance-port --port --idle-timeout --udp --locally-redundant --read-access-geo-redundant --description --geo-redundant --zone-redundant"
                return 0
                ;;
            "list")
                __comp_reply "--cloud-service-name --instance-name"
                return 0
                ;;
            "update")
                __comp_reply "--eula --description --image-family --privacy-uri --icon-uri --name --small-icon-uri --label --language --published-date --new-secondary-key --locally-redundant --read-access-geo-redundant --geo-redundant --zone-redundant --new-primary-key"
                return 0
                ;;
            "publish")
                __comp_reply "--name --msdn --private"
                return 0
                ;;
            "upload")
                __comp_reply "--source --quiet --max-chunk-size --name"
                return 0
                ;;
            "replicate")
                __comp_reply "--quiet --wait --image-version --regions --sku --name --offer"
                return 0
                ;;
            "remove")
                __comp_reply "--name"
                return 0
                ;;
            "sas")
                __comp_reply "--name --start-datetime --expiry-datetime --permissions"
                return 0
                ;;
            "wait")
                __comp_reply "--id"
                return 0
                ;;
            "replication-status")
                __comp_reply "--name"
                return 0
                ;;
            "region")
                __comp_reply "default add help"
                return 0
                ;;
            "delete")
                __comp_reply "--cloud-service-name --lun --instance-name --name --delete-disk"
                return 0
                ;;
            "default")
                __comp_reply "--name --region"
                return 0
                ;;
            "add")
                __comp_reply "--container-name --name --region --storage-account-name"
                return 0
                ;;
            "--region")
                __comp_reply "--storage-account-name"
                return 0
                ;;
            "--storage-account-name")
                __comp_reply "--container-name"
                return 0
                ;;
            "--container-name")
                __comp_reply "--create"
                return 0
                ;;
        esac
    done
    if [[ $COMP_LINE =~ compute ]];then
        __comp_reply "--help"
    else
       __comp_reply "--output-format compute help --region --storage-container setup storage --output-style --config --account --debug --version --help --storage-account"
    fi
    return 0
}
#========================================
# comp_reply
#----------------------------------------
function __comp_reply {
    word_list=$@
    COMPREPLY=($(compgen -W "$word_list" -- ${cur}))
}

complete -F _azurectl -o default azurectl
