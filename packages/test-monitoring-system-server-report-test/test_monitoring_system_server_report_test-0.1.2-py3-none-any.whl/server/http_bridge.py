from flask import Flask, render_template, jsonify
import psycopg2
from config_loader import main

# Flask setup
app = Flask(__name__)

# Load configuration
config = main()

if config:
    DB_NAME = config.get("DB_NAME")
    USER = config.get("USER")
    PASSWORD = config.get("PASSWORD")
    HOST = config.get("HOST", "localhost")
    PORT = int(config.get("PORT", 5432))

# Function to clear the database
def clear_database():
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT
        )
        cursor = conn.cursor()

        # Close the database connection
        conn.close()
        print("Database cleared successfully!")

    except Exception as e:
        print(f"Error clearing the database: {e}")

# Function to fetch metrics from the database
def get_data_from_db():
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT
        )
        cursor = conn.cursor()

        # Fetch the latest stored data (limit 5 rows)
        cursor.execute("SELECT * FROM metrics ORDER BY id DESC LIMIT 1000;")
        rows = cursor.fetchall()

        # Clear all records from the `metrics` table
        cursor.execute("TRUNCATE TABLE metrics;")
        conn.commit()

        # Close the database connection
        conn.close()

        # Return rows as a list of dictionaries
        metrics = [
            {
                "hostname": row[2],  # hostname column
                "metric": row[3],    # metric column
                "value": row[4],     # value column
                "timestamp": row[1]  # timestamp column
            }
            for row in rows
        ]

        return metrics

    except Exception as e:
        print(f"Error fetching data from PostgreSQL: {e}")
        return []

@app.route('/')
def index():
    metrics = get_data_from_db()
    return render_template("dashboard.html", metrics=metrics)

# Run Flask server on port 8000
if __name__ == "__main__":
    # Clear the database before starting the Flask app
    clear_database()
    app.run(port=8000, host="0.0.0.0", debug=True)

