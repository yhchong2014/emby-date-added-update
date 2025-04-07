## Description

This repository automates the process of updating the `DateAdded` field for media items in an Emby server using the Emby API. The goal of this script is to ensure that the "Date Added" field matches the release date of the media. The script can be run either manually or automatically based on a schedule.

### Features:
- **Automatic Date Update**: The script fetches items from your Emby server and updates the `DateAdded` field based on the media’s premiere date.
- **Scheduled Runs**: The workflow is scheduled to run automatically at 12:00 PM UTC every day.
- **Manual Trigger**: You can also trigger the script manually through GitHub Actions.
- **Customization**: You can customize the script by adding your own library IDs, and the script will update all items in those libraries.

---

### Setup Instructions:

1. **Add Secrets to GitHub Repository**:
   - Go to the repository settings.
   - Under `Secrets and variables`, navigate to `Actions`, then click `New repository secret`.
   - Add the following secrets:
   | Variable       | Description                                                                 |
   |----------------|-----------------------------------------------------------------------------|
   | `EMBY_API_KEY` | Go to the Emby API and generate one.                                        |
   | `EMBY_HOST`    | Your own Emby public address.                                                |
   | `EMBY_USER_ID` | Go to the Emby server user, select the host user, and copy the user ID from the URL. |
   
2. **Configure Library IDs**:
   - Open `update_emby_dates.py` and replace the library IDs with your own.
   - To find the library ID, click on your Emby library, observe the URL, and look for `parentId=xxx` — where `xxx` is your library ID.

3. **Run the Workflow**:
   - Go to the **Actions** tab in your GitHub repository.
   - Select **Emby Date Updater**.
   - Click on **Run workflow** to manually trigger the update process.

---

## Disclaimer

- This code has been modified with the help of GPT, as I am not familiar with coding.
- The original reference for this code is from [MoviePilot-Plugins by jxxghp](https://github.com/jxxghp/MoviePilot-Plugins).
- Use this code at your own risk. Always test in a safe environment and back up important data before running the code.
- Not responsible for any data loss, damage, or other issues that may occur when using this code.

---
