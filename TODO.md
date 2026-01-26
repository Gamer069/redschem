## COMMON

- [x] update this todo list as i implement features
- [x] setup git
- [x] more comments 
- [x] docs (maybe later)
- [ ] nicer code
- [ ] get a response from the one, AND ONLY, @mattbatwings on lrs discord

## BACKEND

- [x] simple foundation
- [x] make it more error resistant
- [x] header parsing
- [x] database management
- [x] multiple files
- [x] get rid of asyncio
- [x] admin commands (resync)
- [x] manual refresh command
- [x] add lock to prevent multiple syncs running at the same time
- [x] listen for message events such as messageCreate so you don't have to restart the whole bot to add a schem
- [x] better table structure
- [x] drop db/dont duplicate items
- [x] good logging (see https://github.com/Delgan/loguru)
- [ ] error handling for invalid headers
- [ ] rate limiting


## FRONTEND
- [x] make a frontend
- [x] somehow deal with the extra data in \<Schematic\/> properly - if it's too long then the tile will be like 50km long and we dont want that - maybe make it scrollable and open up like a \<code\> style thing so it doesn't take up much space?
- [x] add different themes in frontend so its not always just catppuccin mocha (DONE just need to figure out live theme switching)
- [x] good 404 page
- [x] more spacing between rows in the schematic component
- [x] fix styling so it looks usable
- [ ] fix frontend styling so it looks VERY good

### MAYBE
- [ ] admin dashboard..?

### SEARCH

- [x] add search
- [x] make search keybind
- [ ] make search faster (when input's length === 1 and that one character changes/gets deleted to not cause chaos and re-render THE ENTIRE THING)
- [ ] add search filters

## BOT TESTING GROUND TODOS
- [x] move 16 segment display to separate category and subcategory in bot testing ground (just for testing)
- [x] add literally all schematics just to see if it will work in prod in bot testing ground
- [ ] load testing with concurrent users
- [ ] test database migration workflow
