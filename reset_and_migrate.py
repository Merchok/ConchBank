import database

if __name__ == "__main__":
    print("Resetting database and migrating data from JSON...")
    
    # Re-initialize database and force recreate all tables
    database.initialize_database(force_recreate=True)
    
    # Migrate data from JSON files
    success = database.migrate_data_from_json()
    
    if success:
        print("Migration completed successfully!")
        print("Your data has been transferred to the SQLite database.")
    else:
        print("Migration failed. Please check if the JSON files exist.")
