#========================================
# import_metadata
#----------------------------------------
function import_metadata {
    azurecli_words="help storage container disk image --help --version --config --account"
    help_words="--help"
    storage_words="--help list"
    container_words="--help list"
    disk_words="--help upload delete list --max-chunk-size --name"
    image_words="--help list"
}

#========================================
# _azure_cli
#----------------------------------------
function _azure_cli {
    local cur prev opts
    _get_comp_words_by_ref cur prev

    #========================================
    # Import auto generated metadata
    #----------------------------------------
    import_metadata

    #========================================
    # Current base mode
    #----------------------------------------
    local cmd=$(echo $COMP_LINE | cut -f2 -d " " | tr -d -)

    #========================================
    # Complete word list
    #----------------------------------------
    eval cmd_options=\$${cmd}_words
    if [ -z "$cmd_options" ]; then
        cmd_options=$azurecli_words
    fi
    __comp_reply "$cmd_options"
    return 0
}

#========================================
# comp_reply
#----------------------------------------
function __comp_reply {
    word_list=$@
    COMPREPLY=($(compgen -W "$word_list" -- ${cur}))
}

complete -F _azure_cli -o default azure-cli
