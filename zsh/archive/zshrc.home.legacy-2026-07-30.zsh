# Use powerline
USE_POWERLINE="true"
# Source manjaro-zsh-configuration
if [[ -e /usr/share/zsh/manjaro-zsh-config ]]; then
  source /usr/share/zsh/manjaro-zsh-config
fi
# Use manjaro zsh prompt
if [[ -e /usr/share/zsh/manjaro-zsh-prompt ]]; then
  source /usr/share/zsh/manjaro-zsh-prompt
fi

#konsolle
#zle -N other-window
#bindkey '^[[27;5;9~' other-window
# NEW TO ACTUALISE
#confirm actualisation with date
alias ssr='simplescreenrecorder & disown'

#aliases

#flex
alias mm='cmatrix';

## larva
alias lvdv="/home/hruzam/www/ovum/larva.dev/dev && ls -lathr"

#General
alias patch='git stash show "stash@{0}" -p > changes.patch';
alias ddb='echo "/home/hruzam/Downloads/"';
alias ftp='subl /mnt/manjaro_data/X00_Imago/fantasyobchod_moje_pozn/SFTP_server_setup.txt -a &'
alias gpt='git stash show -p stash@{0} > temp.patch'
alias dsk='wmctrl -s' 
alias sub2='subl --layout 2_columns &'
alias alf="cd && subl -n -a .zshrc &"
alias alf1="cd && subl -n -a .tmux.conf"
alias src="source ~/.zshrc"
#alias src1="tmux source-file ~/.tmux.conf"
alias akt="/usr/bin/php74 /usr/bin/composer update" #rucne composer.json composer.lock (muzes porovnat s ostrou a doplnit z ostre rucne)
alias t12='subl -n -a ~/www/fantasyobchod/catalog/controller/process/ModelTest.php ~/www/fantasyobchod/catalog/controller/process/ControllerTest.php ~/www/fantasyobchod/catalog/controller/process/ViewTest.tpl ~/www/DB_mysql_apod/SQL_cvicne.sql &'
alias t13='subl -n -a ~/www/fantasyobchod_moje_pozn/00_ZeroToHero.txt'
alias t0='t12 && alf'
alias hasz='openssl rand -hex 12 | cut -c 1-21';
alias dbup='mysql -u root -p';
alias dbfo="fo && /usr/bin/mariadb -u majkee -p fantasyobchod"
alias dbim="im && mysql -u root -p "
alias svt='mkdir -p /home/hruzam/log && history -i >> ~/log/_terminal.txt'
alias svt1='script ~/log/_terminal.txt'
alias ord='ls -lthr'
alias cod="php -r 'echo uniqid(). PHP_EOL;'"

#browsers
alias ffxn='firefox -new-window https://www.google.com &'
alias ffxl='ffoxLocal &' #open local DTB
alias ffxp='ffoxProduction &' #open production DTB
alias ffgpt='ffoxChatGpt &' #open Open AI Chat GPT



#PHP
alias fpm7='sudo systemctl stop php-fpm && sudo systemctl restart php74-fpm'
alias fpm='sudo systemctl stop php74-fpm && sudo systemctl restart php-fpm'

#HDD
alias btr0="upower -i $(upower -e | grep 'BAT')"
alias btr1="upower -i $(upower -e | grep 'BAT') | grep percentage | awk '{print $2}'"


#Appi
alias res="cd && echo 'responsively mode' && ~/AppImage && ./ResponsivelyApp-1.8.0.AppImage &"

#StroMyAliases
alias stm='cd ~/www/StroMy/StroMy'
alias gl2='fo && git pull'
alias gd2='stm && git add $(ExtractBetweenTags ~/www/StroMy/DailyScrum.txt "*s" "*f" "*m") && git status'
alias gnt2='stm && AddDailyScrum ~/www/StroMy/DailyScrum.txt "neconeco"'
alias gt2='stm && git commit -m "$(ExtractBetweenTags ~/www/StroMy/DailyScrum.txt "*m" "*n" "*s")"'
alias grt2='git reset'
alias gph2='git push git@github.com:hruzam/StroMy.git'

