# Completed Brick Breaker Tasks

This version implements all four tasks from the original README:

1. Accurate brick collision:
   - Detects whether the ball hit the left/right or top/bottom side.
   - Reverses the correct velocity component.
   - Prevents the ball from clipping through bricks.

2. Game-over / win screen:
   - Shows WIN when every brick is destroyed.
   - Shows GAME OVER when all lives are lost.
   - Displays final score and waits for input.

3. Replay + difficulty:
   - After the end screen, press R/Enter/Space to return to difficulty selection.
   - Easy, Medium, and Hard change ball speed and paddle size/speed.

4. Sound feedback:
   - Procedural sounds are generated in code, so no audio files are required.
   - Sounds play for brick hits, paddle hits, wall hits, and win/game-over.
