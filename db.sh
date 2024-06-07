# Initialize the migrations directory
flask db init

# Create the initial migration script
flask db migrate -m "Initial migration."

# Apply the initial migration to the database
flask db upgrade