#FantasyObchodAliases
#alias fo="cd ~/www/fantasyobchod"
alias rfo="fo && subl &"
alias gs1="fo && git status"
alias gh1="fo && git stash"
alias gl1="fo && git pull"
alias ge1="fo && subl .gitignore &"
alias gg1="fo && git stash && git pull && subl &"
alias gd1='fo && git add $(ExtractBetweenTags ~/www/fantasyobchod_moje_pozn/DailyScrum.txt "*s" "*f" "*m") && git status'
alias gt1='fo && git commit -m "$(ExtractBetweenTags ~/www/fantasyobchod_moje_pozn/DailyScrum.txt "*m" "*n" "*s")"'
alias grt1='fo && git reset'
alias gph1='fo && git push'
alias gnt1='AddDailyScrum ~/www/StroMy/DailyScrum.txt "neconeco"'
alias fup="subl ~/www/fantasyobchod_moje_pozn/SFTP_server_setup.txt && filezilla &"
alias kup="pkill filezilla"
alias va74='echo "120922@Imago" | valet use php74'
alias fost="globalFantasyobchodStartScript"
alias heu="fo && dsk 2; subl -a cron/heureka-ostra.xml"

#new aliases dedicated to projects later
alias p7="valet use php74"
alias p8="valet use php8"

#ImagoAliases
#alias im="cd ~/www/freya"
alias imx='im && subl --n ~/www/freya_moje_poznamky/zero-to-hero.txt'
alias seeder='php artisan db:seed'
alias che="php artisan view:clear; php artisan cache:clear; php artisan config:clear"
alias gpl="git pull && npm run build && php artisan optimize:clear"
alias mig="time php artisan migrate:fresh --seed" # NOT refresh

#commonLaravelAliases
alias art='php artisan'
alias tinker='php artisan tinker'
alias migrate='php artisan migrate'
alias serve='php artisan serve'
alias optimize='php artisan optimize:clear'

#psdvsAliases
alias dbps="fo && /usr/bin/mariadb -u majkee -p psdvs"
alias psdvs="cd && /media/data/projects/psdvs"
alias psdvs_zsh="cp ~/.zshrc /media/data/projects/psdvs/monkeyEnv"
alias psd_="/media/data/projects/psdvs && dsk 2; code & disown"


#alternative Fantasyobchod
alias mkay="cd && /media/data/projects/monkey_fantasy/fantasyobchod && git status"

#Dochazka
alias doc="~/www/fantasyobchod_moje_pozn/dochazka && nano dochazka.txt"

#FunctionTest
alias fcet='TestVypisu'


# =============================================================================
# PROJECT SWITCHER SYSTEM
# =============================================================================
# 1. Load machine-specific config FIRST
[[ -f ~/.config/zsh/config.zsh ]] && source ~/.config/zsh/config.zsh

# 2. Load project switcher (uses config variables)
[[ -f ~/.config/zsh/project-switcher.zsh ]] && source ~/.config/zsh/project-switcher.zsh

# 3. Sync my terminal/php environment
[[ -f ~/.config/zsh/env-sync.zsh ]] && source ~/.config/zsh/env-sync.zsh

# 4. Git Lifecycle System
[[ -f ~/.config/zsh/git-lifecycle.zsh ]] && source ~/.config/zsh/git-lifecycle.zsh

#following comands not under maintenance
#@2026_02_10HRU>
# =============================================================================
# Rest is unmaintained
# =============================================================================



#Systemove nastroje

# fce stahne z URL a ulozi instalacni baliky
# podle parametru v csv sestavi nazev souboru i adresu stazeni
alias down_pack='function __download_packages'

# Alias to call the function conveniently
alias upconfiles='update_conflicted_files'

#functions

