from cmath import pi
import rospy
import time
from std_msgs.msg import String
from dynamixel_workbench_msgs.srv import DynamixelCommand
from sensor_msgs.msg import JointState
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
import numpy as np

def joint_publisher():
    publisher = rospy.Publisher('/joint_trajectory',JointTrajectory, queue_size=0)
    rospy.init_node('joint+publisher',anonymous=False)
    while not rospy.is_shutdown():
        state = JointTrajectory()
        state.header.stamp = rospy.Time.now()
        state.joint_names = ["joint_1"] #Configura la lista de nombres de las articulaciones 'joint_names' y agrega joint_1 a ella
        point = JointTrajectoryPoint()
        point.positions = [pi,pi,3.8,pi,0]#Almacenar una posicion
        point.time_from_start = rospy.Duration(3)#Tiempo en el cual se debe realizar la accion
        state.points.append(point)#Agrega 'point' a 'state'
        publisher.publish(state) #REaliza el publish
        print('Published command')
        rospy.sleep(1) #Retardo de 1s

def callback(data):
    global posicion_actual
    posicion_actual= np.multiply(data.position,180/pi)

def listener():
    rospy.init_node('joint_listener',anonymous=True)
    rospy.Subscriber("/dynamixel_workbench/joint_states",JointState,callback)

def joint_command(command,id,address_name,value,time):
    #('dynamixel_workbench/dynamixel_command')#Esperar hasta que el servicio este disponible
    try:
        dynamixel_command = rospy.ServiceProxy('/dynamixel_workbench/dynamixel_command',DynamixelCommand)#permite a un nodo enviar solicitudes a un servicio en otro nodo.
        result = dynamixel_command(command,id,address_name,value)#se envia la solicitud al sevicio
        rospy.sleep(time)
        return result.comm_result
    except rospy.ServiceException as exc:
        print(str(exc))



if __name__ == '__main__':
    try:
        listener()
        print("Universidad Nacional de Colombia")
        print("Facultad de Ingenieria")
        print("Robotica")
        print("Laboratorio 4")
        print("2023-2")
        print("Integrantes: Juan Barrera - Daniel Segura")
        Pos1=[21, 2038, 3060, 2038, 1779]
        Pos2=[290, 2326, 3360, 1060, 1779]
        Pos3=[3702,  2444,  3419, 2390, 1779]
        Pos4=[983, 1821, 3397, 2002, 1779]
        Pos5=[920 ,1655 , 3400, 1541, 1779]
        print("Las siguientes posiciones estan en grados, seleccione 1")
        print("Posicion 1: [0 180 270 180 150]")
        print("Posicion 2: [25 205 295 160 150 ]")
        print("Posicion 1: 325 215 300 210 150]")
        print("Posicion 1: [ 85 160 300 175 150]")
        print("Posicion 1: [80 145 300 135 150]")
        ListaPos=[Pos1,Pos2,Pos3,Pos4,Pos5]
        #joint_command('',1,'Torque_Limit',100,0)
        #joint_command('',1,'Goal_Position',63,0.5)
        #joint_command('',2,'Goal_Position',1998,0.5)
        #joint_command('',3,'Goal_Position',2675,0.5)
        #joint_command('',4,'Goal_Position',2666,0.5)
        #joint_command('',5,'Goal_Position',1553,0.5)
        while True:
            print(" ")
            numPosicion= int(input("Elija posicion: "))
            PosElegia=ListaPos[numPosicion-1]
            for i in range(5):
                #joint_command('',i+1,'Torque_Limit',70,0)
                joint_command('',i+1,'Goal_Position',PosElegia[i],2)
            print('')
            for i in range(5):
                #print("Posicion de la articulacion" + int(i) + ":")
                print(posicion_actual[i])
                print('')

    except rospy.ROSInterruptException:
        pass
    