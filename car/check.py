import os
import json
from django.utils import timezone
from datetime import timedelta

class Api_calls:
    @staticmethod
    def get_api(query, table_name):
        try:
    
            master_obj, created = Master_Table_List.objects.get_or_create(Table_Name=table_name)

            # Get current time
            current_time = timezone.now()
            local_time = timezone.localtime(current_time)

            # Get the duration for the refresh check (in hours)
            duration = int(master_obj.Duration)
            if not duration:
                duration = 2  # Default duration to 2 hours if not set

            # Path to the file that stores the data
            file_path = os.path.join(settings.BASE_DIR, 'Datas_file', f'{table_name}.txt')

            # Check if we should update the data (if newly created or data is older than the given duration)
            if created or (local_time - master_obj.Last_Update > timedelta(hours=duration)):
                # Fetch new data from the database if it was posted or updated
                data = api_methods.get_common(query)

                if data:
                    # Serialize the data
                    serial_data = serialize.serial(data)

                    # Update the master object with new data timestamp and status
                    master_obj.Last_Update = local_time
                    master_obj.New_Update = 'Yes'
                    master_obj.save()

                    # Ensure the directory exists for storing the data file
                    if not os.path.exists(os.path.dirname(file_path)):
                        os.makedirs(os.path.dirname(file_path))

                    # Write the serialized data to the file
                    with open(file_path, 'w') as file:
                        json.dump(serial_data, file, indent=3)

                    # Return success response with the new data
                    success_data = {
                        "Result": 1,
                        "Message": "Success",
                        "Api-result": serial_data
                    }
                    return success_data

            # If the file exists and has data, use the data from the file
            if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                # Mark the update status as 'No' since the file data is being used (no new updates)
                master_obj.New_Update = 'No'
                master_obj.save()  # Save the status update to the database

                # Read the data from the file
                with open(file_path, 'r') as file:
                    data = json.load(file)

                # Return success response with the data from the file
                success_data = {
                    "Result": 1,
                    "Message": "Success",
                    "Api-result": data
                }
                return success_data

            # Return failure if no valid file or data is available
            return {
                "Result": 1,
                "Message": "Fails",
                "Api-result": "No File Data"
            }

        except Exception as err:
            # Return failure response if there's an error
            return {
                "Result": 0,
                "Message": "Fail to Get",
                "Api-result": str(err)
            }
