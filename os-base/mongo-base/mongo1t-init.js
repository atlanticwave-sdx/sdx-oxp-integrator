print('#################### Start Creating Databases ####################');

rs.initiate()

admin_db = db.getSiblingDB('admin')
admin_db.createUser(
  {
    user: "admin_user",
    pwd: "admin_pwd",
    roles: [
        {
          role: "root",
          db: "admin"
        }
    ]
  }
);


amlight_db = db.getSiblingDB('amlight')

amlight_db.createUser(
  {
    user: "amlight_user",
    pwd: "amlight_pwd",
    roles: [
        {
          role: "readWrite",
          db: "amlight"
        }
    ]
  }
);

db = db.getSiblingDB('sax')

db.createUser(
  {
    user: "sax_user",
    pwd: "sax_pwd",
    roles: [
        {
          role: "readWrite",
          db: "sax"
        }
    ]
  }
);

db = db.getSiblingDB('tenet')

db.createUser(
  {
    user: "tenet_user",
    pwd: "tenet_pwd",
    roles: [
        {
          role: "readWrite",
          db: "tenet"
        }
    ]
  }
);

rs.add("mongo2t:27028")
rs.add("mongo3t:27029")
