# Royal Chess

## Overview

Welcome to the Royal Chess project! This brand-new multiplayer chess game is developed in Python, and structured in three different levels: engine, network, and UI. The engine has been developed following the best standards in the field, using advanced techniques such as bitboards; to ensure optimal performance. Royal Chess is **AI free**, for example, to evaluate moves utilizing the negamax algorithm, AI will never be used in there! You can play in multiplayer via LAN, hence you can challenge only people in your network!

This project was developed by a team of two people:

- **https://github.com/ItsAlessandro**, Responsible for the development of the engine and the networking part
- **https://github.com/AlessandroMarchionni**, Responsible for the development of the integration with Pygame

## Features

- **Advanced engine**: Utilizing bitboards to represent the board, high performances are guaranteed
- **Multiplayer in LAN**: Being in the same network as your opponent is enough to play with him in Royal Chess.
- **GUI**: Intuitive user interface, developed in Pygame
- **Absence of AI**: Nowadays the easiest way to develop a chess engine is with AI, in this project is preferred to utilize the most robust existing method.

## Getting started

After installing pygame, you should host the server using one machine in the **same sub-network** as the other hosts, once initialized the server.py file in the console will be available the server IP utilizable to connect the clients to the server, once all is connected the clients can create sessions and start games, enjoy!

## Future updates 

1. Destructure the engine.py in classes, to improve readability (29 May / in progress)
2. Implement all the networking routes as the communication.txt says (29 May / in progress)
3. Enhance usability in the program (29 May / in progress)

*Alessandro Duranti, 29/05/2024*