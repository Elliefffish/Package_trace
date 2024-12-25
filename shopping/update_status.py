import sqlite3
import time
import datetime

def update_package_periodically(package_id = '', min=3):
    conn = sqlite3.connect('shopping.db')
    cursor = conn.cursor()

    #package_id = set()  # Keep track of processed package_ids

    while package_id != '' :
        # Fetch the latest package_id from the Status table
        cursor.execute("SELECT status_id FROM Packages WHERE package_id = (?)", (package_id,))
        current_status_id = cursor.fetchone()[0]

        # Check if the latest_package_id is new and not processed yet
        if current_status_id !=None and current_status_id > 1:
            # Update the Package table
            cursor.execute("UPDATE Packages SET status_time = ?, status_id = ? WHERE package_id = ?", (datetime.datetime.now(), current_status_id-1, package_id))
            conn.commit()
        else:
            break

            #package_id.add(latest_package_id)  # Mark as processed

        time.sleep(10*min)  # Wait for 3 minutes (180 seconds)

    conn.close()  # Close the connection (this line will only be reached if the loop breaks)

# Start the periodic update process
update_package_periodically('PKG9691', 1)
