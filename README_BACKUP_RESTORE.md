# How to Download a Backup from Heroku and Restore to PostgreSQL Locally

This guide explains how to download a database backup from Heroku and restore it to a local PostgreSQL database.

---

## **Prerequisites**
1. **Heroku CLI**: Ensure the Heroku CLI is installed and you are logged in.
   ```bash
   heroku login
   ```
2. **PostgreSQL**: Ensure PostgreSQL is installed and running locally.
   ```bash
   pg_isready
   ```

---

## **Step 1: Create a Backup on Heroku**
1. Trigger a backup of your Heroku database:
   ```bash
   heroku pg:backups:capture --app <your-app-name>
   ```
   Replace `<your-app-name>` with the name of your Heroku app.

2. Check the status of the backup:
   ```bash
   heroku pg:backups --app <your-app-name>
   ```

---

## **Step 2: Download the Backup**
1. Download the backup file:
   ```bash
   heroku pg:backups:download --app <your-app-name>
   ```
   This will download the backup as a `.dump` file to your current directory.

2. Move the file to a secure location (optional):
   ```bash
   mv latest.dump backups/
   ```

---

## **Step 3: Initial Creation of the Local Database**
1. Ensure the PostgreSQL server is running:
   ```bash
   brew services start postgresql  # macOS
   sudo service postgresql start  # Linux
   ```

2. Create a new database locally:
   ```bash
   createdb <local-database-name>
   ```
   Replace `<local-database-name>` with the name of your local database.

3. Restore the backup file to the new database:
   ```bash
   pg_restore --verbose --clean --no-acl --no-owner -h localhost -U <your-username> -d <local-database-name> <path-to-dump-file>
   ```
   Replace:
   - `<your-username>` with your PostgreSQL username.
   - `<local-database-name>` with the name of your local database.
   - `<path-to-dump-file>` with the path to the `.dump` file.

4. Verify the restore process by connecting to the database:
   ```bash
   psql -h localhost -U <your-username> -d <local-database-name>
   ```

5. Check the tables and data:
   ```sql
   \dt
   SELECT * FROM <table-name> LIMIT 10;
   ```

---

## **Step 4: Update an Existing Local Database**
If the local database already exists, you can overwrite it with the latest backup:

1. Restore the backup file to the existing database:
   ```bash
   pg_restore --verbose --clean --no-acl --no-owner -h localhost -U <your-username> -d <local-database-name> <path-to-dump-file>
   ```
   Replace:
   - `<your-username>` with your PostgreSQL username.
   - `<local-database-name>` with the name of your local database.
   - `<path-to-dump-file>` with the path to the `.dump` file.

2. Verify the restore process by connecting to the database:
   ```bash
   psql -h localhost -U <your-username> -d <local-database-name>
   ```

3. Check the tables and data:
   ```sql
   \dt
   SELECT * FROM <table-name> LIMIT 10;
   ```

---

## **Notes**
- Always back up your Heroku database before making significant changes.
- Ensure sensitive data is not exposed when sharing or storing backup files.
- Use `.gitignore` to exclude backup files from version control:
  ```
  backups/*
  *.dump
  ```