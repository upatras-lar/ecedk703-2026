import numpy as np
import cv2
import os, glob


# some typical ArUco markers dictionaries
ArUco_dictionaries = {
	"4X4_50/20mm": cv2.aruco.DICT_4X4_50, "4X4_50/30mm": cv2.aruco.DICT_4X4_50, "4X4_50/40mm": cv2.aruco.DICT_4X4_50, "4X4_50/50mm": cv2.aruco.DICT_4X4_50, "4X4_50/100mm": cv2.aruco.DICT_4X4_50,
    "4X4_50/150mm": cv2.aruco.DICT_4X4_50, "4X4_50/200mm": cv2.aruco.DICT_4X4_50, "4X4_50/250mm": cv2.aruco.DICT_4X4_50, "4X4_50/300mm": cv2.aruco.DICT_4X4_50,
	"4X4_100/20mm": cv2.aruco.DICT_4X4_100, "4X4_100/30mm": cv2.aruco.DICT_4X4_100, "4X4_100/40mm": cv2.aruco.DICT_4X4_100, "4X4_100/50mm": cv2.aruco.DICT_4X4_100, "4X4_100/100mm": cv2.aruco.DICT_4X4_100,
    "4X4_100/150mm": cv2.aruco.DICT_4X4_100, "4X4_100/200mm": cv2.aruco.DICT_4X4_100, "4X4_100/250mm": cv2.aruco.DICT_4X4_100, "4X4_100/300mm": cv2.aruco.DICT_4X4_100,
    "4X4_250/20mm": cv2.aruco.DICT_4X4_250, "4X4_250/30mm": cv2.aruco.DICT_4X4_250, "4X4_250/40mm": cv2.aruco.DICT_4X4_250, "4X4_250/50mm": cv2.aruco.DICT_4X4_250, "4X4_250/100mm": cv2.aruco.DICT_4X4_250,
    "4X4_250/150mm": cv2.aruco.DICT_4X4_250, "4X4_250/200mm": cv2.aruco.DICT_4X4_250, "4X4_250/250mm": cv2.aruco.DICT_4X4_250, "4X4_250/300mm": cv2.aruco.DICT_4X4_250,
    "4X4_1000/20mm": cv2.aruco.DICT_4X4_1000, "4X4_1000/30mm": cv2.aruco.DICT_4X4_1000, "4X4_1000/40mm": cv2.aruco.DICT_4X4_1000, "4X4_1000/50mm": cv2.aruco.DICT_4X4_1000, "4X4_1000/100mm": cv2.aruco.DICT_4X4_1000,
    "4X4_1000/150mm": cv2.aruco.DICT_4X4_1000, "4X4_1000/200mm": cv2.aruco.DICT_4X4_1000, "4X4_1000/250mm": cv2.aruco.DICT_4X4_1000, "4X4_1000/300mm": cv2.aruco.DICT_4X4_1000,
	"5X5_50/20mm": cv2.aruco.DICT_5X5_50, "5X5_50/30mm": cv2.aruco.DICT_5X5_50, "5X5_50/40mm": cv2.aruco.DICT_5X5_50, "5X5_50/50mm": cv2.aruco.DICT_5X5_50, "5X5_50/100mm": cv2.aruco.DICT_5X5_50,
    "5X5_50/150mm": cv2.aruco.DICT_5X5_50, "5X5_50/200mm": cv2.aruco.DICT_5X5_50, "5X5_50/250mm": cv2.aruco.DICT_5X5_50, "5X5_50/300mm": cv2.aruco.DICT_5X5_50,
    "5X5_100/20mm": cv2.aruco.DICT_5X5_100, "5X5_100/30mm": cv2.aruco.DICT_5X5_100, "5X5_100/40mm": cv2.aruco.DICT_5X5_100, "5X5_100/50mm": cv2.aruco.DICT_5X5_100, "5X5_100/100mm": cv2.aruco.DICT_5X5_100,
    "5X5_100/150mm": cv2.aruco.DICT_5X5_100, "5X5_100/200mm": cv2.aruco.DICT_5X5_100, "5X5_100/250mm": cv2.aruco.DICT_5X5_100, "5X5_100/300mm": cv2.aruco.DICT_5X5_100,
    "5X5_250/20mm": cv2.aruco.DICT_5X5_250, "5X5_250/30mm": cv2.aruco.DICT_5X5_250, "5X5_250/40mm": cv2.aruco.DICT_5X5_250, "5X5_250/50mm": cv2.aruco.DICT_5X5_250, "5X5_250/100mm": cv2.aruco.DICT_5X5_250,
    "5X5_250/150mm": cv2.aruco.DICT_5X5_250, "5X5_250/200mm": cv2.aruco.DICT_5X5_250, "5X5_250/250mm": cv2.aruco.DICT_5X5_250, "5X5_250/300mm": cv2.aruco.DICT_5X5_250,
    "5X5_1000/20mm": cv2.aruco.DICT_5X5_1000, "5X5_1000/30mm": cv2.aruco.DICT_5X5_1000, "5X5_1000/40mm": cv2.aruco.DICT_5X5_1000, "5X5_1000/50mm": cv2.aruco.DICT_5X5_1000, "5X5_1000/100mm": cv2.aruco.DICT_5X5_1000,
    "5X5_1000/150mm": cv2.aruco.DICT_5X5_1000, "5X5_1000/200mm": cv2.aruco.DICT_5X5_1000, "5X5_1000/250mm": cv2.aruco.DICT_5X5_1000, "5X5_1000/300mm": cv2.aruco.DICT_5X5_1000,
    "6X6_50/20mm": cv2.aruco.DICT_6X6_50, "6X6_50/30mm": cv2.aruco.DICT_6X6_50, "6X6_50/40mm": cv2.aruco.DICT_6X6_50, "6X6_50/50mm": cv2.aruco.DICT_6X6_50, "6X6_50/100mm": cv2.aruco.DICT_6X6_50,
    "6X6_50/150mm": cv2.aruco.DICT_6X6_50, "6X6_50/200mm": cv2.aruco.DICT_6X6_50, "6X6_50/250mm": cv2.aruco.DICT_6X6_50, "6X6_50/300mm": cv2.aruco.DICT_6X6_50,
    "6X6_100/20mm": cv2.aruco.DICT_6X6_100, "6X6_100/30mm": cv2.aruco.DICT_6X6_100, "6X6_100/40mm": cv2.aruco.DICT_6X6_100, "6X6_100/50mm": cv2.aruco.DICT_6X6_100, "6X6_100/100mm": cv2.aruco.DICT_6X6_100,
    "6X6_100/150mm": cv2.aruco.DICT_6X6_100, "6X6_100/200mm": cv2.aruco.DICT_6X6_100, "6X6_100/250mm": cv2.aruco.DICT_6X6_100, "6X6_100/300mm": cv2.aruco.DICT_6X6_100,
    "6X6_250/20mm": cv2.aruco.DICT_6X6_250, "6X6_250/30mm": cv2.aruco.DICT_6X6_250, "6X6_250/40mm": cv2.aruco.DICT_6X6_250, "6X6_250/50mm": cv2.aruco.DICT_6X6_250, "6X6_250/100mm": cv2.aruco.DICT_6X6_250,
    "6X6_250/150mm": cv2.aruco.DICT_6X6_250, "6X6_250/200mm": cv2.aruco.DICT_6X6_250, "6X6_250/250mm": cv2.aruco.DICT_6X6_250, "6X6_250/300mm": cv2.aruco.DICT_6X6_250,
    "6X6_1000/20mm": cv2.aruco.DICT_6X6_1000, "6X6_1000/30mm": cv2.aruco.DICT_6X6_1000, "6X6_1000/40mm": cv2.aruco.DICT_6X6_1000, "6X6_1000/50mm": cv2.aruco.DICT_6X6_1000, "6X6_1000/100mm": cv2.aruco.DICT_6X6_1000,
    "6X6_1000/150mm": cv2.aruco.DICT_6X6_1000, "6X6_1000/200mm": cv2.aruco.DICT_6X6_1000, "6X6_1000/250mm": cv2.aruco.DICT_6X6_1000, "6X6_1000/300mm": cv2.aruco.DICT_6X6_1000,
    "7X7_50/20mm": cv2.aruco.DICT_7X7_50, "7X7_50/30mm": cv2.aruco.DICT_7X7_50, "7X7_50/40mm": cv2.aruco.DICT_7X7_50, "7X7_50/50mm": cv2.aruco.DICT_7X7_50, "7X7_50/100mm": cv2.aruco.DICT_7X7_50,
    "7X7_50/150mm": cv2.aruco.DICT_7X7_50, "7X7_50/200mm": cv2.aruco.DICT_7X7_50, "7X7_50/250mm": cv2.aruco.DICT_7X7_50, "7X7_50/300mm": cv2.aruco.DICT_7X7_50,
    "7X7_100/20mm": cv2.aruco.DICT_7X7_100, "7X7_100/30mm": cv2.aruco.DICT_7X7_100, "7X7_100/40mm": cv2.aruco.DICT_7X7_100, "7X7_100/50mm": cv2.aruco.DICT_7X7_100, "7X7_100/100mm": cv2.aruco.DICT_7X7_100,
    "7X7_100/150mm": cv2.aruco.DICT_7X7_100, "7X7_100/200mm": cv2.aruco.DICT_7X7_100, "7X7_100/250mm": cv2.aruco.DICT_7X7_100, "7X7_100/300mm": cv2.aruco.DICT_7X7_100,
    "7X7_250/20mm": cv2.aruco.DICT_7X7_250, "7X7_250/30mm": cv2.aruco.DICT_7X7_250, "7X7_250/40mm": cv2.aruco.DICT_7X7_250, "7X7_250/50mm": cv2.aruco.DICT_7X7_250, "7X7_250/100mm": cv2.aruco.DICT_7X7_250,
    "7X7_250/150mm": cv2.aruco.DICT_7X7_250, "7X7_250/200mm": cv2.aruco.DICT_7X7_250, "7X7_250/250mm": cv2.aruco.DICT_7X7_250, "7X7_250/300mm": cv2.aruco.DICT_7X7_250,
    "7X7_1000/20mm": cv2.aruco.DICT_7X7_1000, "7X7_1000/30mm": cv2.aruco.DICT_7X7_1000, "7X7_1000/40mm": cv2.aruco.DICT_7X7_1000, "7X7_1000/50mm": cv2.aruco.DICT_7X7_1000, "7X7_1000/100mm": cv2.aruco.DICT_7X7_1000,
    "7X7_1000/150mm": cv2.aruco.DICT_7X7_1000, "7X7_1000/200mm": cv2.aruco.DICT_7X7_1000, "7X7_1000/250mm": cv2.aruco.DICT_7X7_1000, "7X7_1000/300mm": cv2.aruco.DICT_7X7_1000,
    "ORIGINAL/20mm": cv2.aruco.DICT_ARUCO_ORIGINAL,	"ORIGINAL/30mm": cv2.aruco.DICT_ARUCO_ORIGINAL,	"ORIGINAL/40mm": cv2.aruco.DICT_ARUCO_ORIGINAL,	"ORIGINAL/50mm": cv2.aruco.DICT_ARUCO_ORIGINAL,	"ORIGINAL/100mm": cv2.aruco.DICT_ARUCO_ORIGINAL,
	"ORIGINAL/150mm": cv2.aruco.DICT_ARUCO_ORIGINAL, "ORIGINAL/200mm": cv2.aruco.DICT_ARUCO_ORIGINAL, "ORIGINAL/250mm": cv2.aruco.DICT_ARUCO_ORIGINAL, "ORIGINAL/300mm": cv2.aruco.DICT_ARUCO_ORIGINAL,
}

