from agentCores import agentCores

def runMigration():
    try:
        # Initialize agentCores with MongoDB connection
        core = agentCores()
        
        # Run migration
        print("Starting migration...")
        core.migrateAgentCores()
        print("Migration completed.")
        
    except Exception as e:
        print(f"Error during migration: {str(e)}")

if __name__ == "__main__":
    runMigration()