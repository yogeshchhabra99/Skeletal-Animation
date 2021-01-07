Created BY Yogesh Chhabra 2017csb1120

The animations are saved in .csv format 
Run:
To run an animation, python python Player.py and select a csv file for animation. Select the runJump.csv file for full demo.

To create an animation, run Animator.py, read description below for more info. 

Description:
The aim is to create skeletal animation. I have created 2d animation for simplicity. You can create and save animations using Animator.py and then play them using Player.py. You dont have o create a lot of frames, the player interpolates between the frames with a factor defined at top, to make the animation smooth.

The animator allows you to create and save keyframes. Select a bone using you keyboard(e.g. press 'a' key to select the bone 'a', pressing 'm' will allow you to translate the skeleton), see the image file for bone names. Then use Left/Right arrow keys to rotate the selected bone. Left click mouse to save the keyframe. The keyframe is automatically added to output.csv file. You should rename it later to describe your animation.

If you select 'm' using keyboard, you can move i.e. translate the character. Up and down arrow keys move the origin of character to up and down, while the left/right ones left and right.

Player.py : Upon opening it shows you available .csv files that have animations. Select one of them and press enter to play the animation. It reads keyframes from csv, and interpolates between the frames with the interpolation factor set at the top.

The are sample animations waveHandAnim.csv and runjump.csv. You can select that to see.

How it works:
I have created a bone structure, which is nothing but a rotation wrt the parent bone, the vertices affected by the bone take that rotation. Since the vertices in this example are just spheres at the end of the bone, we dont need to specify weight of bones for each vertex. Each bone when rotated will affect the rotation of all its child but not its parents. Try playing with animator.py to understand better. These rotations(of all bones, and the origin of skeleton) are then saved in a csv file. One set of these rotation defines one frame. Frames are rendered interpolated one after another to create a smooth animation. 

KeyWords:
OpenGl, Animation, Python, graphics

Music/Images Credits:
https://www.fesliyanstudios.com/royalty-free-music/downloads-c/western-music/29
<a href='https://www.freepik.com/vectors/background'>Background vector created by upklyak - www.freepik.com</a>