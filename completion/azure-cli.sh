# azure-cli bash completion script

function _azure_cli {
    local cur prev opts
    _get_comp_words_by_ref cur prev

    #========================================
    # Current base mode
    #----------------------------------------
    local cmd=$(echo $COMP_LINE | cut -f2 -d " " | tr -d -)

    #========================================
    # main commands
    #----------------------------------------
    local commands=$(__azure_cli_commands)
    local options=$(__azure_cli_command_opts)

    #========================================
    # sub commands
    #----------------------------------------
    local sub_commands=$(__azure_cli_commands $cmd)
    if [ ! -z "$sub_commands" ];then
        commands=$sub_commands
        options="--help $(__azure_cli_command_opts $cmd)"
    fi

    __comp_reply "$commands $options"
    return 0
}

#========================================
# comp_reply
#----------------------------------------
function __comp_reply {
    word_list=$@
    COMPREPLY=($(compgen -W "$word_list" -- ${cur}))
}

#========================================
# __azure_cli_command_opts
#----------------------------------------
function __azure_cli_command_opts {
    local begin=0
    local mode
    local search="global options:"
    if [ ! $1 = "azurecli" ]; then
        mode=$1
        search="options:"
    fi
    azure-cli $mode --help | while read line; do
        if [[ "$line" =~ ^$search ]];then
            begin=1
        elif [ $begin -eq 1 ];then
            opt=$(echo $line | cut -f1-2 -d' ' | cut -f2 -d, | cut -f1 -d=)
            echo -n "$opt "
        fi
    done
}

#========================================
# __azure_cli_commands
#----------------------------------------
function __azure_cli_commands {
    local begin=0
    local commands
    local mode
    if [ ! $1 = "azurecli" ]; then
        mode=$1
    fi
    azure-cli $mode --help | while read line; do
        if [[ "$line" =~ ^commands: ]];then
            begin=1
        elif [ $begin -eq 1 ];then
            if [ -z "$line" ]; then
                begin=0
            else
                cmd=$(echo $line | cut -f1 -d' ')
                echo -n "$cmd "
            fi
        fi
    done
}

complete -F _azure_cli azure-cli