# create the image window
def create_image_window(window_name, width, height):
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)  # create the window with the given name
    cv2.resizeWindow(window_name, int(width), int(height))  # resize the window to the given width and height

# show the images with the given window names and size factor
def show_images_on_screen(images, windows_names = [], size_factor = 2/3, show_images_flag = True, hold_images_flag = False, hold_images_time = 0):
    images = [np.array(image) for image in images]  # make sure the images are numpy arrays
    if len(windows_names) != len(images):  # if the number of window names is not equal to the number of images
        windows_names += [f"Image {k}" for k in range(abs(len(images) - len(windows_names)))]  # create window names for the images
    if show_images_flag:  # show the camera's original image
        for k in range(len(images)):  # for each image
            create_image_window(windows_names[k], size_factor * images[k].shape[1], size_factor * images[k].shape[0])
            cv2.imshow(windows_names[k], images[k])  # show the camera's original image
        if hold_images_flag: cv2.waitKey(int(hold_images_time))  # wait for some time
        else: pass  # continue

# calibrate the camera
def calibrate_camera(calibration_images_path):
    max_iterations = 100; epsilon_error = 1e-5  # the maximum number of iterations allowed and the desired accuracy
    termination_criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, max_iterations, epsilon_error)  # the termination criteria
    # sample some world space 3d points, based on the specific chessboard pattern used
    grid_rows = 9  # the grid rows, the number of inner corners in the chessboard pattern along the y-axis
    grid_columns = 6  # the grid columns, the number of inner corners in the chessboard pattern along the x-axis
    world_points_grid = np.zeros((grid_rows * grid_columns, 3), np.float32)  # initialize the world space 3d points grid
    world_points_grid[:, :2] = np.mgrid[0 : grid_rows, 0 : grid_columns].T.reshape(-1, 2)  # the world space 3d points grid (I assume the chessboard is on the xy plane, with z = 0)
    world_points_grid[:, 2] = 0  # set the z coordinate of the world space 3d points grid to 0
    world_points = []  # initialize the world space 3d points
    image_points = []  # initialize the image plane 2d points
    # calibrate the camera looping through all the images with the chessboard pattern
    images = glob.glob(calibration_images_path)  # load the images that contain the chessboard pattern in different poses for the calibration
    if len(images) != 0:  # if there are images to calibrate the camera
        print(f"Number of images for camera calibration: {len(images)}")  # print the number of images used for the camera calibration
        for img in images:  # loop through the images to calibrate the camera
            original_image_drawn_chessboard = cv2.imread(img)  # load the image
            gray_image = cv2.cvtColor(original_image_drawn_chessboard, cv2.COLOR_BGR2GRAY)  # convert the image to grayscale
            corners_found, corners = cv2.findChessboardCorners(gray_image, (grid_rows, grid_columns), None)  # find the chessboard corners
            if corners_found == True:  # if the corners are found
                world_points.append(world_points_grid)  # add the world space 3d points grid
                corners_refined = cv2.cornerSubPix(gray_image, corners, (11, 11), (-1, -1), termination_criteria)  # find more precise corner positions
                cv2.drawChessboardCorners(original_image_drawn_chessboard, (grid_rows, grid_columns), corners_refined, corners_found)  # draw the corners on the chessboard
                image_points.append(corners_refined)
                show_images_on_screen([original_image_drawn_chessboard], ["Original images with the drawn corners on the chessboard pattern"], 1, True, True, 1000)  # show the calibration images with the corners on the chessboard
        if len(image_points) != 0:  # if there are image points to calibrate the camera
            print(f"Number of images with chessboard corners found: {len(image_points)}")  # print the number of images with chessboard corners found
            # calibrate the camera and get the distortion coefficients and the intrinsic parameters of the intrinsic matrix
            reprojection_error, intrinsic_mat, dist_coeffs, _, _ = cv2.calibrateCamera(world_points, image_points, gray_image.T.shape[:2], None, None)  # calibrate the camera
            print(f"Reprojection error (in pixels): {reprojection_error:.5f}")
            print(f"Camera intrinsic matrix (in pixels): {np.round(intrinsic_mat, 3)}")
            print(f"Camera distortion coefficients (dimensionless): {dist_coeffs.flatten()}")
            return intrinsic_mat, dist_coeffs.flatten(), reprojection_error  # return the intrinsic matrix, the distortion coefficients and the reprojection error (in pixels)
        else:  # if there are no corners found in the images
            print("No corners found in the images!")  # print that there are no corners found in the images
            return None, None, None  # return None for the intrinsic matrix, the distortion coefficients and the reprojection error
    else:  # if there are no images to calibrate the camera
        print("No images found for camera calibration!")  # print that there are no images to calibrate the camera
        return None, None, None  # return None for the intrinsic matrix, the distortion coefficients and the reprojection error

