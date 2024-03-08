-- This is the SQL code that creates the database tables for the app.
CREATE TABLE IF NOT EXISTS "django_migrations" (
"id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
"app" varchar(255) NOT NULL, 
"name" varchar(255) NOT NULL, 
"applied" datetime NOT NULL);

CREATE TABLE sqlite_sequence(name,seq);

-- These next three tables are crucial for the functioning of the app. 
-- They are the tables that store the user data, the rejected matches, and the matches.

-- The users table stores the user data.
CREATE TABLE IF NOT EXISTS "Bumble4Stem_users" (
"id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
"email" varchar(255) NOT NULL UNIQUE, 
"display_name" varchar(255) NOT NULL, 
"age" integer NOT NULL, 
"batch" varchar(255) NOT NULL, 
"phn_no" integer NOT NULL, 
"pronouns" varchar(255) NOT NULL, 
"research_interests" text NOT NULL, 
"bio" text NOT NULL);

-- The rejected table stores the user ids of the users who have rejected each other.
CREATE TABLE IF NOT EXISTS "Bumble4Stem_rejected" (
"id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
"r1id_id" integer NOT NULL REFERENCES "Bumble4Stem_users" ("id") DEFERRABLE INITIALLY DEFERRED, 
"r2id_id" integer NOT NULL REFERENCES "Bumble4Stem_users" ("id") DEFERRABLE INITIALLY DEFERRED);

-- The matches table stores the user ids of the users who have matched with each other.
CREATE TABLE IF NOT EXISTS "Bumble4Stem_matches" (
"id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
"m1id_id" integer NOT NULL REFERENCES "Bumble4Stem_users" ("id") DEFERRABLE INITIALLY DEFERRED, 
"m2id_id" integer NOT NULL REFERENCES "Bumble4Stem_users" ("id") DEFERRABLE INITIALLY DEFERRED);

-- The next few lines of code create the indexes for the tables.
CREATE INDEX "Bumble4Stem_rejected_r1id_id_da81dd0e" ON "Bumble4Stem_rejected" ("r1id_id");

CREATE INDEX "Bumble4Stem_rejected_r2id_id_8a03bc89" ON "Bumble4Stem_rejected" ("r2id_id");

CREATE INDEX "Bumble4Stem_matches_m1id_id_1f556deb" ON "Bumble4Stem_matches" ("m1id_id");

CREATE INDEX "Bumble4Stem_matches_m2id_id_212533aa" ON "Bumble4Stem_matches" ("m2id_id");

-- The next few tables are the default tables that Django creates when you run the command "python manage.py migrate".
CREATE TABLE IF NOT EXISTS "auth_group_permissions" (
"id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
"group_id" integer NOT NULL REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED, 
"permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE TABLE IF NOT EXISTS "auth_user_groups" (
"id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
"user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, 
"group_id" integer NOT NULL REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE TABLE IF NOT EXISTS "auth_user_user_permissions" (
"id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
"user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, 
"permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE UNIQUE INDEX "auth_group_permissions_group_id_permission_id_0cd325b0_uniq" ON "auth_group_permissions" ("group_id", "permission_id");

CREATE INDEX "auth_group_permissions_group_id_b120cbf9" ON "auth_group_permissions" ("group_id");

CREATE INDEX "auth_group_permissions_permission_id_84c5c92e" ON "auth_group_permissions" ("permission_id");

CREATE UNIQUE INDEX "auth_user_groups_user_id_group_id_94350c0c_uniq" ON "auth_user_groups" ("user_id", "group_id");

CREATE INDEX "auth_user_groups_user_id_6a12ed8b" ON "auth_user_groups" ("user_id");

CREATE INDEX "auth_user_groups_group_id_97559544" ON "auth_user_groups" ("group_id");

CREATE UNIQUE INDEX "auth_user_user_permissions_user_id_permission_id_14a6b632_uniq" ON "auth_user_user_permissions" ("user_id", "permission_id");

CREATE INDEX "auth_user_user_permissions_user_id_a95ead1b" ON "auth_user_user_permissions" ("user_id");

CREATE INDEX "auth_user_user_permissions_permission_id_1fbb5f2c" ON "auth_user_user_permissions" ("permission_id");

-- This table stores the logs of the admin.
CREATE TABLE IF NOT EXISTS "django_admin_log" (
"id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
"action_time" datetime NOT NULL, 
"object_id" text NULL, 
"object_repr" varchar(200) NOT NULL, 
"change_message" text NOT NULL, 
"content_type_id" integer NULL REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED, 
"user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, 
"action_flag" smallint unsigned NOT NULL CHECK ("action_flag" >= 0));

CREATE INDEX "django_admin_log_content_type_id_c4bce8eb" ON "django_admin_log" ("content_type_id");

CREATE INDEX "django_admin_log_user_id_c564eba6" ON "django_admin_log" ("user_id");

-- This table stores the content types of the users.
CREATE TABLE IF NOT EXISTS "django_content_type" (
"id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
"app_label" varchar(100) NOT NULL, 
"model" varchar(100) NOT NULL);

CREATE UNIQUE INDEX "django_content_type_app_label_model_76bd3d3b_uniq" ON "django_content_type" ("app_label", "model");

-- This table stores the permissions of the users.
CREATE TABLE IF NOT EXISTS "auth_permission" (
"id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
"content_type_id" integer NOT NULL REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED, 
"codename" varchar(100) NOT NULL, "name" varchar(255) NOT NULL);

CREATE UNIQUE INDEX "auth_permission_content_type_id_codename_01ab375a_uniq" ON "auth_permission" ("content_type_id", "codename");

CREATE INDEX "auth_permission_content_type_id_2f476e4b" ON "auth_permission" ("content_type_id");

-- This table stores the groups of the users.
CREATE TABLE IF NOT EXISTS "auth_group" (
"id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
"name" varchar(150) NOT NULL UNIQUE);

-- This table stores the user data on Django's side.
CREATE TABLE IF NOT EXISTS "auth_user" (
"id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
"password" varchar(128) NOT NULL, 
"last_login" datetime NULL, 
"is_superuser" bool NOT NULL, 
"username" varchar(150) NOT NULL UNIQUE, 
"last_name" varchar(150) NOT NULL, "email" varchar(254) NOT NULL, 
"is_staff" bool NOT NULL, "is_active" bool NOT NULL, 
"date_joined" datetime NOT NULL, "first_name" varchar(150) NOT NULL);

-- This table stores the sessions of the users.
CREATE TABLE IF NOT EXISTS "django_session" (
"session_key" varchar(40) NOT NULL PRIMARY KEY, 
"session_data" text NOT NULL, 
"expire_date" datetime NOT NULL);

CREATE INDEX "django_session_expire_date_a5c62663" ON "django_session" ("expire_date");