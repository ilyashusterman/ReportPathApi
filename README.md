# Usage

#### commands:

---
* Prepate python virtual interpreter via `virtualenv -p python3 venv`
* install python packages `pip install -r requirements.txt`
* set databases connections properly ( install mongod from https://docs.mongodb.com/manual/mongo/ firebase setup https://firebase.google.com/docs/admin/setup/ (python firebase-admin))
* run main `make run`
---

Documentation:
---
    General:
    --------
    
    
    flow:
        - convert each input to converted_input
        - store converted_input to mongoDB
        - store converted_input to firebase using firebase convention (incident-firebase) - no input validation needed    


    msg -> sys_msg rules:
    ---------------------
    1. all messages city origin is Las Vegas
    2. type: 
        ACCIDENT -> crash
        ALL_OTHER -> incident
    3. subtype:
        if type == crash:
            ACCIDENT_MAJOR -> major
            ACCIDENT_MINOR -> minor
        else:
            * -> minor
    4. location: use lat, lng instead of x, y
    5. if reliability bigger than 6 (exclusive) -> accurate is true
    6. if confidence * reliability > 20 -> accurate is true
    8. id is uuid
    9. timestamp is seconds


    store to firebase:
    ------------------
    1. color: 'red' for major incidents otherwise 'orange'
    2. title: "what happened"
    3. subtitle: street
    4. time: timestamp in milis
  