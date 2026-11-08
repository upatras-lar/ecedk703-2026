import os
import json
import glob
import shutil
from camera_utils import calibrate_camera, capture_calibration_images


# -----------------------------------------------------------
#  SAVE CALIBRATION DATA INTO camera_params.json
# -----------------------------------------------------------
def save_to_json(camera_number, intrinsic, distortion, json_file = "camera_params.json"):

    data = {}

    # Load existing JSON if present
    if os.path.exists(json_file):
        with open(json_file, "r") as f:
            try:
                data = json.load(f)
            except:
                data = {}   # empty or corrupt

    # Overwrite or create this camera number
    data["camera_parameters"][str(camera_number)] = {
        "camera_matrix": intrinsic.tolist(),
        "dist_coeffs": distortion.tolist()
    }

    # Save back to file
    with open(json_file, "w") as f:
        json.dump(data, f, indent=4)

    print(f"Saved calibration for camera [{camera_number}] into {json_file}.")


# -----------------------------------------------------------
#  DELETE PREVIOUS CALIBRATION IMAGES
# -----------------------------------------------------------
def delete_calibration_images(folder):
    if not os.path.exists(folder):
        return

    imgs = glob.glob(os.path.join(folder, "*"))
    if len(imgs) == 0:
        print("No calibration images to delete.")
        return

    answer = input(f"Delete ALL images in '{folder}'? (y/n): ").lower().strip()
    if answer == "y":
        shutil.rmtree(folder)
        os.makedirs(folder)
        print("All calibration images deleted.\n")
    else:
        print("Images kept.\n")


# -----------------------------------------------------------
#  MAIN PROGRAM
# -----------------------------------------------------------
def main():

    calibration_folder = "calibration_images"
    calibration_pattern = os.path.join(calibration_folder, "*.png")

    print("\n========== CAMERA CALIBRATION ==========\n")

    # -------------------------------------------------------
    # DELETE IMAGES (OPTIONAL)
    # -------------------------------------------------------
    delete_answer = input("Delete previous calibration images? (y/n): ").lower().strip()
    if delete_answer == "y":
        delete_calibration_images(calibration_folder)
    else:
        print("Keeping existing calibration images.\n")

    # -------------------------------------------------------
    # ASK FOR CAMERA NUMBER TO STORE IN JSON
    # -------------------------------------------------------
    while True:
        cam_number = input("Enter camera number to save calibration under: ").strip()
        if cam_number.isdigit():
            cam_number = int(cam_number)
            break
        print("Invalid input. Must be an integer.")

    # -------------------------------------------------------
    # CAPTURE NEW IMAGES (OPTIONAL)
    # -------------------------------------------------------
    capture_answer = input("Capture new calibration images now? (y/n): ").lower().strip()
    if capture_answer == "y":
        capture_calibration_images(calibration_folder)

    # -------------------------------------------------------
    # RUN CALIBRATION
    # -------------------------------------------------------
    print("\nRunning calibration...\n")

    intrinsic, dist_coeffs, error = calibrate_camera(calibration_pattern)

    if intrinsic is None:
        print("Calibration failed. No valid detections.")
        return

    print("\n--- CALIBRATION RESULTS ---")
    print("Intrinsic Matrix:\n", intrinsic)
    print("Distortion Coefficients:\n", dist_coeffs)
    print(f"Reprojection Error: {error:.5f}")

    # -------------------------------------------------------
    # SAVE RESULTS TO JSON
    # -------------------------------------------------------
    save_to_json(
        camera_number = cam_number,
        intrinsic = intrinsic,
        distortion = dist_coeffs
    )


if __name__ == "__main__":
    main()
