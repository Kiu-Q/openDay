# Info Day Shooting Game - Thunder Challenge Edition

## Purpose
The "Thunder Challenge Edition" of the Open Day Shooting Game is a Python-based interactive experience developed for the Ho Fung College Info Day. In this edition, the gameplay is elevated with a competitive Player vs. Computer challenge and new mechanics that advance both fun and technical sophistication.

## Improvements
Thunder Challenge introduces major improvements over the previous version:
- **Entirely New Game Mode (Thunder Challenge):** 30-second survival against a Computer AI, requiring players to beat the CPU's score.
- **Advanced Computer Opponent:** CPU character driven by a dynamic cleverness algorithm, featuring pathfinding and avoidance logic.
- **Power-Up System:** Thunder collectible appears mid-game; capturing it weakens the CPU's AI temporarily and lets the player clear monsters for bonus points.
- **Targets from Every Direction:** Enemies spawn at random edges and travel towards the screen center, making reflexes and strategy crucial.
- **Evolving Spawn Frequency:** As time passes, enemies appear faster to increase challenge.
- **Expanded Object Classes:** Computer AI and Thunder objects added alongside existing shooter, monsters, and students.
- **Visual and Sound Updates:** Enhanced color palette, new sound effects for core actions (including thunder power-up).

## Progress
The game now features:
- **Thunder Challenge Mode:** Compete against a CPU in a timed session with top scores recorded per run.
- **Multi-Directional Targets:** Monsters and students appear from all edges, not just left/right or bottom/top.
- **Real-Time Hand Tracking:** Both player and Computer AI move and target dynamically as monsters and students approach.
- **Intelligent AI:** CPU adapts its movement, avoids students and the player, and chases monsters to simulate competitive play.
- **Thunder Power-Up:** Temporary advantage—weakens CPU cleverness, clears monsters, and rewards bonus points for the player.
- **Leaderboard:** Records top scores for players, resettable for a fresh competition environment.

## Techniques Used
- **Pygame:** Handles the game loop, window management, graphics rendering, and input events.
- **Mediapipe:** Powers hand tracking, letting players control the shooter intuitively via webcam gestures.
- **OpenCV:** Captures video frames for Mediapipe's hand recognition.
- **Python Shelve:** Manages persistent leaderboard data for Thunder Challenge mode.
- **Dynamic AI:** Computer opponent uses quadratic cleverness curve and context-sensitive pathfinding, avoiding hazards and adapting over 30 seconds.

## How to Play
1. Launch the Thunder Challenge game script.
2. Press the SPACEBAR to start.
3. Move your hand in front of your webcam to control the shooter's position. The CPU will compete against you automatically.
4. Avoid shooting students and aim for monsters. Collect the Thunder power-up when available to weaken the CPU and clear monsters for extra score.
5. Survive for 30 seconds—your goal is to beat the Computer's score. Win by scoring higher or if the CPU hits a student.
6. If you achieve a top score, enter your name for leaderboard ranking!

## Installation
Follow these steps to set up and run Thunder Challenge:
1. Clone the repository.
2. Open a command prompt in the repository folder.
3. Run `pip install -r requirements.txt` to install dependencies.
4. If required, install the Microsoft Visual C++ Redistributable from https://aka.ms/vs/17/release/vc_redist.x64.exe.
5. Run `python openDayThunderChallenge.py` to launch the Thunder Challenge mode.

## Details: How the Code Works
Thunder Challenge is an extension of the previous Open Day game. It introduces advanced game logic and AI mechanics:
### Main Components
- **Game Initialization:** Loads assets (images, sounds), initializes constants and sets up Pygame and Mediapipe for the session.
- **Thunder Challenge Mode:** Starts the 30-second survival run, displaying a leaderboard and rendering game instructions.
- **Dynamic Target Spawning:** Monsters and students spawn from all window edges, utilizing randomized entry points and velocities to keep gameplay unpredictable.
- **CPU Opponent (Computer Class):** Strategically moves toward monsters while avoiding students and the player. The AI algorithm:
    - Computes cleverness with a quadratic curve, so the CPU becomes smarter as the round progresses.
    - Avoids hazards using repulsion and dynamic error margin, reacting to proximity with students or the player.
    - Pathfinding directs CPU to the nearest monster, seeking optimal scoring opportunities.
    - Thunder power-up drastically reduces CPU cleverness, lowering its scoring ability and making player comeback possible.
- **Thunder Power-Up:** Thunder is a special collectible. When the player hits it:
    - CPU cleverness multiplier is permanently reduced.
    - All monsters on-screen are cleared for extra player points.
    - Thunder sound effect plays, indicating the power-up's activation.
- **Collision Detection:** Both player and CPU check for collisions with on-screen objects each frame.
    - Monsters: Both score points.
    - Students: Player loses or CPU misstep—player wins immediately.
    - Thunder: Only the player can collect; CPU ignores it.
- **Leaderboard Management:** When a top score is achieved, player enters their name and scores are updated via Python shelve.

Thunder Challenge is built on robust object-oriented game design, with each entity (player, CPU, monsters, students, thunder) inheriting shared logic for rendering and position updates. Compared to the previous version, the code integrates AI, power-ups, and multiple simultaneous object spawning, significantly increasing gameplay depth and replay value while preserving accessibility for casual play and school events.

---

## Acknowledgements
Developed by Li Tsz Kiu (Kiu-Q) for Ho Fung College Open Day. Images and sounds courtesy of hofung.edu.hk, Freepik, いらすとや, and Pixabay.

## License
MIT License. See `LICENSE.md` for terms.