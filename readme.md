This is a readme for the Nyaaim-9 project. Currently this project is stagnant until I figure out what I want to do with it. 

The project came about because me and my friends enjoy DCS, however to host a server you need to use Windows Server and a pretty beefy one at that. These are expensive ($100/mo +) and I wanted to find a way to lower that cost.

This project is designed so that you can control and spin up a DCS server from a discord bot that you host yourself. It has an API that talks to the server. The server has a network monitor running, and will send a signal to the API to shutdown when traffic falls below a certain point. (This is buggy. The netmonitor dies sometimes, so always check on your servers or else you're going to rack up costs.). It uses the Vultr API for its calls. It expects you to have done 1 initial setup of the instance manually, so that the bot has a set of defaults to use to create your server. DCS Servers are large, so the files themselves are stored on a block storage device. This gets attached to the server after start up. In my experience for servers with less than 8 players, there was no performance hit.




    
