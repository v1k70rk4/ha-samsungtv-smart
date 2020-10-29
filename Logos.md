# HomeAssistant - SamsungTV Tizen Component

***Change/add logos***
---------------
Is there a missing logo for a TV channel or app that you frequently use and is this annoying you a lot? Read the steps below to update the information this component relies on to make matches.

The information used to match your media title against is from a source called [TMDB](https://www.themoviedb.org/). Next to knowing about movies and TV shows, this website also knows about most of the TV networks globally. However, their database is not perfect and you may find that a logo is outdated or simply missing.

Next to TMDB a manual set of logos is maintained for popular Samsung smart TV apps. 


***Add or update logo of TV channel in TMDB***
---------------

1. Register yourself [here](https://www.themoviedb.org/signup) and login to TMDB.
2. Search for your TV channel [here](https://www.themoviedb.org/search?query=).
3. Click on 'Networks' and see if it is listed (go to step 5 if it is listed).
4. If it is NOT listed:
  - Search for a TV show that is broadcasted on this TV channel.
  - In case you cannot find your TV show either, select a random one or create one that the TV network originally created by pressing the '+' on the top of the screen and clicking 'add TV show' and follow guidance to create the show.  
  - Click on the TV show and click 'Edit this page'.
  - Under 'Production information' look for Network.
  - Click on 'Add network'.
  - Type the name of the TV channel you wish to add, it should not be in the list so type in the name and click update.
  - Confirm if it asks whether you are sure to add this network to the database.
  - The newly created network should appear as part of the network information for the TV show.
  - You can open the newly created network by right-clicking on it and opening on a seperate tab to make the further edits as described in step 5.
    - **Important: if the TV show was not originally created by the network, please make sure to remove the network again from the TV show to not pollute the TMDB database!**
5. If it is listed:
  - Click on its logo to view the network page.
  - Click 'Overview' -> 'Edit'
  - Click on 'Logos' -> Under 'Upload a logo' hit 'Select' and select a proper high-quality PNG or SVG to upload to TMDB.
  - When everything went OK you will see the logo appear underneath.


***Add or update logo of Samsung smart TV app***
---------------

The logos are currently manually maintained in [this](https://github.com/jaruba/channel-logos) repository.

This page will be updated with how the repository can be updated.

