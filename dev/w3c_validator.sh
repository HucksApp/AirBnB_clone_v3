#!/bin/bash




post(){
: '
post with curl
Usage:  analyse_html <header> <url> <file_path> 
'
    curr_dir=$(sudo pwd);
    m=$(curl -H $1 -X POST $2 -F file=@"$curr_dir/$3")
    echo "$m"
}

analyse_html(){
: '
post with curl
Usage:  analyse_html <header> <url> <file_path> 
'
    header="Content-Type:text/html;charset=utf-8"
    url=https://validator.w3.org/nu/?out=json
    result=$(post "$header" "$url" "$1")
    echo "$result"|  python3 -c "import sys, json; \
    messages=json.load(sys.stdin).get('messages', []); \
    res=['[{}:{}] {}'.format('$1', m['lastLine'], m['message']) for m in messages]; \
    print(res)"
    

}







analyse_html "web_static/1-index.html"


#header='Content-Type: text/html; charset=utf-8'
#url='https://validator.w3.org/nu/?out=json'
#post "$header" "$url" "web_static/0-index.html"
#echo $result | grep messages
