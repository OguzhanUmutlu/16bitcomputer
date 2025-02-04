# 16bitcomputer
Just a little fun project in Logisim Evolution. A simple 16-bit computer.

## How to run a program?

- Install python for the compiler.
- Compile your assembly code using the instructions in the Excel file and then run `python compile.py`.
- Open up Logisim Evolution on cpu.circ, press the ROM on the left which should look like a big box of numbers going down.
- In the left menu press `(click to edit)`.
- If the popup window is too big resize it to be smaller.
- Press `Open...` at the bottom of the popup window.
- Select the `program_rom` file that was compiled before and then press `Open`.
- After that, close the popup window.
- Now on the left of the ROM you were on, you should see a button and an upper-cased `RESET` button.
- Click the `RESET` button.
- Now on the left top corner of the screen, you will see two sections: `Design`, `Simulate`
- Press `Simulate`.
- In the Simulate menu, there will be 5 buttons on top of the menu indicating: Stop simulator, Step simulator once, Enable clock ticks, Tick clock one half cycle, Tick clock one full cycle
- Press the third button being the `Enable clock ticks`
- You can change the speed of the program on top of the Logisim Evolution screen, by going in: `Simulate > Auto-Tick Frequency` and then selecting the speed. The bigger the frequency the faster it will be.
- And viola! You should now see the answer in the RAM in the right side of the whole circuit, which should look similar to the ROM.
