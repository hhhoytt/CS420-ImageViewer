# Image Classifier

Made by Harrison Hoytt for UTK COSC 420's Lab 1 Cellular Automata.

Features:
- Displays all images from your experiments folder one at a time
- Lets you save your results over your `MasterExperiment.csv` file
- Skips over already entered information so you don't have to worry about overwritting it

## Initial Setup

Firstly, if you want to see the images in order, **You will need to modify `ca_simulator.py` in order for this app to work as intended!**

In `ca_simulator.py`, replace line 99 with this: `img_fn = self.exp_dir + "/experiment_" + str(experiment) + "_step_" + str(z).zfill(2) + ".png"`

With this change, when the .png gets created, the step number will be padded out to 2 numbers. 

This change is so it reads through the images in the order of their steps. The app should still run perfectly if you don't make this change, but you wont get the images shown to you in order! If you already started on your spreadsheet and just want to continue without running the simulator script again, you can, you just wont see the steps in order. I have not actuall tested this myself but it should still work with the steps out of order.

**NOTE:** This change will only put the steps in order. Currently the experiments will be out of order, but that doesn't matter as much. This means that after editing experiment 0 it will jump you to experiment 10. If you save halfway and don't see any changes saved for experiment 1-9, just scroll down and you will see you data saved for the other experiments!

## How to Run

You can run the program with `python image-classifier.py`. This python script must be in the same directory as the `experiments` directory and the `MasterExperiment.csv` file.

## Known Issues

- The app seems to run slow when it first starts up, with the buttons being unresponsive. I'm not sure why this happens but it usually passes after 30 seconds
- The way I'm checking for records that have already been entered is really slow when there's a lot of records. I need to speed this up
- The input boxes allow for tabs and newlines to be entered. They really shouldn't. Also the class input box should only allow 1 character