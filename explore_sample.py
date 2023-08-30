import matplotlib.pyplot as plt
import json
import numpy as np
from absl import app, flags, logging

FLAGS = flags.FLAGS
flags.DEFINE_string("sample", None, "Path to sample. Provide only the ID (omit _1.json)")
flags.mark_flag_as_required("sample")

def load_file(path):
    data = None
    with open(path, "r") as fh:
        data = json.load(fh)
    return data

def plot_summary(data):
    logging.info(f"Creating summary for {data['name']} on phase {data['phase']}")
    f, ax = plt.subplots(1, 2, figsize=(12, 3.5))
    f.suptitle(f"{data['name']} phase {data['phase']}: \"{data['voice']}\"")

    # Show the image
    image = np.flip(np.asarray(data['image']), axis=2)
    ax[0].imshow(image)
    ax[0].axis('off')

    # Load the trajectories 
    # Note: the gripper state is at index 30, so let's grab that too
    trajectory = np.asarray([np.take(state, [0,1,2,3,4,5,30]) for state in data["state/raw"]])
    labels = ["Joint-1", "Joint-2", "Joint-3", "Joint-4", "Joint-5", "Joint-6", "Gripper"]
    # Plot each trajectory separately
    for i in range(trajectory.shape[1]):
        # Plot trajectories in length 0-100%
        x = np.arange(trajectory.shape[0]) / trajectory.shape[0] * 100
        ax[1].plot(x, trajectory[:,i], label=labels[i])
    # Prettify
    ax[1].set_xlabel("Percentage of Trajectory Completed")
    ax[1].set_ylabel("Absolute Joint Angle (radians)")
    ax[1].legend(loc="center right", ncols=1, fancybox=True, bbox_to_anchor=(1.25,0.5))
    plt.subplots_adjust(left=0.01, bottom=0.15)

def main(argv):
    del argv

    logging.info(f"Plotting sample from file: {FLAGS.sample}")

    plot_summary(load_file(FLAGS.sample + "_1.json"))
    plot_summary(load_file(FLAGS.sample + "_2.json"))

    plt.show()

if __name__ == "__main__":
    app.run(main)
