import cv2 
import numpy as np 
import pyzed.sl as sl
import sys

def main() :
    #default vars
    error = False
    AngleValue = 0
    RotationValue = 0
    xOffset = 0
    xRes = 1920
    middleOfRes = xRes/2
    #vars
    #Green Tone, change based on tone of light. MAY BE TOO WIDE CURRENTLY
    #ITS IN GBR NOT RGB
    lowerBound=np.array([33,80,40])
    upperBound=np.array([102,255,255])

    zed = sl.Camera()

    input_type = sl.InputType()
    if len(sys.argv) >= 2 :
        input_type.set_from_svo_file(sys.argv[1])
    init = sl.InitParameters(input_t=input_type)
    init.camera_resolution = sl.RESOLUTION.HD1080
    init.depth_mode = sl.DEPTH_MODE.PERFORMANCE
    init.coordinate_units = sl.UNIT.MILLIMETER

    err = zed.open(init)
    if err != sl.ERROR_CODE.SUCCESS :
        print(repr(err))
        zed.close()
        exit(1)

    runtime = sl.RuntimeParameters()
    runtime.sensing_mode = sl.SENSING_MODE.STANDARD

    image_size = zed.get_camera_information().camera_resolution
    image_size.width = image_size.width / 2
    image_size.height = image_size.height / 2

    # Declare your sl.Mat matrices
    image_zed = sl.Mat(image_size.width, image_size.height, sl.MAT_TYPE.U8_C4)
    
    depth_image_zed = sl.Mat(image_size.width, image_size.height, sl.MAT_TYPE.U8_C4)
    point_cloud = sl.Mat()

    while True:
        err = zed.grab(runtime)
        if err == sl.ERROR_CODE.SUCCESS :
            # Retrieve the left image, depth image in the half-resolution
            zed.retrieve_image(image_zed, sl.VIEW.LEFT, sl.MEM.CPU, image_size)
            zed.retrieve_image(depth_image_zed, sl.VIEW.DEPTH, sl.MEM.CPU, image_size)
            # Retrieve the RGBA point cloud in half resolution
            zed.retrieve_measure(point_cloud, sl.MEASURE.XYZRGBA, sl.MEM.CPU, image_size)

            #LEFT IMAGE CONVERTED TO OPENCV READABLE FORMAT
            image_ocv = image_zed.get_data()
            depth_image_ocv = depth_image_zed.get_data()

            #uncomment if u have a display
            #cv2.imshow("Image", image_ocv)
            #cv2.imshow("Depth", depth_image_ocv)

            ret, image = image_ocv.read()
            #not sure if resize function will work
            frame = cv2.resize(image, (1920, 1080))

            imgHSV = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
       
            mask=cv2.inRange(imgHSV,lowerBound,upperBound)
            maskOpen=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernelOpen)
            maskClose=cv2.morphologyEx(maskOpen,cv2.MORPH_CLOSE,kernelClose)
            maskFinal=maskClose
            _, conts, _= cv2.findContours(maskFinal.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            #RUN THIS IF GREEN IS FOUND
            for i in range(len(conts)):
                c =  max(conts,key=cv2.contourArea)
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                M = cv2.moments(c)
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                if radius > 5:
                    x,y,w,h=cv2.boundingRect(conts[i])
                    cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255), 2)
                    xcenter = (int(M["m10"] / M["m00"]))
                    print(xcenter)
                    xOffset = int(xcenter - middleOfRes)
                    print(xOffset)
                    print(x)
                    err, point_cloud_value = point_cloud.get_value(x, y)
                    distance = math.sqrt(point_cloud_value[0] * point_cloud_value[0] + point_cloud_value[2] * point_cloud_value[2])
                    print(distance)
                    
                    
                else:
                    break

  
        else:
            #send network tables error, Bryon's time to pop off
            error = True

    #close everything down if it fails, WHICH IT WON'T
    cv2.destroyAllWindows()
    zed.close()


if __name__ == "__main__":
    main()
