#!/bin/bash

mongosh <<EOF
use admin;
db.createUser({user: "martin", pwd: "rampouch", roles:[{role: "root", db: "admin"}]});
exit;
EOF