#open loacal database
function ffoxLocal() {

    # Get the current virtual desktop number
    local desktop="$(dsk | awk '{print $NF}')"

    if pgrep firefox; then
        firefox -new-tab 'http://fantasyobchod.l/adminer?username=root&db=fantasyobchod&sql=' 
    else
        firefox -new-window 'http://fantasyobchod.l/adminer?username=root&db=fantasyobchod&sql=' 
    fi
}

#open database
function ffoxProduction() {

    # Get the current virtual desktop number
    local desktop="$(dsk | awk '{print $NF}')"

    if pgrep firefox; then
        firefox -new-tab 'https://www.imago.cz/adminer/?username=c0main_db_user&db=c0main_database&dump=' 
    else
        firefox -new-window 'https://www.imago.cz/adminer/?username=c0main_db_user&db=c0main_database&dump=' 
    fi
}

function ffoxChatGpt() {
    # Default to virtual display 0 if no argument is provided
    local display_num=$(dsk | awk '{print $NF}' || echo 0)

    # Check if Firefox is running on the specified virtual display
    #if firefox_virtual_displays | grep -q "$display_num"; then
        # Switch to the specified virtual display
        #wmctrl -o $((display_num * 1920)),$((display_num * 1080))
    if wmctrl -l | grep -q "Mozilla Firefox"; then
        # Open a new tab in the existing Firefox window
        firefox -new-tab 'https://chatgpt.com/?oai-dm=1' 
    else
        # Open a new Firefox window on the specified virtual display
        wmctrl -s "$display_num"
        firefox -new-window 'https://chatgpt.com/?oai-dm=1' 
    fi
}


function firefox_virtual_displays() {
    # Get the list of windows and their desktop numbers
    window_list=$(wmctrl -l)

    # Extract desktop numbers where Firefox is running
    firefox_displays=$(echo "$window_list" | grep "Firefox" | awk '{print $2}')

    # Remove duplicate entries
    unique_displays=$(echo "$firefox_displays" | tr ' ' '\n' | sort -u)

    echo "$unique_displays"
}



#find like sublime "ctrl+shift+f"

# Definice aliasu pro grep s rekurzivním hledáním a zobrazením čísel řádků
#call it by terminal 'msrc'
alias mygrep='grep -Hrn'

# Funkce mysearch s definovanou statickou cestou k adresáři
function msrc() {
    mygrep "$1" "/home/hruzam/www/fantasyobchod"
}


# Function to update conflicting files and identify owning packages
update_conflicted_files() {
    # File to store conflicting files
    conflicting_files_file="/tmp/conflicting_files.txt"
    # File to store results
    results_file="/tmp/owning_packages.txt"

    # Run pacman with -Syyu and save output
    sudo pacman -Syyu --noconfirm 2>&1 | tee /tmp/pacman_update_output.txt

    # Extract conflicting files and save them to a file
    grep "exists in filesystem" /tmp/pacman_update_output.txt | cut -d ":" -f 2- > "$conflicting_files_file"

    # Loop through each conflicting file, identify owning package, and save results
    while IFS= read -r conflicting_file; do
        echo "Conflicting file: $conflicting_file"
        # Check if any package owns the file
        owning_package=$(pacman -Qo "$conflicting_file" 2>/dev/null)
        if [ -n "$owning_package" ]; then
            echo "$owning_package" >> "$results_file"
        else
            echo "No package owns $conflicting_file" >> "$results_file"
        fi
    done < "$conflicting_files_file"

    # Print message to review results
    echo "Owning packages for conflicting files have been identified. Please review the results in $results_file."

    # Clean up conflicting files file
    rm "$conflicting_files_file"
}


