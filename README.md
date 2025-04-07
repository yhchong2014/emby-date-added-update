1. Go to respository settings --> secrets and variables --> actions --> new respository secret

2. 
| Variable       | Description                                                                 |
|----------------|-----------------------------------------------------------------------------|
| `EMBY_API_KEY` | Go to the Emby API and generate one.                                        |
| `EMBY_HOST`    | Your own Emby public address.                                                |
| `EMBY_USER_ID` | Go to the Emby server user, select the host user, and copy the user ID from the URL. |

3. Open update_emby_dates.py and replace with your library ids
   Click on your emby library --> observe the link and look for parentId=xxx, xxx is your library id

4. Click Actions --> Emby Date Updater --> Run workflow

## Disclaimer

- This code has been modified with the help of GPT, as I am not familiar with coding.
- The original reference for this code is from [MoviePilot-Plugins by jxxghp](https://github.com/jxxghp/MoviePilot-Plugins).
- Use this code at your own risk. Always test in a safe environment and back up important data before running the code.
- Not responsible for any data loss, damage, or other issues that may occur when using this code.
