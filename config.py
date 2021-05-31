#Face Detector parameters
NETWORK_TYPE = 'mobile0.25'
FACE_DETECTION_RESOLUTION = (300,300)
CPU = False
TRAINED_MODEL_RES = 'models/retinaface/weights/Resnet50_Final.pth'
TRAINED_MODEL_MOBILE = './models/retinaface/weights/mobilenet0.25_Final.pth'
TRAINED_MODEL_MOBILE_PRETRAIN = "./models/retinaface/weights/mobilenetV1X0.25_pretrain.tar"
TRAINED_MODEL_LANDMARKS = 'models/landmark_detector/shape_predictor_68_face_landmarks.dat'
SAVE_FOLDER = './results/'
ORIGIN_SIZE = False
CONFIDENCE_THRESHOLD = 0.02
TOP_K = 5000
NMS_THRESHOLD =0.4
KEEP_TOP_K = 750
SAVE_IMAGE=False
SHOW_IMAGE=True
VIS_THRESH =0.5

#Light weight Face Dector parameters
CONFIDENCE_THRESHOLD_LW = 0.6
CANDIDATE_SIZE_LW = 1500
INPUT_SIZE_LW = 640
TRAINED_MODEL_SLIM_320 ="./models/ulfg_fd//models/pretrained/version-slim-320.pth"
TRAINED_MODEL_SLIM_640 =   "./models/ulfg_fd/models/pretrained/version-slim-640.pth"
TRAINED_MODEL_RFB_320 = "./models/ulfg_fd/models/pretrained/version-RFB-320.pth"
TRAINED_MODEL_RFB_640 = "./models/ulfg_fd/models/pretrained/version-RFB-640.pth"

#display paramaeters
MODE_OFFSETX = 0
MODE_OFFSETY = 0
MODE_SETWIDTH = 3840    #max screen resolution
#MODE_SETWIDTH =  4096  #max blackfly resolution
MODE_SETHEIGHT = 2160   #max screen resoltion
#MODE_SETHEIGHT = 3000  #max blackfly resolution

#max roll angle for face
MAX_ROLL_ANGLE = 5

#minium face bounding box for cropping image
MIN_BBOX_SIZE = 50


#FOCAL LENGTH OF CAMERAS
FOCAL_LENGTH_BLACKFLY = 0.012

#FOCAL LENGTH OPEN MV CAMERA
FOCAL_LENGTH_OPENMV = 0.0028