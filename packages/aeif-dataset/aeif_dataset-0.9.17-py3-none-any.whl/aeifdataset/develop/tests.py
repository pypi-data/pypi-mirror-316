import aeifdataset as ad

import numpy as np
import open3d as o3d
from math import radians, cos, sqrt
from decimal import Decimal


def filter_points(points, x_range, y_range, z_range):
    x_min, x_max = x_range
    y_min, y_max = y_range
    z_min, z_max = z_range
    mask = (points['x'] < x_min) | (points['x'] > x_max) | \
           (points['y'] < y_min) | (points['y'] > y_max) | \
           (points['z'] < z_min) | (points['z'] > z_max)
    return points[mask]


def numpy_to_open3d(points):
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points[:, :3])  # Nur die x, y, z-Koordinaten
    return pcd


def structured_to_xyz(points):
    xyz = np.vstack((points['x'], points['y'], points['z'])).T  # Shape: (n, 3)
    return xyz


def preprocess_point_cloud(pcd, voxel_size):
    pcd_down = pcd.voxel_down_sample(voxel_size)
    pcd_down.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=voxel_size * 2, max_nn=30))
    fpfh = o3d.pipelines.registration.compute_fpfh_feature(
        pcd_down,
        o3d.geometry.KDTreeSearchParamHybrid(radius=voxel_size * 5, max_nn=100)
    )
    return pcd_down, fpfh


def flat_distance(lat1, lon1, lat2, lon2):
    # Umrechnung von Grad zu Metern
    lat_dist = (lat2 - lat1) * 111320  # Breitengradabstand in Metern
    lon_dist = (lon2 - lon1) * 111320 * cos(radians(lat1))  # Längengradabstand in Metern, angepasst an die Breite

    # Euklidischer Abstand
    distance = sqrt(lat_dist ** 2 + lon_dist ** 2)
    return distance


def find_matching_row(file_path: str, target_timestamp: Decimal) -> int:
    """
    Find the line number in the file where the timestamp matches the target timestamp with millisecond precision.

    Args:
        file_path (str): Path to the file containing timestamped data.
        target_timestamp (Decimal): Target timestamp to match.

    Returns:
        int: The line number that matches the timestamp, or -1 if no match is found.
    """
    # Convert the target timestamp to milliseconds
    target_timestamp_ms = target_timestamp // Decimal(1_000_000)

    # Open and read the file
    with open(file_path, 'r') as file:
        for line_number, line in enumerate(file, start=1):  # Start line_number at 1
            # Split each line and parse the timestamp
            parts = line.strip().split()
            file_timestamp_ms = Decimal(parts[0]) // Decimal(1_000_000)

            # Check for match with millisecond precision
            if file_timestamp_ms == target_timestamp_ms:
                return line_number  # Return the line number

    return -1  # Return -1 if no match is found


def read_line_by_number(file_path: str, line_number: int) -> str:
    """
    Read a specific line from a file by its line number.

    Args:
        file_path (str): Path to the file.
        line_number (int): The line number to read.

    Returns:
        str: The content of the line.
    """
    with open(file_path, 'r') as file:
        for current_line_number, line in enumerate(file, start=1):
            if current_line_number == line_number:
                return line.strip()

    raise ValueError(f"Line number {line_number} not found in file.")


def format_to_4x4_matrix(line_content: str) -> np.ndarray:
    """
    Convert a line of 12 pose values into a 4x4 transformation matrix.

    Args:
        line_content (str): Line containing 12 values as a string.

    Returns:
        np.ndarray: A 4x4 transformation matrix.
    """
    # Extract the 12 values from the line
    values = [float(x) for x in line_content.split()]

    if len(values) != 12:
        raise ValueError("Line content does not contain 12 values.")

    # Convert to a 4x4 matrix
    matrix = np.zeros((4, 4), dtype=np.float64)
    matrix[:3, :4] = np.array(values).reshape(3, 4)
    matrix[3, :] = [0, 0, 0, 1]  # Set the last row to [0, 0, 0, 1]
    return matrix


