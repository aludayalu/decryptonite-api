from flask import Flask,request,make_response
import os
import json
from hashlib import sha256
app = Flask(__name__)

total_levels=2

def valid_player(name,pwd):
    if os.path.exists(f"players/{name}"):
        if json.loads(open(f"players/{name}").read())["pwd"]==pwd:
            return True

def safe(name):
    if os.path.exists(f"players/{name}"):
        if json.loads(open(f"players/{name}").read())["status"]=="safe":
            return True

@app.route("/login")
def login():
    args=dict(request.args)
    args_keys=list(args.keys())
    if "school" in args_keys and os.path.exists(f"schools/{args['school']}"):
        return json.dumps(json.loads(open(f"schools/{args['school']}").read()))
    return "false"

@app.route("/addplayer")
def add_player():
    args=dict(request.args)
    args_keys=list(args.keys())
    if "school" in args_keys and os.path.exists(f"schools/{args['school']}") and "uname" in args_keys and "pwd" in args_keys:
        if os.path.exists(f"players/{args['uname']}") and len(str(args['pwd']).replace(" ",""))!=0:
            return "False"
        details=json.loads(open(f"schools/{args['school']}").read())
        open(f"players/{args['uname']}","a").write(json.dumps({"school":args['school'],"pwd":args['pwd'],"status":"safe","privelege":"player","stage":0}))
        details["players"].append(args["uname"])
        open(f"schools/{args['school']}","w+").write(json.dumps(details))
        return "True"
    return "False"

@app.route("/removeplayer")
def rem_player():
    args=dict(request.args)
    args_keys=list(args.keys())
    if "school" in args_keys and os.path.exists(f"schools/{args['school']}") and "uname" in args_keys:
        if not os.path.exists(f"players/{args['uname']}") and len(str(args['pwd']).replace(" ",""))!=0:
            return "False"
        os.remove(f"players/{args['uname']}")
        details=json.loads(open(f"schools/{args['school']}").read())
        details["players"].remove(args["uname"])
        open(f"schools/{args['school']}","w+").write(json.dumps(details))
        return "True"
    return "False"

@app.route("/disqualify")
def dq():
    args=dict(request.args)
    args_keys=list(args.keys())
    if "admin" in args_keys and "pwd" in args_keys and os.path.exists(f"players/{args['admin']}") and json.loads(open(f"players/{args['admin']}").read())["privelege"]=="admin" and json.loads(open(f"players/{args['admin']}").read())["pwd"]==args["pwd"] and "uname" in args_keys:
        player_stats=json.loads(open(f"players/{args['uname']}").read())
        player_stats["status"]="disqualified"
        open(f"players/{args['uname']}","w+").write(json.dumps(player_stats))
        return "True"
    return "False"

@app.route("/makeadmin")
def make_admin():
    args=dict(request.args)
    args_keys=list(args.keys())
    if "admin" in args_keys and "pwd" in args_keys and os.path.exists(f"players/{args['admin']}") and json.loads(open(f"players/{args['admin']}").read())["privelege"]=="admin" and json.loads(open(f"players/{args['admin']}").read())["pwd"]==args["pwd"] and "uname" in args_keys:
        player_stats=json.loads(open(f"players/{args['uname']}").read())
        player_stats["privelege"]="admin"
        open(f"players/{args['uname']}","w+").write(json.dumps(player_stats))
        return "True"
    return "False"

@app.route("/level")
def fetch_level():
    args=dict(request.args)
    args_keys=list(args.keys())
    if "uname" in args_keys and "pwd" in args_keys and valid_player(args["uname"],args["pwd"]) and safe(args["uname"]):
        player_level=json.loads(open(f"players/{args['uname']}").read())["stage"]
        return json.loads(open(f'levels/{player_level}').read())["question"]
    return "False"

@app.route("/submit")
def submit_level():
    args=dict(request.args)
    args_keys=list(args.keys())
    if "uname" in args_keys and "pwd" in args_keys and "answer" in args_keys and valid_player(args["uname"],args["pwd"]) and safe(args["uname"]):
        player_level=json.loads(open(f"players/{args['uname']}").read())["stage"]
        if json.loads(open(f'levels/{player_level}').read())["answer"]==args["answer"]:
            if total_levels>(player_level+1):
                details=json.loads(open(f"players/{args['uname']}").read())
                details["stage"]+=1
                open(f"players/{args['uname']}","w+").write(json.dumps(details))
            return "True"
    return "False"

if __name__ == "__main__":
    app.run(debug=True)