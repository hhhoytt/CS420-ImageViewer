# Image Classifier

Made by Harrison Hoytt for COSC 420's Lab 1.

Features:
- Displays all images from your experiments folder one at a time
- Lets you save your results over your `MasterExperiment.csv` file
- Skips over already entered information so you don't have to worry about overwritting it

## How to Run

**You will need to modify `ca_simulator.py` in order for this app to work correctly!**

When the name of the image file gets created, the step number needs to be padded out to 2 numbers. 
Replace line 99 with this: `img_fn = self.exp_dir + "/experiment_" + str(experiment) + "_step_" + str(z).zfill(2) + ".png"`

This change is so it reads through the images in order. It may work if you don't do that, but I'm not sure.

Once you make that change, you can run the program with `python image-classifier.py`. This python script must be in the same directory as the `experiments` directory and the `MasterExperiment.csv` file.