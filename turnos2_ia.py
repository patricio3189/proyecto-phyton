#esto podemos usarlo de modelo para la plantilla turnos
#podriamos analizarlo y aprender de este codigo


turnos = []

def agregar_paciente():
    nombre_paciente = input("Ingrese el nombre y apellido del paciente: ")
    edad_paciente = input("Ingrese la edad del paciente: ")
    dni_paciente = input("Ingrese el DNI del paciente: ")
    telefono_paciente = input("Ingrese el teléfono del paciente: ")
    paciente = {
        "nombre_apellido": nombre_paciente,
        "edad": edad_paciente,
        "dni": dni_paciente,
        "telefono": telefono_paciente
    }
    return paciente

def mostrar_medicos():
    print("Lista de médicos:")
    for idx, medico in enumerate(medicos):
        print(f"{idx+1}. {medico['nombre_apellido']}")

def agendar_turno():
    paciente = agregar_paciente()
    mostrar_medicos()
    opcion = int(input("Seleccione el número del médico: ")) - 1
    medico = medicos[opcion]
    fecha = input("Ingrese la fecha del turno (dd/mm/aaaa): ")
    turno = {
        "paciente": paciente,
        "medico": medico,
        "fecha": fecha
    }
    turnos.append(turno)
    print("Turno agendado correctamente.")