def capture_calibration_images(folder_name):
    # create calibration_images folder if it does not exist
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # camera configuration (Ubuntu / OpenCV)
    camera_resolution = 480
    camera_aspect_ratio = 4/3
    cap = cv2.VideoCapture(0)   # external camera (0 if needed)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, camera_resolution)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, int(camera_aspect_ratio * camera_resolution))

    # check if there is an open external camera
    if not cap.isOpened():
        print("Error: Could not open external camera.")
        return

    while True:
        ret, frame = cap.read()  # read camera frame

        # check if there is a working camera feed
        if not ret:
            print("Error: Could not read frame from camera.")
            break

        # overlay text on camera frame
        instructions = "Press ENTER to capture an image, or \"s\" to stop/close the camera ..."
        cv2.putText(frame, instructions, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        num_images = len([f for f in os.listdir(folder_name) if f.lower().endswith((".png", ".jpg", ".jpeg"))])
        count_text = f"Images captured: {num_images}"
        cv2.putText(frame, count_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        # show camera frame on the OpenCV window
        cv2.imshow("Camera Feed", frame)

        # wait for user's input
        key = cv2.waitKey(1) & 0xFF
        if key == 13:  # press enter to capture the current camera frame
            img_name = os.path.join(folder_name, f"image_{num_images + 1}.png")
            cv2.imwrite(img_name, frame)
            print(f"Captured {img_name}")
        elif key == ord("s"):  # press the "s" key to stop/close the camera
            break
        
    # OpenCV cleanup
    cap.release()
    cv2.destroyAllWindows()

# estimate the ArUco markers poses with respect to the camera
def estimate_ArUco_marker_pose(image, ArUco_marker, intrinsic_mat, dist_coeffs):
    image = np.array(image)  # make sure the image is a numpy array
    if ArUco_marker not in ArUco_dictionaries.keys():  # if the ArUco marker is not in the available ArUco markers dictionaries
        print(f"The ArUco marker {ArUco_marker} is not in the available ArUco markers dictionaries!")
        return np.eye(4), image  # return None for the ArUco marker transformation matrix and the image with the detected markers and their poses
    else:  # if the ArUco marker is in the available ArUco markers dictionaries
        ArUco_dict = cv2.aruco.Dictionary_get(ArUco_dictionaries[ArUco_marker])  # get the specific ArUco dictionary
        parameters = cv2.aruco.DetectorParameters_create()  # create the ArUco detector parameters
        corners, ids, _ = cv2.aruco.detectMarkers(image, ArUco_dict, parameters = parameters)  # detect the ArUco markers in the image
        ArUco_marker_side_length = float(ArUco_marker.split("/")[1].split("mm")[0]) / 1000.0  # get the ArUco marker side length in meters
        if ids is not None:  # if markers are detected
            for k in range(len(ids)):  # for each detected ArUco marker
                rotation_vec, translation_vec, _ = cv2.aruco.estimatePoseSingleMarkers(corners[k], ArUco_marker_side_length, intrinsic_mat, dist_coeffs)  # estimate the pose of the ArUco marker
                if k == 0:  # if it is the first ArUco marker
                    rotation_matrix, _ = cv2.Rodrigues(rotation_vec)  # convert the rotation vector to a rotation matrix
                    ArUco_transformation_matrix = np.eye(4)  # initialize the transformation matrix
                    ArUco_transformation_matrix[:3, :3] = rotation_matrix.reshape(3, 3)  # set the rotation matrix in the transformation matrix
                    ArUco_transformation_matrix[:3, 3] = translation_vec.reshape(3,)  # set the translation vector in the transformation matrix
                cv2.drawFrameAxes(image, intrinsic_mat, dist_coeffs, rotation_vec, translation_vec, [0.1, 0.05][[True, False].index(k == 0)])  # draw the axis of each ArUco marker            
            cv2.aruco.drawDetectedMarkers(image, corners, ids)  # draw the detected ArUco markers
            print(f"ArUco markers detected: {ids.flatten()}")  # print the detected ArUco markers
            return ArUco_transformation_matrix, image  # return the ArUco marker transformation matrix and the image with the detected markers and their poses
        else:  # if no markers are detected
            print("No ArUco marker detected.")
            return np.eye(4), image  # return None for the ArUco marker transformation matrix and the image with the detected markers and their poses