# ulozeni baliku pro instalaci pacman
# Funkce pro stahování balíčků
function __download_packages() {
    # Kontrola počtu argumentů
    if [ "$#" -ne 2 ]; then
        echo "Usage: download_packages <download_dir> <source_csv>"
        return 1
    fi

    # Složka pro stahování
    download_dir="$1"

    # Zdrojové CSV souboru
    source_csv="$2"

    # Definice oddělovače
    delimiter=","

    # Načtení CSV souboru a zpracování jednotlivých řádků
    while IFS="$delimiter" read -r param1 param2 param3 param4; do
        # Název balíčku
        package_name="${param3}.pkg.tar.zst"

        # Sestavení URL adresy
        url="${param1}${param2}/${param3}/${param4}/${package_name}"

        # Stažení balíčku
        wget -P "$download_dir" "$url"
    done < "$source_csv"
}


# definice funkce ExtractBetweenTags pro .zshrc
function ExtractBetweenTags() {
    local file=$1
    local start_tag=$2
    local end_tag=$3
    local mid_tag=$4
    local in_text=0
    local out=""
    local cur_line=""
    while read cur_line; do
        # ignoruje komentare a prazdne radky
        if [[ $cur_line =~ ^[[:space:]]*# || -z $cur_line ]]; then
            continue
        fi
        
        # najde prvni vyskyt zacatecniho tagu
        if [[ $cur_line == *$start_tag* && $in_text -eq 0 ]]; then
            in_text=1
            cur_line=${cur_line#*$start_tag}  # odstranime text pred zacatecnim tagem
        fi
        
        # najde vyskyt koncoveho tagu
        if [[ $cur_line == *$end_tag* && $in_text -eq 1 ]]; then
            in_text=0
            out="${out}${cur_line%$end_tag*}"  # ulozime text pred koncovym tagem
            break  # ukoncime cyklus po nalezeni koncoveho tagu
        fi
        
        # najde vyskyt prostredniho tagu
        if [[ $cur_line == *$mid_tag* && $in_text -eq 1 ]]; then
            in_text=0
            break  # ukoncime cyklus pri nalezeni prostredniho tagu
        fi
        
        # ulozi text mezi zacatecnim a koncovym tagem
        if [[ $in_text -eq 1 ]]; then
            # odstrani text pred zacatecnim tagem
            cur_line=${cur_line#*$start_tag}
            out="${out}${cur_line%$end_tag*} "  # pridame mezery mezi jednotlivymi retezci
        fi
    done < $file
    
    echo "$out"
}

function AddDailyScrum() {
    local daily_scrum_file="/home/hruzam/www/StroMy/DailyScrum.txt"
    local commit_message="${2:-Fill manualy, please}"
    local today="$(date +%F)"
    local add_files="${3:-Fill manualy, please}"
    
    # search for the history tag and move down 10 lines
    local history_line=$(grep -n "<history>" "$daily_scrum_file" | cut -d ":" -f 1)
    ((history_line+=10))
    
    # check if the history line exists
    if [[ $(sed "${history_line}q;d" "$daily_scrum_file") == *"Daily Scrum nr."* ]]; then
        # get the current daily scrum number
        local current=$(sed "${history_line}q;d" "$daily_scrum_file" | grep -oP '\d+')
        ((next=current+1))
    else
        next=1
    fi
    
   
    # insert the new daily scrum entry into the file
    local entry="Daily Scrum nr.${next} \n************************\n
      date: ${today}\n*m ${commit_message} *n\n*s ${add_files} *f\n*end*"

    sed -i -e "${history_line}i\\" -e "$entry"
}


function TestVypisu() {
# Získání seznamu změněných a přidaných souborů
    git status --porcelain | awk '$1 == "M" || $1 == "A" {print $2}' > ~/www/changes.txt
      if [ -s ~/www/changes.txt ]; then
        add_files=$(cat ~/www/changes.txt)
      else
        add_files="Fill manually, please"
      fi
      #rm ~/www/changes.txt
    echo "$add_files"
}

function switch_php() {
    if [[ $1 == "7.4" ]]; then
        sudo update-alternatives --set php /usr/bin/php7.4
        echo "Switched to PHP 7.4"
    elif [[ $1 == "8.0" ]]; then
        sudo update-alternatives --set php /usr/bin/php8.0
        echo "Switched to PHP 8.0"
    else
        echo "Usage: switch_php {7.4|8.0}"
    fi
    php -v
}

function globalFantasyobchodStartScript() {

    #1.use propper valet configuration
    echo 'starting propper valet configuration...'
    valet use 74
    #2.switch to fo-git directory
    echo 'doing git "things"'
    #Y/N?
    #if there is something to commit...{
    #ask for added files
    #ask for staged files
    #} 
    
    #Y/N?
    #aupdate database? product, category, order themes
    #individual confirming which one?

    #do something for filezilla
    #"host": "fantasyobchod.cz",
    #"user": "defaultfan",
    #"password": "<REDACTED-2026-07-30 — rotate this credential>",
    #"port": "21",

} 
#source /usr/share/nvm/init-nvm.sh
#source /usr/share/nvm/init-nvm.sh
#export PATH=~/.npm-global/bin:$PATH
export PATH=~/.npm-global/bin:$PATH
export PATH=~/.npm-global/bin:$PATH


### ADHOC TEMP ###
colafi() {

# cd && npx repomix --config www/session/larva/scratch/repomix.larva_runtime_companion.json --output www/session/larva/scratch/larva_runtime_companion_repomix..xml
# cd && npx repomix --config www/session/larva/scratch/repomix.larva_runtime_companion.json --style markdown --output www/session/larva/scratch/larva_runtime_companion_repomix.md
# # --output www/session/larva/scratch/larva_runtime_companion_repomix..md

# cd && npx repomix --config www/session/larva/scratch/repomix.larva_core.json --style markdown --output www/session/larva/scratch/larva_core_repomix.md
# cd && npx repomix --config www/session/larva/scratch/repomix.larva_core.json --output www/session/larva/scratch/larva_core_repomix.xml

#
# Create a staging directory
#STAGE=/home/hruzam/www/session/_stage_for_agents
#rm -rf "$STAGE" && mkdir -p "$STAGE"
#
#cp -r ~/.cursor/
#cp -r ~/.config/gemini/agents/
#cp -r ~/.config/gemini/bin/
#cp -r ~/.config/claude/bin/
#cp -r ~/.claude/CLAUDE.md
#cp -r ~/.claude/agents/
#cp -r ~/.claude/commands/
#cp -r ~/.gemini/projects.json
#cp -r ~/.gemini/GEMINI.md
#cp -r ~/www/session/.shared/

cp -r -v /home/hruzam/www/session/_scrum/dot.shared@skills/skill.frame-larva.md /home/hruzam/www/session/.shared/skills
cp -r -v /home/hruzam/www/session/_scrum/dot.shared@skills/skill.honest.md /home/hruzam/www/session/.shared/skills
cp -r -v /home/hruzam/www/session/_scrum/dot.shared@skills/skill.learn-repomix.md /home/hruzam/www/session/.shared/skills
cp -r -v /home/hruzam/www/session/_scrum/dot.shared@skills/skill.load-from-destination.md /home/hruzam/www/session/.shared/skills
cp -r -v /home/hruzam/www/session/_scrum/dot.shared@skills/skill.naming-convention.md /home/hruzam/www/session/.shared/skills
cp -r -v /home/hruzam/www/session/_scrum/dot.shared@skills/skill.regime-karpathy.md /home/hruzam/www/session/.shared/skills
cp -r -v /home/hruzam/www/session/_scrum/dot.shared@skills/skill.report-as-larva-scribe.md /home/hruzam/www/session/.shared/skills
cp -r -v /home/hruzam/www/session/_scrum/dot.shared@skills/skill.target-by-vector.md /home/hruzam/www/session/.shared/skills
cp -r -v /home/hruzam/www/session/_scrum/dot.shared@commands/command.commands-common-claude.ai.md /home/hruzam/www/session/.shared/commands

}