if __name__ == '__main__':
    save_dir = '/mnt/dataset/anonymisation/validation/27_09_seq_1/png'
    dataset = ad.Dataloader("/mnt/hot_data/dataset/seq_1")
    frame = ad.DataRecord('/mnt/hot_data/dataset/seq_1/id00021_2024-09-27_10-31-32.4mse')[18]
    # gps to kml file

    maneuvers = ad.get_maneuver_split('/mnt/hot_data/dataset/seq_1')

    for maneuver in maneuvers:
        import simplekml
        from datetime import datetime

        # KML-Datei erstellen
        kml = simplekml.Kml()

        # Positionen aus dem Manöver hinzufügen
        for record in maneuver:
            for frame in record:
                for pos in [frame.vehicle.GNSS.position[0]]:
                    # Sekunden und Nanosekunden extrahieren
                    raw_timestamp = pos.timestamp
                    seconds = raw_timestamp // 1_000_000_000  # Ganzzahlige Sekunden
                    nanoseconds = raw_timestamp % 1_000_000_000  # Restliche Nanosekunden

                    # Zeitstempel formatieren
                    timestamp = datetime.utcfromtimestamp(int(seconds))
                    formatted_timestamp = f"{timestamp.isoformat()}.{int(nanoseconds):09d}Z"

                    # Punkt hinzufügen
                    point = kml.newpoint(name="Position", coords=[(pos.longitude, pos.latitude)])
                    point.timestamp.when = formatted_timestamp  # Zeitstempel mit Nanosekunden

        # Fahrverlauf als Linie mit Zeitstempeln
        line = kml.newlinestring(name="Fahrverlauf")
        line.coords = [
            (frame.vehicle.GNSS.position[0].longitude, frame.vehicle.GNSS.position[0].latitude)
            for record in maneuver
            for frame in record
        ]
        line.style.linestyle.color = simplekml.Color.blue
        line.style.linestyle.width = 3

        # KML speichern
        kml.save("fahrverlauf_with_nanoseconds.kml")
        print("Fahrverlauf mit Nanosekundenpräzision in fahrverlauf_with_nanoseconds.kml gespeichert.")

    # Save one image as png or jpeg. Optional suffix can be applied.
    # ad.save_image(camera.image.image, output_path, f'{camera.image.get_timestamp()}_{camera_name}', dtype='jpeg')
    # ad.save_all_images_in_frame(frame, output_path, create_subdir=True)
    # ad.save_dataset_images_multithreaded(dataset, output_path, use_raw=True, num_cores=8)
    # Aktuelle Übereinstimmungen: 1831

    previous_transform = None
    fail_counter = 0
    match_counter = 0  # Zähler für erfolgreiche Übereinstimmungen

    for datarecord in dataset:
        for frame in datarecord:
            frame.vehicle.GNSS.position

    points_tower = frame.tower.lidars.UPPER_PLATFORM4
    points_vehicle = frame.vehicle.lidars.TOP

    points_tower_xyz = structured_to_xyz(points_tower)
    points_vehicle_xyz = structured_to_xyz(points_vehicle)

    # Open3D-Punktwolken für beide Sensoren erstellen
    pcd_tower = numpy_to_open3d(points_tower_xyz)
    pcd_vehicle = numpy_to_open3d(points_vehicle_xyz)

    # Parameter anpassen
    voxel_size = 1.0  # Größerer Wert für Downsampling und Feature-Berechnung
    distance_threshold = voxel_size * 5  # Größere Schwelle für RANSAC-Registrierung

    # Wenn entweder `previous_transform` leer ist oder der Fehlschlagzähler 3 erreicht hat, führe RANSAC aus
    if previous_transform is None or fail_counter >= 3:
        # Vorverarbeitung der Punktwolken und Berechnung von FPFH-Features
        pcd_tower_down, fpfh_tower = preprocess_point_cloud(pcd_tower, voxel_size)
        pcd_vehicle_down, fpfh_vehicle = preprocess_point_cloud(pcd_vehicle, voxel_size)

        ransac_result = o3d.pipelines.registration.registration_ransac_based_on_feature_matching(
            pcd_vehicle_down, pcd_tower_down, fpfh_vehicle, fpfh_tower,
            False,
            80.0,
            o3d.pipelines.registration.TransformationEstimationPointToPoint(False),
            5,
            [
                o3d.pipelines.registration.CorrespondenceCheckerBasedOnEdgeLength(0.7),
                o3d.pipelines.registration.CorrespondenceCheckerBasedOnDistance(80.0)
            ],
            o3d.pipelines.registration.RANSACConvergenceCriteria(500000, 500)
        )

        # Transformationsmatrix nach RANSAC
        initial_transform = ransac_result.mtx
        fail_counter = 0  # Fehlschlagzähler zurücksetzen
    else:
        # Nutze die vorherige Transformation als Initialisierung für ICP
        initial_transform = previous_transform

    # Feinausrichtung mit ICP
    threshold = 1.0  # Maximale Distanz für Paarbildung in ICP
    icp_result = o3d.pipelines.registration.registration_icp(
        pcd_vehicle, pcd_tower, threshold, initial_transform,
        o3d.pipelines.registration.TransformationEstimationPointToPoint()
    )

    transformation_matrix = icp_result.mtx

    # Bewertung der ICP-Registrierung
    fitness = icp_result.fitness
    inlier_rmse = icp_result.inlier_rmse

    # Überprüfung der Fitness- und RMSE-Bedingung
    if 0.6 < fitness < 0.8 and inlier_rmse < 0.367:
        # Setze die Transformation als `previous_transform` für den nächsten Durchlauf
        previous_transform = transformation_matrix
        fail_counter = 0  # Fehlschlagzähler zurücksetzen
        match_counter += 1  # Zähler für erfolgreiche Übereinstimmung erhöhen
    else:
        # Falls die Bedingungen nicht erfüllt sind, erhöhe den Fehlschlagzähler
        fail_counter += 1
    print(f"Aktuelle Übereinstimmungen: {match_counter}")

    timestamp_file = "/home/ameise/workspace/GlobalRegistration/venv/bin/results/2024-12-13_13-09-39/seq_1#00699-01399_poses_tum.txt"
    data_file = "/home/ameise/workspace/GlobalRegistration/venv/bin/results/2024-12-13_13-09-39/seq_1#00699-01399_poses_kitti.txt"
    target_timestamp = frame.timestamp

    matching_line_number = find_matching_row(timestamp_file, target_timestamp)

    if matching_line_number != -1:
        # Read the corresponding line from the data file
        matching_line_content = read_line_by_number(data_file, matching_line_number)
        # Format the line as a 4x4 matrix
        matrix = format_to_4x4_matrix(matching_line_content)
    else:
        print("No matching line found.")

    # Inverse der Fahrzeug-zu-Turm-Transformation (Tower → Vehicle)
    tower_to_vehicle_transform = np.linalg.inv(transformation_matrix)

    # Endgültige Transformation von Tower → Global
    tower_to_global_transform = np.dot(matrix, tower_to_vehicle_transform)

    # Punkte im Tower-Koordinatensystem transformieren
    tower_points_global = np.dot(tower_to_global_transform,
                                 np.hstack((points_tower_xyz, np.ones((points_tower_xyz.shape[0], 1)))).T).T

    # Transformation ausgeben
    print("Tower to Global Transformation Matrix:")
    print(tower_to_global_transform)

    '''
    # Transformiere die Fahrzeug-Punktwolke mit der resultierenden Transformationsmatrix
    pcd_vehicle_transformed = pcd_vehicle.transform(transformation_matrix)

    # Visualisierung vorbereiten
    pcd_tower.paint_uniform_color([1, 0, 0])  # Turm-Punktwolke rot färben
    pcd_vehicle_transformed.paint_uniform_color([0, 1, 0])  # Fahrzeug-Punktwolke grün färben

    # Open3D-Visualizer starten
    o3d.visualization.draw_geometries(
        [pcd_tower, pcd_vehicle_transformed],
        zoom=0.7,
        front=[0.0, 0.0, -1.0],  # Ansicht nach vorne
        lookat=[0.0, 0.0, 0.0],  # Mittelpunkt der Ansicht
        up=[0.0, -1.0, 0.0]  # Oben-Achse nach oben ausgerichtet
    )

    frame = dataset[0][0]
    for datarecord in dataset:
        for frame in datarecord:
            speed = np.linalg.norm(frame.vehicle.DYNAMICS.velocity[0].linear_velocity) * 3.6
            if speed < 1:
                print(f'Datarecord: {datarecord.name}, Frame: {frame.frame_id}')
    
    image = frame.vehicle.cameras.STEREO_LEFT
    
    
    points_left = frame.vehicle.lidars.LEFT
    points_top = frame.vehicle.lidars.TOP
    points_right = frame.vehicle.lidars.RIGHT
    
        ad.show_points(
        (points_left, (255, 0, 0)),
        (points_top, (0, 255, 0)),
        (points_right, (0, 0, 255))
    )

    ad.show_points(
        (points_left, (255, 0, 0)),
        (points_top, (0, 255, 0))
    )
    
    xyz_points = np.stack(
        (points_left['x'], points_left['y'], points_left['z']), axis=-1)
    visualize_lidar_points(xyz_points, title='Upper Platform LiDAR Point Cloud')
    
    LEFT
    x_range = (-2.9, 1.8)
    y_range = (-1.7, 1.6)
    z_range = (-2.8, 0.2)

    RIGHT
    x_range = (-1.2, 1.5)
    y_range = (-0.6, 1.7)
    z_range = (-1.1, 0)
    
    new_pts = filter_points(points_right, x_range, y_range, z_range)
    coordinates = np.vstack((new_pts['x'], new_pts['y'], new_pts['z'])).T
    ad.show_points(points_right)
    
    ad.save_image(image, '/mnt/hot_data/samples')
    ad.show_points(points)

    ad.show_tf_correction(image, points, -0.003, -0.01, -0.004)
    ad.get_projection_img(image, points).show()
    ad.get_projection_img(image2, points).show()
    '''
