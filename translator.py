import psycopg2
from translate  import Translator

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host="localhost",
    database="data-dashboard",
    user="nima",
    password=""
)
cur = conn.cursor()

# Retrieve all English texts from the database
cur.execute("SELECT id, name FROM countries")
records = cur.fetchall()

# Loop through the records and translate each English text to Persian
translator = Translator(to_lang='fa')
for record in records:
    id = record[0]
    english_text = record[1]

    # Check if the Persian text already exists for this record
    cur.execute("SELECT persian_name FROM countries WHERE id = %s", (id,))
    result = cur.fetchone()
    if result and result[0]:
        print(f"Skipping record with id {id} because it already has a Persian translation")
        continue
    
    persian_text = translator.translate(english_text)
    
    # Update the corresponding record in the database with the Persian text
    cur.execute("UPDATE countries SET persian_name = %s WHERE id = %s", (persian_text, id))
    conn.commit()

# Close the database connection
cur.close()
conn.close()